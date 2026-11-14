"""Versioned claim evidence and bounded research feedback; never promote state."""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import json
from typing import Any


def _items(value: Any) -> list:
    return value if isinstance(value, list) else []


def _key(reference: dict) -> tuple[str, str]:
    return PurePosixPath(reference.get("path", "")).as_posix(), reference.get("sha256", "")


def _load(reference: Any, issues: list, ctl: Any, code: str, schema: str | None = None) -> tuple[Path, dict] | None:
    before = len(issues)
    ctl.check_maybe_hashed_file(reference, issues, code, require_hash=True)
    if len(issues) != before or not isinstance(reference, dict):
        return None
    path = ctl.project_path(reference["path"])
    if path is None or not path.is_file():
        return None
    try:
        value = ctl.load_json(path)
    except (SystemExit, OSError) as exc:
        ctl.add_issue(issues, "error", code + "_JSON", str(exc))
        return None
    if schema:
        ctl.validate_json_schema(value, ctl.ROOT / "schemas" / (schema + ".schema.json"), issues, code + "_SCHEMA", str(path.relative_to(ctl.ROOT)))
    return None if len(issues) != before else (path, value)


def validate_project(sessions: list[tuple[Path, dict]], issues: list, ctl: Any) -> None:
    """Validate v1.3 evidence across sessions, allowing reuse of frozen versions."""
    manifest_schema = json.loads((ctl.ROOT / "schemas/run-manifest.schema.json").read_text())
    sessions = [(directory, manifest) for directory, manifest in sessions
                if not ctl._schema_errors(manifest, manifest_schema, manifest_schema, "manifest")]
    records: dict[tuple[str, str], dict] = {}
    loading: set[tuple[str, str]] = set()
    revisions: dict[tuple[str, str], str] = {}

    def error(code: str, message: str) -> None:
        ctl.add_issue(issues, "error", code, message)

    def load_claim(reference: Any) -> dict | None:
        if not isinstance(reference, dict):
            error("CLAIM_REFERENCE", "claim evidence must be a hashed reference")
            return None
        if not all(isinstance(reference.get(field), str) for field in ("path", "sha256")):
            error("CLAIM_REFERENCE", "claim evidence needs string path and hash")
            return None
        key = _key(reference)
        if key in loading:
            error("CLAIM_EVIDENCE_CYCLE", f"cyclic version dependency at {key[0]}")
            return None
        if key in records:
            return records[key]
        loaded = _load(reference, issues, ctl, "CLAIM_EVIDENCE", "claim-evidence")
        if loaded is None:
            return None
        path, claim = loaded
        revision_key = claim["claim_id"], claim["revision"]
        if revision_key in revisions and revisions[revision_key] != key[1]:
            error("CLAIM_REVISION_CONFLICT", f"{revision_key}: distinct contents use the same claim version")
        revisions[revision_key] = key[1]
        for field in ("target", "proof"):
            ctl.check_maybe_hashed_file(claim[field], issues, "CLAIM_" + field.upper(), require_hash=True)
        loading.add(key)
        for dependency in claim["depends_on"]:
            parent = load_claim(dependency["record"])
            if parent and (parent["claim_id"], parent["revision"]) != (dependency["claim_id"], dependency["revision"]):
                error("CLAIM_DEPENDENCY_VERSION", f"{path.relative_to(ctl.ROOT)}: dependency identity/version mismatch")
        previous_ref = claim["supersedes"]
        if previous_ref is not None:
            previous = load_claim(previous_ref)
            if previous and (previous["claim_id"] != claim["claim_id"] or int(previous["revision"][1:]) >= int(claim["revision"][1:])):
                error("CLAIM_SUPERSESSION", f"{path.relative_to(ctl.ROOT)}: supersession must advance a version of the same claim")
        if (previous_ref is None) != (claim["change_kind"] == "initial"):
            error("CLAIM_CHANGE_KIND", f"{path.relative_to(ctl.ROOT)}: a revision must identify the version it supersedes")
        loading.remove(key)
        records[key] = claim
        return claim

    indexed: dict[Path, dict[tuple[str, str], dict]] = {}
    reviews: dict[Path, dict[tuple[str, str], dict]] = {}
    for directory, manifest in sessions:
        selected = indexed.setdefault(directory, {})
        for reference in _items(manifest.get("claim_records")):
            claim = load_claim(reference)
            if claim:
                selected[_key(reference)] = claim
        reviewed = reviews.setdefault(directory, {})
        for reference in _items(manifest.get("critical_reviews")):
            loaded = _load(reference, issues, ctl, "CLAIM_REVIEW", "critical-review")
            if loaded is None:
                continue
            path, review = loaded
            ctl.validate_critical_review(review, path, issues)
            if review.get("schema_version") != "1.1":
                error("CLAIM_REVIEW_VERSION", f"{path.relative_to(ctl.ROOT)}: versioned claims require a v1.1 review")
                continue
            claim = load_claim(review["claim_record"])
            key = _key(review["claim_record"])
            if key not in selected:
                error("CLAIM_REVIEW_UNINDEXED", f"{path.relative_to(ctl.ROOT)}: reviewed claim is absent from this session index")
            if claim and ((claim["claim_id"], claim["revision"]) != (review["claim_id"], review["revision"]) or claim["proof"] != review["candidate"]):
                error("CLAIM_REVIEW_SCOPE", f"{path.relative_to(ctl.ROOT)}: review covers a different statement, proof, or revision")
            if key in reviewed:
                # A later selected verdict must never silently replace an earlier rejection.
                error("CLAIM_REVIEW_DUPLICATE", f"{path.relative_to(ctl.ROOT)}: select one authoritative assessment per exact version; preserve others as history")
            reviewed[key] = review
        for reference in _items(manifest.get("checks")):
            loaded = _load(reference, issues, ctl, "SESSION_CHECK", "check-result")
            if loaded is not None:
                import checkctl
                for message in checkctl.inspect_result(loaded[1], ctl.ROOT):
                    error("SESSION_CHECK_INTEGRITY", f"{loaded[0].relative_to(ctl.ROOT)}: {message}")
        for step in _items(manifest.get("compute_steps")):
            if not isinstance(step, dict):
                continue  # schema diagnostics are authoritative for shape
            if step.get("status") in {"completed", "stopped"}:
                elapsed, outcome = step.get("elapsed_seconds"), step.get("outcome")
                if elapsed is None or not outcome:
                    error("COMPUTE_RECEIPT", f"{directory.relative_to(ctl.ROOT)}: completed compute step needs measured time and outcome")
                if isinstance(elapsed, (float, int)) and elapsed > step.get("max_seconds", float("inf")) and step.get("status") != "stopped":
                    error("COMPUTE_BUDGET", f"{directory.relative_to(ctl.ROOT)}: exceeded time budget must stop and be recorded")
                cost, limit = step.get("cost_usd"), step.get("max_cost_usd")
                if isinstance(cost, (int, float)) and isinstance(limit, (int, float)) and cost > limit and step.get("status") != "stopped":
                    error("COMPUTE_BUDGET", f"{directory.relative_to(ctl.ROOT)}: exceeded cost budget must stop and be recorded")
        progress = manifest.get("progress", {})
        if manifest.get("status") == "completed" and isinstance(progress, dict):
            if progress.get("kind") == "not_assessed" or not progress.get("explanation"):
                error("INFORMATION_GAIN_REQUIRED", f"{directory.relative_to(ctl.ROOT)}: explain the mathematical information gained, or explicitly why none was gained")

    superseded = {_key(claim["supersedes"]) for claim in records.values() if claim["supersedes"] is not None and claim["change_kind"] == "substantive"}
    stale = set(superseded)
    changed = True
    while changed:
        changed = False
        for key, claim in records.items():
            if key not in stale and any(_key(dep["record"]) in stale for dep in claim["depends_on"]):
                stale.add(key)
                changed = True
    for key in sorted(stale):
        if key in records:
            claim = records[key]
            ctl.add_issue(issues, "warning", "CLAIM_RECHECK_REQUIRED", f"{claim['claim_id']} {claim['revision']}: version/dependency changed; withhold reuse pending recheck, canonical status is unchanged")

    def gate(directory: Path, manifest: dict, required_ids: set[str] | None = None) -> set[tuple[str, str]]:
        selected = indexed[directory]
        if required_ids is not None:
            selected = {key: claim for key, claim in selected.items() if claim["claim_id"] in required_ids}
        if not selected:
            error("CLAIM_SNAPSHOT_REQUIRED", f"{directory.relative_to(ctl.ROOT)}: key evidence needs an indexed claim/proof version")
        meaning = manifest.get("meaning_audit", {})
        if not isinstance(meaning, dict) or meaning.get("status") != "matched" or not meaning.get("note"):
            error("STATEMENT_MEANING_GATE", f"{directory.relative_to(ctl.ROOT)}: confirm that the result answers the intended target")
        passed = set()
        for key, claim in selected.items():
            review = reviews[directory].get(key)
            if key in stale:
                error("STALE_CLAIM_USE", f"{claim['claim_id']} {claim['revision']}: stale evidence cannot clear a formal gate")
                continue
            if claim["meaning_audit"]["status"] != "matched" or not claim["meaning_audit"]["note"] or not claim["novelty"]["note"]:
                error("CLAIM_MEANING_GATE", f"{claim['claim_id']} {claim['revision']}: document target correspondence and prior-work/novelty standing")
                continue
            if not review or review["review_kind"] != "independent" or review["verdict"] != "survives_current_attacks":
                error("CLAIM_REVIEW_REQUIRED", f"{claim['claim_id']} {claim['revision']}: a surviving independent assessment of this exact version is required")
                continue
            passed.add(key)
        return passed

    for directory, manifest in sessions:
        if manifest.get("critical_review") is not None:
            error("SESSION_REVIEW_FORMAT", f"{directory.relative_to(ctl.ROOT)}: use versioned critical_reviews for v1.3; leave historical v1.2 records unchanged")
        if manifest.get("route_signal") == "decisive_support" or (manifest.get("status") == "completed" and manifest.get("critical_review_required")):
            gate(directory, manifest)
        paths = {directory / "state-transition.json"}
        reference = manifest.get("state_transition")
        if isinstance(reference, dict):
            path = ctl.project_path(reference.get("path", ""))
            if path is not None:
                paths.add(path)
        for path in paths:
            if not path.is_file():
                continue
            try:
                transition = ctl.load_json(path)
            except (SystemExit, OSError):
                continue  # main validator reports malformed transitions
            if not ctl.transition_requires_review(transition):
                continue
            evidence = {}
            for reference in _items(manifest.get("task_records")):
                loaded = _load(reference, issues, ctl, "TRANSITION_TASK", "task-evidence")
                if loaded and loaded[0].parent == directory and loaded[0].stem == loaded[1].get("task_id"):
                    evidence[loaded[0].stem] = loaded[1]
            cited = [evidence.get(task_id) for task_id in _items(transition.get("evidence_records")) if isinstance(task_id, str)]
            if not cited or any(task is None for task in cited):
                error("TRANSITION_EVIDENCE_LINK", f"{path.relative_to(ctl.ROOT)}: cite manifest-indexed local evidence task IDs")
                continue
            claim_ids = {claim_id for task in cited if task for claim_id in task.get("proof_items", [])}
            reviewed_changes = [item for item in transition.get("changes", {}).get("claims", [])
                                if ctl.transition_requires_review({"changes": {"claims": [item]}})]
            if any(not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in reviewed_changes):
                error("TRANSITION_CLAIM_COVERAGE", f"{path.relative_to(ctl.ROOT)}: formal claim changes need explicit claim IDs")
            changed_ids = {item["id"] for item in reviewed_changes if isinstance(item, dict) and isinstance(item.get("id"), str)}
            if not claim_ids or not changed_ids.issubset(claim_ids):
                error("TRANSITION_CLAIM_COVERAGE", f"{path.relative_to(ctl.ROOT)}: cited evidence does not identify every changed claim")
            passed = gate(directory, manifest, claim_ids)
            for task in cited:
                if not task:
                    continue
                if task.get("evidence_class") == "numerical" and changed_ids:
                    error("NUMERICAL_PROMOTION", f"{path.relative_to(ctl.ROOT)}: numerical evidence cannot discharge an analytic proof gate")
                covered = {indexed[directory][key]["claim_id"] for key in passed if indexed[directory][key]["proof"] == task.get("artifact")}
                if not set(task.get("proof_items", [])).issubset(covered) or not task.get("derivation_roots"):
                    error("TRANSITION_EVIDENCE_SCOPE", f"{path.relative_to(ctl.ROOT)}: evidence must cover the exact reviewed claim/proof revision")
                if task.get("status") in {"planned", "dispatched", "critic_pending"} or task.get("verdict") in {"proposal_only", "uncertain"}:
                    error("TRANSITION_EVIDENCE_PENDING", f"{path.relative_to(ctl.ROOT)}: pending evidence cannot support promotion")


def affected(state: dict, claim_id: str) -> list[str]:
    """Read-only transitive dependents in the canonical claim graph."""
    found = {claim_id}
    while True:
        added = {claim["id"] for claim in state.get("claims", []) if set(claim.get("depends_on", [])) & found}
        if added.issubset(found):
            return sorted(found - {claim_id})
        found |= added
