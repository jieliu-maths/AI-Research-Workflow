#!/usr/bin/env python3
"""Deterministic control-plane checks for a proof-ledger research workflow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "research" / "machine" / "project-state.json"
SCHEMA_PATH = ROOT / "schemas" / "research-state.schema.json"
TEMPLATE_PATH = ROOT / "dashboard" / "template.html"
DASHBOARD_PATH = ROOT / "dashboard" / "index.html"
PROPOSAL_PATH = ROOT / "research" / "machine" / "project-state.proposal.json"
PROPOSAL_DASHBOARD_PATH = ROOT / "dashboard" / "proposal-preview.html"
REPORT_DIR = ROOT / "report"
REPORT_MD_PATH = REPORT_DIR / "project-summary.md"
REPORT_TEX_PATH = REPORT_DIR / "project-summary.tex"
REPORT_PDF_PATH = REPORT_DIR / "project-summary.pdf"
CORE_RESEARCH_FILES = (
    "PROJECT_CHARTER.md",
    "STATE.md",
    "research/problem.md",
    "research/proof_ledger.md",
    "research/proof_map.md",
    "research/route_matrix.md",
    "research/notation.md",
    "research/assumptions.md",
    "research/open_questions.md",
    "research/research_log.md",
)
RUNS_PATH = ROOT / "runs"
WORKSPACE_ROLES_PATH = ROOT / "research" / "machine" / "workspace-roles.json"
WORKSPACE_ROLES_TEMPLATE_PATH = ROOT / "research" / "machine" / "_template" / "workspace-roles.json"
SIDECAR_SCHEMAS = (
    ROOT / "schemas" / "run-manifest.schema.json",
    ROOT / "schemas" / "task-evidence.schema.json",
    ROOT / "schemas" / "state-transition.schema.json",
    ROOT / "schemas" / "state-mapping-proposal.schema.json",
    ROOT / "schemas" / "run-hydration-proposal.schema.json",
    ROOT / "schemas" / "workspace-roles.schema.json",
    ROOT / "schemas" / "orchestration.schema.json",
    ROOT / "schemas" / "route-review.schema.json",
)
TEMPLATE_CONTRACTS = {
    "runs/_template/brief.md": ("template_version: 2.4.0", "state_in:", "theorem_targets:", "machine_record:", "orchestration_record:", "route_approval_reference:", "route_id:", "## Candidate preflight plan"),
    "runs/_template/task-brief.md": ("template_version: 2.4.0", "strict_prerequisites:", "non_strict_links:", "blocking_reason:", "evidence_class:", "derivation_roots:", "independence_from:", "machine_record:", "dispatch_sha256:", "route_id:", "candidate_class:", "canonical_topology:", "quotient_dependencies:", "scaling_regime:", "stress_tests:", "symbol_scope:"),
    "runs/_template/learning-note-Txxx.md": ("template_version: 2.4.0", "## Mathematical objective", "## Decisive formula", "## Proof consequence", "## Cheapest reusable preflight tests", "## What remains unresolved"),
    "runs/_template/status.md": ("template_version: 2.4.0", "Proof items", "Strict prerequisites", "Non-strict links", "Evidence class", "Machine record", "Gate", "Authoritative decision artifact", "director_state:", "route_signal:", "Route evidence review trigger"),
    "runs/_template/amendments.md": ("template_version: 2.4.0", "evidence and SHA-256", "derivation roots", "machine record", "human authorization"),
    "runs/_template/resolution-Txxx.md": ("template_version: 2.4.0", "researcher_sha256:", "critic_sha256:", "derivation_roots:", "machine_record:", "## Candidate scope after correction"),
    "runs/_template/state_update_proposal.md": ("template_version: 2.4.0", "state_from:", "state_to_proposed:", "owner_approval_reference:", "## Proposed claim changes", "## Proposed route changes"),
    "runs/_template/director-run-summary.md": ("template_version: 2.4.0", "## Current theorem target", "## Decisive formula", "## Consequence for the proof map", "## Candidate scope and unexcluded alternatives", "## What remains open", "## Route evidence assessment", "## Owner approvals requested"),
    "runs/_template/route-review.md": ("template_version: 2.4.0", "## Original route thesis", "## Researcher synthesis", "## Systematic literature refresh driven by the obstruction", "## Independent Critic assessment", "## Director recommendation", "## Owner decision required"),
    "research/machine/_template/project-state.proposal.json": ('"status": "proposal_only"', '"unresolved_mappings"', '"candidate_state"'),
    "research/machine/_template/workspace-roles.json": ('"schema_version": "1.1"', '"topology": "peer_tasks"', '"shared_project_directory": true', '"title": "0 Director"', '"title": "1 Researcher"', '"title": "2 Critic"', '"is_current_task": true'),
}

SCHEMA_BY_KIND = {
    "state": ROOT / "schemas" / "research-state.schema.json",
    "manifest": ROOT / "schemas" / "run-manifest.schema.json",
    "task": ROOT / "schemas" / "task-evidence.schema.json",
    "transition": ROOT / "schemas" / "state-transition.schema.json",
    "mapping": ROOT / "schemas" / "state-mapping-proposal.schema.json",
    "hydration": ROOT / "schemas" / "run-hydration-proposal.schema.json",
    "roles": ROOT / "schemas" / "workspace-roles.schema.json",
    "orchestration": ROOT / "schemas" / "orchestration.schema.json",
    "route_review": ROOT / "schemas" / "route-review.schema.json",
}

CLAIM_STATUSES = {
    "open",
    "conditional",
    "conjectural",
    "formal",
    "external_input",
    "formal_exact",
    "established",
    "manuscript_unaudited",
    "selected_unverified",
    "deferred",
    "verified",
    "numerical",
    "rejected",
}
RESOLVED_CLAIM_STATUSES = {"verified", "formal_exact", "established"}
CANONICAL_ROUTE_STATUSES = {"proposed", "active", "closed", "rejected"}
OPERATIONAL_ROUTE_STATUSES = {"planned", "running", "completed", "rejected", "gated"}
RUN_STATUSES = {"planned", "running", "gated", "completed", "aborted", "rejected"}
EVIDENCE_VERDICTS = {
    "supports",
    "rejects_route",
    "uncertain",
    "survives_current_attacks",
    "proposal_only",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError as exc:
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"expected an object in {path.relative_to(ROOT)}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_path(relative: str) -> Path | None:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    candidate = ROOT / rel
    current = ROOT
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            return None
    try:
        candidate.resolve(strict=False).relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def add_issue(
    issues: list[dict[str, str]], severity: str, code: str, message: str
) -> None:
    issues.append({"severity": severity, "code": code, "message": message})


def _schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _resolve_local_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"only local schema references are supported: {reference}")
    current: Any = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or token not in current:
            raise ValueError(f"unresolved schema reference: {reference}")
        current = current[token]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference is not an object: {reference}")
    return current


def _schema_errors(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    location: str,
) -> list[str]:
    errors: list[str] = []
    if "$ref" in schema:
        return _schema_errors(value, _resolve_local_ref(root_schema, schema["$ref"]), root_schema, location)
    if "allOf" in schema:
        for branch in schema["allOf"]:
            errors.extend(_schema_errors(value, branch, root_schema, location))
    if "oneOf" in schema:
        branch_results = [_schema_errors(value, branch, root_schema, location) for branch in schema["oneOf"]]
        matches = sum(not result for result in branch_results)
        if matches != 1:
            errors.append(f"{location}: must match exactly one allowed form")
            return errors
    if "if" in schema and not _schema_errors(value, schema["if"], root_schema, location):
        errors.extend(_schema_errors(value, schema.get("then", {}), root_schema, location))
    elif "if" in schema and "else" in schema:
        errors.extend(_schema_errors(value, schema["else"], root_schema, location))

    expected = schema.get("type")
    if expected is not None:
        choices = expected if isinstance(expected, list) else [expected]
        if not any(_schema_type_matches(value, item) for item in choices):
            errors.append(f"{location}: expected type {' or '.join(choices)}")
            return errors
    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value {value!r} is not allowed")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{location}: string is too short")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{location}: does not match {schema['pattern']}")
        if schema.get("format") == "date":
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                errors.append(f"{location}: expected an ISO date")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{location}: expected an ISO date-time")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: has too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{location}: has too many items")
        if schema.get("uniqueItems"):
            frozen = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(frozen) != len(set(frozen)):
                errors.append(f"{location}: items must be unique")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                errors.extend(_schema_errors(item, schema["items"], root_schema, f"{location}[{index}]"))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{location}: missing required field {field}")
        properties = schema.get("properties", {})
        for field, field_value in value.items():
            if field in properties:
                errors.extend(_schema_errors(field_value, properties[field], root_schema, f"{location}.{field}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{location}: unexpected field {field}")
    return errors


def validate_json_schema(
    value: Any,
    schema_path: Path,
    issues: list[dict[str, str]],
    code: str,
    location: str,
) -> None:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors = _schema_errors(value, schema, schema, location)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        add_issue(issues, "error", f"{code}_ENGINE", f"{schema_path.relative_to(ROOT)}: {exc}")
        return
    for message in errors:
        add_issue(issues, "error", code, message)


def check_hashed_file(
    record: dict[str, Any], issues: list[dict[str, str]], code_prefix: str
) -> None:
    relative = record.get("path")
    expected = record.get("sha256")
    if not isinstance(relative, str) or not relative:
        add_issue(issues, "error", f"{code_prefix}_PATH", "missing file path")
        return
    if not isinstance(expected, str) or len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
        add_issue(
            issues,
            "error",
            f"{code_prefix}_HASH_FORMAT",
            f"{relative}: expected a 64-character SHA-256",
        )
        return
    path = project_path(relative)
    if path is None:
        add_issue(issues, "error", f"{code_prefix}_ESCAPE", f"{relative}: path leaves the project or crosses a symlink")
        return
    if not path.is_file():
        add_issue(issues, "error", f"{code_prefix}_MISSING", f"missing {relative}")
        return
    actual = sha256(path)
    if actual != expected:
        add_issue(
            issues,
            "error",
            f"{code_prefix}_DRIFT",
            f"{relative}: recorded {expected[:12]}..., actual {actual[:12]}...",
        )


def check_maybe_hashed_file(
    record: Any,
    issues: list[dict[str, str]],
    code_prefix: str,
    *,
    require_hash: bool,
    check_path: bool = True,
) -> None:
    if not isinstance(record, dict):
        add_issue(issues, "error", f"{code_prefix}_RECORD", "expected a file reference object")
        return
    relative, expected = record.get("path"), record.get("sha256")
    if not isinstance(relative, str) or not relative:
        add_issue(issues, "error", f"{code_prefix}_PATH", "missing file path")
        return
    if expected is None and not require_hash:
        return
    if not isinstance(expected, str) or len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
        add_issue(issues, "error", f"{code_prefix}_HASH_FORMAT", f"{relative}: expected a 64-character SHA-256")
        return
    if check_path:
        path = project_path(relative)
        if path is None:
            add_issue(issues, "error", f"{code_prefix}_ESCAPE", f"{relative}: path leaves the project or crosses a symlink")
            return
        if not path.is_file():
            add_issue(issues, "error", f"{code_prefix}_MISSING", f"missing {relative}")
        elif sha256(path) != expected:
            add_issue(issues, "error", f"{code_prefix}_DRIFT", f"{relative}: recorded hash does not match the file")


def check_path_reference(
    record: Any, issues: list[dict[str, str]], code_prefix: str, *, check_path: bool
) -> Path | None:
    if not isinstance(record, dict) or set(record) != {"path"}:
        add_issue(issues, "error", f"{code_prefix}_RECORD", "expected an object containing only path")
        return None
    relative = record.get("path")
    if not isinstance(relative, str) or not relative:
        add_issue(issues, "error", f"{code_prefix}_PATH", "missing file path")
        return None
    path = project_path(relative)
    if path is None:
        add_issue(issues, "error", f"{code_prefix}_ESCAPE", f"{relative}: path leaves the project or crosses a symlink")
        return None
    if check_path and not path.is_file():
        add_issue(issues, "error", f"{code_prefix}_MISSING", f"missing {relative}")
        return None
    return path


def validate_sidecar_schemas(issues: list[dict[str, str]]) -> None:
    for path in SIDECAR_SCHEMAS:
        if not path.is_file():
            add_issue(issues, "error", "SIDECAR_SCHEMA_MISSING", f"missing {path.relative_to(ROOT)}")
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            add_issue(issues, "error", "SIDECAR_SCHEMA_JSON", f"{path.relative_to(ROOT)}: {exc}")
            continue
        if value.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            add_issue(issues, "error", "SIDECAR_SCHEMA_DIALECT", f"{path.relative_to(ROOT)}: expected draft 2020-12")
    for relative, tokens in TEMPLATE_CONTRACTS.items():
        path = ROOT / relative
        if not path.is_file():
            add_issue(issues, "error", "RUN_TEMPLATE_MISSING", f"missing {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                add_issue(issues, "error", "RUN_TEMPLATE_FIELD", f"{relative}: missing contract token {token!r}")


def validate_run_manifest(value: dict[str, Any], path: Path, issues: list[dict[str, str]], *, template: bool = False) -> None:
    validate_json_schema(value, SCHEMA_BY_KIND["manifest"], issues, "MANIFEST_SCHEMA_RULE", str(path.relative_to(ROOT)))
    required = {"schema_version", "run_id", "route_id", "state_in", "status", "brief", "route_approval_reference", "task_records", "director_summary", "state_transition"}
    version = value.get("schema_version")
    if version == "1.1" or template:
        required |= {"orchestration", "route_signal", "route_review"}
    for field in sorted(required - value.keys()):
        add_issue(issues, "error", "MANIFEST_FIELD", f"{path.relative_to(ROOT)}: missing {field}")
    run_id, route_id, status = value.get("run_id"), value.get("route_id"), value.get("status")
    if version == "1.0" and not template:
        add_issue(issues, "warning", "MANIFEST_LEGACY_SCHEMA", f"{path.relative_to(ROOT)}: v1.0 has no Director orchestration or route signal")
    elif version != "1.1":
        add_issue(issues, "error", "MANIFEST_SCHEMA", f"{path.relative_to(ROOT)}: expected manifest schema 1.1")
    if not isinstance(run_id, str) or not re.fullmatch(r"R[0-9]+", run_id):
        add_issue(issues, "error", "MANIFEST_ID", f"{path.relative_to(ROOT)}: invalid schema_version or run_id")
    if route_id is not None and (not isinstance(route_id, str) or not re.fullmatch(r"route:[A-Za-z0-9][A-Za-z0-9._-]*", route_id)):
        add_issue(issues, "error", "MANIFEST_ROUTE", f"{path.relative_to(ROOT)}: invalid route_id")
    if status not in {"planned", "running", "gated", "completed", "aborted"}:
        add_issue(issues, "error", "MANIFEST_STATUS", f"{path.relative_to(ROOT)}: invalid status")
    if not re.fullmatch(r"S[0-9]+", str(value.get("state_in", ""))):
        add_issue(issues, "error", "MANIFEST_STATE", f"{path.relative_to(ROOT)}: invalid state_in")
    require_frozen = status != "planned" and not template
    check_maybe_hashed_file(value.get("brief"), issues, "MANIFEST_BRIEF", require_hash=require_frozen, check_path=not template)
    if not isinstance(value.get("route_approval_reference"), str) or not value.get("route_approval_reference"):
        add_issue(issues, "error", "MANIFEST_APPROVAL", f"{path.relative_to(ROOT)}: route_approval_reference is required")
    elif route_id is not None and status in {"running", "gated", "completed"} and value.get("route_approval_reference") == "proposal-only":
        add_issue(issues, "error", "MANIFEST_ROUTE_GATE", f"{path.relative_to(ROOT)}: an activated route needs an owner approval reference")
    task_records = value.get("task_records", [])
    if not isinstance(task_records, list):
        add_issue(issues, "error", "MANIFEST_TASKS", f"{path.relative_to(ROOT)}: task_records must be an array")
    else:
        for record in task_records:
            check_maybe_hashed_file(record, issues, "MANIFEST_TASK", require_hash=True, check_path=not template)
    for field, code in (("director_summary", "MANIFEST_SUMMARY"), ("state_transition", "MANIFEST_TRANSITION")):
        record = value.get(field)
        if record is not None:
            check_maybe_hashed_file(record, issues, code, require_hash=True, check_path=not template)
    if status == "completed" and not template and value.get("director_summary") is None:
        add_issue(issues, "error", "MANIFEST_COMPLETION", f"{path.relative_to(ROOT)}: completed run lacks Director summary")
    if version == "1.1":
        check_path_reference(value.get("orchestration"), issues, "MANIFEST_ORCHESTRATION", check_path=not template)
        signal = value.get("route_signal")
        allowed_signals = {"not_assessed", "decisive_support", "partial_support", "null_result", "scoped_obstruction", "structural_failure", "not_applicable"}
        if signal not in allowed_signals:
            add_issue(issues, "error", "MANIFEST_ROUTE_SIGNAL", f"{path.relative_to(ROOT)}: invalid route_signal")
        if status == "completed" and not template and signal == "not_assessed":
            add_issue(issues, "error", "MANIFEST_ROUTE_UNASSESSED", f"{path.relative_to(ROOT)}: completed run needs a route evidence assessment")
        review = value.get("route_review")
        if review is not None:
            check_path_reference(review, issues, "MANIFEST_ROUTE_REVIEW", check_path=not template)


def validate_task_record(value: dict[str, Any], path: Path, issues: list[dict[str, str]], *, template: bool = False) -> None:
    validate_json_schema(value, SCHEMA_BY_KIND["task"], issues, "TASK_SCHEMA_RULE", str(path.relative_to(ROOT)))
    base_required = {"schema_version", "run_id", "route_id", "task_id", "status", "proof_items", "evidence_class", "derivation_roots", "independence_from", "dispatch", "artifact", "verdict"}
    lineage_required = {"strict_prerequisites", "non_strict_links", "blocking_reason"}
    version = value.get("schema_version")
    required = base_required | lineage_required if version == "1.1" or template else base_required
    for field in sorted(required - value.keys()):
        add_issue(issues, "error", "TASK_RECORD_FIELD", f"{path.relative_to(ROOT)}: missing {field}")
    if version == "1.0" and not template:
        add_issue(issues, "warning", "TASK_RECORD_LEGACY_SCHEMA", f"{path.relative_to(ROOT)}: v1.0 preserved; add strict/non-strict lineage when next reviewed")
    elif version != "1.1":
        add_issue(issues, "error", "TASK_RECORD_SCHEMA", f"{path.relative_to(ROOT)}: expected task schema 1.1")
    if not re.fullmatch(r"R[0-9]+", str(value.get("run_id", ""))):
        add_issue(issues, "error", "TASK_RECORD_RUN", f"{path.relative_to(ROOT)}: invalid run_id")
    if not re.fullmatch(r"T[0-9]+", str(value.get("task_id", ""))):
        add_issue(issues, "error", "TASK_RECORD_ID", f"{path.relative_to(ROOT)}: invalid task_id")
    if value.get("route_id") is not None and not re.fullmatch(r"route:[A-Za-z0-9][A-Za-z0-9._-]*", str(value.get("route_id"))):
        add_issue(issues, "error", "TASK_RECORD_ROUTE", f"{path.relative_to(ROOT)}: invalid route_id")
    if value.get("status") not in {"planned", "dispatched", "returned", "critic_pending", "resolved", "accepted", "rejected"}:
        add_issue(issues, "error", "TASK_RECORD_STATUS", f"{path.relative_to(ROOT)}: invalid status")
    if value.get("evidence_class") not in {"derivation", "source_audit", "critic", "resolution", "owner_resolution", "scoped_obstruction", "numerical", "lean_certificate", "state_proposal"}:
        add_issue(issues, "error", "TASK_RECORD_CLASS", f"{path.relative_to(ROOT)}: invalid evidence_class")
    if value.get("verdict") not in EVIDENCE_VERDICTS:
        add_issue(issues, "error", "TASK_RECORD_VERDICT", f"{path.relative_to(ROOT)}: invalid verdict")
    for field in ("proof_items", "strict_prerequisites", "non_strict_links", "derivation_roots", "independence_from"):
        if field in value and not isinstance(value.get(field), list):
            add_issue(issues, "error", "TASK_RECORD_LINEAGE", f"{path.relative_to(ROOT)}: {field} must be an array")
    require_frozen = value.get("status") != "planned" and not template
    check_maybe_hashed_file(value.get("dispatch"), issues, "TASK_DISPATCH", require_hash=require_frozen, check_path=not template)
    if value.get("artifact") is not None:
        check_maybe_hashed_file(value.get("artifact"), issues, "TASK_ARTIFACT", require_hash=True, check_path=not template)


def validate_state_transition(value: dict[str, Any], path: Path, issues: list[dict[str, str]]) -> None:
    validate_json_schema(value, SCHEMA_BY_KIND["transition"], issues, "TRANSITION_SCHEMA_RULE", str(path.relative_to(ROOT)))
    required = {"schema_version", "proposal_id", "run_id", "state_from", "state_to", "status", "owner_approval_reference", "evidence_records", "changes"}
    for field in sorted(required - value.keys()):
        add_issue(issues, "error", "TRANSITION_FIELD", f"{path.relative_to(ROOT)}: missing {field}")
    if value.get("schema_version") != "1.0" or not re.fullmatch(r"R[0-9]+", str(value.get("run_id", ""))):
        add_issue(issues, "error", "TRANSITION_RUN", f"{path.relative_to(ROOT)}: invalid run_id")
    if not re.fullmatch(r"ST-R[0-9]+-S[0-9]+-S[0-9]+", str(value.get("proposal_id", ""))):
        add_issue(issues, "error", "TRANSITION_ID", f"{path.relative_to(ROOT)}: invalid proposal_id")
    for field in ("state_from", "state_to"):
        if not re.fullmatch(r"S[0-9]+", str(value.get(field, ""))):
            add_issue(issues, "error", "TRANSITION_STATE", f"{path.relative_to(ROOT)}: invalid {field}")
    if value.get("status") not in {"proposal_only", "owner_approved", "applied"}:
        add_issue(issues, "error", "TRANSITION_STATUS", f"{path.relative_to(ROOT)}: invalid status")
    if value.get("status") in {"owner_approved", "applied"} and not value.get("owner_approval_reference"):
        add_issue(issues, "error", "TRANSITION_APPROVAL", f"{path.relative_to(ROOT)}: approved transition lacks owner reference")
    changes = value.get("changes")
    change_fields = {"claims", "routes", "runs", "notation", "assumptions", "manuscript"}
    if not isinstance(changes, dict) or not change_fields.issubset(changes):
        add_issue(issues, "error", "TRANSITION_CHANGES", f"{path.relative_to(ROOT)}: incomplete changes object")


def validate_hydration_proposal(value: dict[str, Any], path: Path, issues: list[dict[str, str]]) -> None:
    validate_json_schema(value, SCHEMA_BY_KIND["hydration"], issues, "HYDRATION_SCHEMA_RULE", str(path.relative_to(ROOT)))
    required = {"schema_version", "status", "run_id", "source_directory", "source_artifacts", "detected_task_ids", "proposed_sidecars", "unresolved_mappings"}
    for field in sorted(required - value.keys()):
        add_issue(issues, "error", "HYDRATION_FIELD", f"{path.relative_to(ROOT)}: missing {field}")
    if value.get("schema_version") not in {"1.0", "1.1"} or value.get("status") != "proposal_only":
        add_issue(issues, "error", "HYDRATION_AUTHORITY", f"{path.relative_to(ROOT)}: hydration must remain proposal_only")
    if value.get("schema_version") == "1.0":
        add_issue(issues, "warning", "HYDRATION_LEGACY_SCHEMA", f"{path.relative_to(ROOT)}: legacy proposal does not include orchestration or route review")
    if not re.fullmatch(r"R[0-9]+", str(value.get("run_id", ""))):
        add_issue(issues, "error", "HYDRATION_RUN", f"{path.relative_to(ROOT)}: invalid run_id")
    artifacts = value.get("source_artifacts", [])
    if not isinstance(artifacts, list):
        add_issue(issues, "error", "HYDRATION_ARTIFACTS", f"{path.relative_to(ROOT)}: source_artifacts must be an array")
    else:
        for record in artifacts:
            if isinstance(record, dict):
                check_hashed_file(record, issues, "HYDRATION_SOURCE")
            else:
                add_issue(issues, "error", "HYDRATION_ARTIFACT", f"{path.relative_to(ROOT)}: invalid artifact record")
    if not isinstance(value.get("unresolved_mappings"), list) or not value.get("unresolved_mappings"):
        add_issue(issues, "error", "HYDRATION_UNRESOLVED", f"{path.relative_to(ROOT)}: unresolved mappings must remain explicit")
    proposed = value.get("proposed_sidecars")
    expected = {"manifest", "task_records", "state_transition"}
    if value.get("schema_version") == "1.1":
        expected |= {"orchestration", "route_review"}
    if not isinstance(proposed, dict) or not expected.issubset(proposed):
        add_issue(issues, "error", "HYDRATION_SIDECARS", f"{path.relative_to(ROOT)}: proposed sidecar inventory is incomplete")


def validate_workspace_roles(
    value: dict[str, Any], path: Path, issues: list[dict[str, str]], *, template: bool = False
) -> None:
    validate_json_schema(value, SCHEMA_BY_KIND["roles"], issues, "WORKSPACE_ROLE_SCHEMA_RULE", str(path.relative_to(ROOT)))
    required = {
        "schema_version", "topology", "project_id", "project_path",
        "shared_project_directory", "bootstrap_task_id", "roles",
    }
    for field in sorted(required - value.keys()):
        add_issue(issues, "error", "WORKSPACE_ROLE_FIELD", f"{path.relative_to(ROOT)}: missing {field}")
    if value.get("schema_version") != "1.1" or value.get("topology") != "peer_tasks":
        add_issue(issues, "error", "WORKSPACE_ROLE_TOPOLOGY", f"{path.relative_to(ROOT)}: expected peer_tasks schema 1.1")
    if value.get("shared_project_directory") is not True:
        add_issue(issues, "error", "WORKSPACE_ROLE_SHARING", f"{path.relative_to(ROOT)}: roles must share the saved project directory")
    roles = value.get("roles")
    if not isinstance(roles, list) or len(roles) != 3:
        add_issue(issues, "error", "WORKSPACE_ROLE_COUNT", f"{path.relative_to(ROOT)}: expected exactly three peer roles")
        return
    expected = {"director", "researcher", "critic"}
    names = [record.get("role") for record in roles if isinstance(record, dict)]
    if len(names) != 3 or set(names) != expected:
        add_issue(issues, "error", "WORKSPACE_ROLE_SET", f"{path.relative_to(ROOT)}: expected one Director, Researcher, and Critic")
    bound_ids: list[str] = []
    expected_titles = {"director": "0 Director", "researcher": "1 Researcher", "critic": "2 Critic"}
    for record in roles:
        if not isinstance(record, dict):
            add_issue(issues, "error", "WORKSPACE_ROLE_RECORD", f"{path.relative_to(ROOT)}: role entry is not an object")
            continue
        status, thread_id = record.get("status"), record.get("thread_id")
        role = record.get("role")
        if record.get("title") != expected_titles.get(role):
            add_issue(issues, "error", "WORKSPACE_ROLE_TITLE", f"{path.relative_to(ROOT)}: {role} must be titled {expected_titles.get(role)!r}")
        if record.get("is_current_task") is not (role == "director"):
            add_issue(issues, "error", "WORKSPACE_ROLE_CURRENT", f"{path.relative_to(ROOT)}: the current task must be 0 Director only")
        if record.get("task_scope") != "top_level":
            add_issue(issues, "error", "WORKSPACE_ROLE_SCOPE", f"{path.relative_to(ROOT)}: {record.get('role')} is not a top-level task")
        if record.get("workspace_mode") != "saved_project_local":
            add_issue(issues, "error", "WORKSPACE_ROLE_MODE", f"{path.relative_to(ROOT)}: {record.get('role')} does not use the shared saved project")
        if status not in {"unbound", "starting", "ready", "attention", "closed"}:
            add_issue(issues, "error", "WORKSPACE_ROLE_STATUS", f"{path.relative_to(ROOT)}: invalid status for {record.get('role')}")
        if status == "unbound" and thread_id is not None:
            add_issue(issues, "error", "WORKSPACE_ROLE_UNBOUND", f"{path.relative_to(ROOT)}: unbound {record.get('role')} has a task ID")
        if status in {"starting", "ready", "attention"}:
            if not isinstance(thread_id, str) or not thread_id:
                add_issue(issues, "error", "WORKSPACE_ROLE_TASK", f"{path.relative_to(ROOT)}: {record.get('role')} is {status} without a task ID")
            else:
                bound_ids.append(thread_id)
    if len(bound_ids) != len(set(bound_ids)):
        add_issue(issues, "error", "WORKSPACE_ROLE_DISTINCT", f"{path.relative_to(ROOT)}: persistent roles must use distinct top-level task IDs")
    if not template and all(record.get("status") == "unbound" for record in roles if isinstance(record, dict)):
        add_issue(issues, "warning", "WORKSPACE_ROLES_UNBOUND", f"{path.relative_to(ROOT)}: role tasks have not been bootstrapped")


def validate_orchestration(
    value: dict[str, Any], path: Path, issues: list[dict[str, str]]
) -> None:
    validate_json_schema(value, SCHEMA_BY_KIND["orchestration"], issues, "ORCHESTRATION_SCHEMA_RULE", str(path.relative_to(ROOT)))
    required = {
        "schema_version", "run_id", "route_id", "director_state",
        "active_task_id", "awaiting_role", "last_completed_task_id",
        "next_action", "owner_gate", "processed_return_keys", "updated_at",
    }
    for field in sorted(required - value.keys()):
        add_issue(issues, "error", "ORCHESTRATION_FIELD", f"{path.relative_to(ROOT)}: missing {field}")
    if value.get("schema_version") != "1.0" or not re.fullmatch(r"R[0-9]+", str(value.get("run_id", ""))):
        add_issue(issues, "error", "ORCHESTRATION_ID", f"{path.relative_to(ROOT)}: invalid schema_version or run_id")
    state = value.get("director_state")
    states = {"idle", "dispatching", "waiting_researcher", "director_review_researcher", "waiting_critic", "director_review_critic", "adjudicating", "advancing", "owner_gate", "run_closure", "closed"}
    if state not in states:
        add_issue(issues, "error", "ORCHESTRATION_STATE", f"{path.relative_to(ROOT)}: invalid director_state")
    awaiting = value.get("awaiting_role")
    active_task = value.get("active_task_id")
    expected_role = {"waiting_researcher": "researcher", "waiting_critic": "critic"}.get(state)
    if expected_role and awaiting != expected_role:
        add_issue(issues, "error", "ORCHESTRATION_WAIT_ROLE", f"{path.relative_to(ROOT)}: {state} must await {expected_role}")
    if expected_role and not re.fullmatch(r"T[0-9]+", str(active_task or "")):
        add_issue(issues, "error", "ORCHESTRATION_WAIT_TASK", f"{path.relative_to(ROOT)}: waiting state needs an active task ID")
    gate = value.get("owner_gate")
    if not isinstance(gate, dict):
        add_issue(issues, "error", "ORCHESTRATION_GATE", f"{path.relative_to(ROOT)}: owner_gate must be an object")
    else:
        gate_required = gate.get("required") is True
        if state == "owner_gate" and (not gate_required or not gate.get("reason")):
            add_issue(issues, "error", "ORCHESTRATION_GATE_REASON", f"{path.relative_to(ROOT)}: owner_gate state needs a named reason")
        if state not in {"owner_gate", "idle"} and gate_required and not gate.get("approval_reference"):
            add_issue(issues, "error", "ORCHESTRATION_GATE_BYPASS", f"{path.relative_to(ROOT)}: work is advancing while an unresolved owner gate remains")
    keys = value.get("processed_return_keys")
    if not isinstance(keys, list) or len(keys) != len(set(keys)):
        add_issue(issues, "error", "ORCHESTRATION_RETURN_KEYS", f"{path.relative_to(ROOT)}: processed return keys must be a unique list")


def validate_route_review(
    value: dict[str, Any], path: Path, issues: list[dict[str, str]], *, template: bool = False
) -> None:
    validate_json_schema(value, SCHEMA_BY_KIND["route_review"], issues, "ROUTE_REVIEW_SCHEMA_RULE", str(path.relative_to(ROOT)))
    required = {"schema_version", "review_id", "route_id", "status", "trigger", "reviewed_runs", "evidence", "recommendation", "recommendation_scope", "owner_decision", "owner_approval_reference", "decision_artifact"}
    if value.get("schema_version") == "1.1" or template:
        required.add("literature_refresh")
    for field in sorted(required - value.keys()):
        add_issue(issues, "error", "ROUTE_REVIEW_FIELD", f"{path.relative_to(ROOT)}: missing {field}")
    if value.get("schema_version") == "1.0" and not template:
        add_issue(issues, "warning", "ROUTE_REVIEW_LEGACY_SCHEMA", f"{path.relative_to(ROOT)}: legacy review predates the mandatory literature refresh")
    elif value.get("schema_version") != "1.1":
        add_issue(issues, "error", "ROUTE_REVIEW_SCHEMA", f"{path.relative_to(ROOT)}: expected route-review schema 1.1")
    if not re.fullmatch(r"RR-[A-Za-z0-9._-]+-[0-9]+", str(value.get("review_id", ""))):
        add_issue(issues, "error", "ROUTE_REVIEW_ID", f"{path.relative_to(ROOT)}: invalid schema_version or review_id")
    route_id = value.get("route_id")
    if not isinstance(route_id, str) or not re.fullmatch(r"route:[A-Za-z0-9][A-Za-z0-9._-]*", route_id):
        add_issue(issues, "error", "ROUTE_REVIEW_ROUTE", f"{path.relative_to(ROOT)}: invalid route_id")
    status = value.get("status")
    if status not in {"due", "in_review", "owner_gate", "closed"}:
        add_issue(issues, "error", "ROUTE_REVIEW_STATUS", f"{path.relative_to(ROOT)}: invalid status")
    trigger = value.get("trigger")
    trigger_fields = {"three_runs_without_decisive_support", "repeated_obstruction_or_roots", "structural_failure", "owner_requested"}
    if not isinstance(trigger, dict) or not trigger_fields.issubset(trigger):
        add_issue(issues, "error", "ROUTE_REVIEW_TRIGGER", f"{path.relative_to(ROOT)}: incomplete trigger record")
    elif not template and not any(trigger.get(field) is True for field in trigger_fields):
        add_issue(issues, "error", "ROUTE_REVIEW_TRIGGER_EMPTY", f"{path.relative_to(ROOT)}: a route review needs at least one trigger")
    reviewed_runs = value.get("reviewed_runs")
    if not isinstance(reviewed_runs, list) or not reviewed_runs or any(not re.fullmatch(r"R[0-9]+", str(run_id)) for run_id in reviewed_runs):
        add_issue(issues, "error", "ROUTE_REVIEW_RUNS", f"{path.relative_to(ROOT)}: reviewed_runs must contain run IDs")
    if status in {"owner_gate", "closed"} and value.get("recommendation") is None:
        add_issue(issues, "error", "ROUTE_REVIEW_RECOMMENDATION", f"{path.relative_to(ROOT)}: review at an owner gate needs a scoped recommendation")
    literature = value.get("literature_refresh")
    if value.get("schema_version") == "1.1" and not isinstance(literature, dict):
        add_issue(issues, "error", "ROUTE_REVIEW_LITERATURE", f"{path.relative_to(ROOT)}: systematic literature refresh is required")
    elif value.get("schema_version") == "1.1" and status in {"owner_gate", "closed"} and literature.get("status") != "completed":
        add_issue(issues, "error", "ROUTE_REVIEW_LITERATURE_OPEN", f"{path.relative_to(ROOT)}: literature refresh must finish before a route recommendation reaches the owner")
    if status == "closed":
        if value.get("owner_decision") == "pending" or not value.get("owner_approval_reference"):
            add_issue(issues, "error", "ROUTE_REVIEW_APPROVAL", f"{path.relative_to(ROOT)}: closed review needs an explicit owner decision")
        decision_artifact = value.get("decision_artifact")
        if decision_artifact is None:
            add_issue(issues, "error", "ROUTE_REVIEW_DECISION", f"{path.relative_to(ROOT)}: closed review needs a hashed decision artifact")
        else:
            check_maybe_hashed_file(decision_artifact, issues, "ROUTE_REVIEW_DECISION", require_hash=True, check_path=not template)


def validate_run_sidecars(issues: list[dict[str, str]]) -> None:
    validate_sidecar_schemas(issues)
    try:
        workspace_template = load_json(WORKSPACE_ROLES_TEMPLATE_PATH)
    except SystemExit as exc:
        add_issue(issues, "error", "WORKSPACE_ROLE_TEMPLATE", str(exc))
    else:
        validate_workspace_roles(workspace_template, WORKSPACE_ROLES_TEMPLATE_PATH, issues, template=True)
    if WORKSPACE_ROLES_PATH.is_file():
        try:
            workspace_roles = load_json(WORKSPACE_ROLES_PATH)
        except SystemExit as exc:
            add_issue(issues, "error", "WORKSPACE_ROLE_JSON", str(exc))
        else:
            validate_workspace_roles(workspace_roles, WORKSPACE_ROLES_PATH, issues)
    else:
        add_issue(issues, "warning", "WORKSPACE_ROLES_MISSING", "research/machine/workspace-roles.json is absent; the three peer role tasks have not been registered")
    templates = ((RUNS_PATH / "_template" / "manifest.json", validate_run_manifest),
                 (RUNS_PATH / "_template" / "Txxx.json", validate_task_record),
                 (RUNS_PATH / "_template" / "state-transition.json", validate_state_transition),
                 (RUNS_PATH / "_template" / "orchestration.json", validate_orchestration),
                 (RUNS_PATH / "_template" / "route-review.json", validate_route_review))
    for path, validator in templates:
        try:
            value = load_json(path)
        except SystemExit as exc:
            add_issue(issues, "error", "SIDECAR_TEMPLATE", str(exc))
            continue
        if validator in {validate_run_manifest, validate_task_record, validate_route_review}:
            validator(value, path, issues, template=True)
        else:
            validator(value, path, issues)
    if not RUNS_PATH.is_dir():
        return
    route_history: dict[str, list[tuple[int, str, str]]] = {}
    route_all_runs: dict[str, list[tuple[int, str, str]]] = {}
    route_reviews: dict[str, list[dict[str, Any]]] = {}
    seen_review_paths: set[Path] = set()
    for directory in sorted(path for path in RUNS_PATH.iterdir() if path.is_dir() and path.name != "_template"):
        match = re.search(r"(R[0-9]+)$", directory.name)
        hydration = directory / "run-hydration.proposal.json"
        if hydration.is_file():
            try:
                hydration_value = load_json(hydration)
            except SystemExit as exc:
                add_issue(issues, "error", "HYDRATION_JSON", str(exc))
            else:
                validate_hydration_proposal(hydration_value, hydration, issues)
                if match and hydration_value.get("run_id") != match.group(1):
                    add_issue(issues, "error", "HYDRATION_LINK", f"{hydration.relative_to(ROOT)}: run_id disagrees with directory")
        manifest = directory / "manifest.json"
        if not manifest.is_file():
            add_issue(issues, "warning", "LEGACY_RUN_NO_MANIFEST", f"{directory.relative_to(ROOT)}: no manifest.json; add it when this run is next touched")
            continue
        try:
            value = load_json(manifest)
        except SystemExit as exc:
            add_issue(issues, "error", "MANIFEST_JSON", str(exc))
            continue
        validate_run_manifest(value, manifest, issues)
        if match and value.get("run_id") != match.group(1):
            add_issue(issues, "error", "MANIFEST_DIRECTORY_ID", f"{manifest.relative_to(ROOT)}: run_id disagrees with directory")
        run_id, route_id = value.get("run_id"), value.get("route_id")
        if isinstance(route_id, str) and re.fullmatch(r"R[0-9]+", str(run_id or "")):
            route_all_runs.setdefault(route_id, []).append((int(str(run_id)[1:]), str(run_id), str(value.get("status", ""))))
        if value.get("schema_version") == "1.1":
            orchestration_record = value.get("orchestration")
            orchestration_path = check_path_reference(orchestration_record, issues, "ORCHESTRATION", check_path=True) if orchestration_record is not None else None
            if orchestration_path and orchestration_path.is_file():
                try:
                    orchestration = load_json(orchestration_path)
                except SystemExit as exc:
                    add_issue(issues, "error", "ORCHESTRATION_JSON", str(exc))
                else:
                    validate_orchestration(orchestration, orchestration_path, issues)
                    if orchestration.get("run_id") != run_id or orchestration.get("route_id") != route_id:
                        add_issue(issues, "error", "ORCHESTRATION_LINK", f"{orchestration_path.relative_to(ROOT)}: run_id or route_id disagrees with manifest")
                    if value.get("status") == "completed" and orchestration.get("director_state") != "closed":
                        add_issue(issues, "error", "ORCHESTRATION_COMPLETION", f"{orchestration_path.relative_to(ROOT)}: completed manifest requires closed Director state")
                    if value.get("status") == "gated" and orchestration.get("director_state") != "owner_gate":
                        add_issue(issues, "error", "ORCHESTRATION_GATE_LINK", f"{orchestration_path.relative_to(ROOT)}: gated manifest requires owner_gate Director state")
            review_record = value.get("route_review")
            review_path = check_path_reference(review_record, issues, "ROUTE_REVIEW", check_path=True) if review_record is not None else None
            if review_path and review_path.is_file() and review_path not in seen_review_paths:
                seen_review_paths.add(review_path)
                try:
                    review = load_json(review_path)
                except SystemExit as exc:
                    add_issue(issues, "error", "ROUTE_REVIEW_JSON", str(exc))
                else:
                    validate_route_review(review, review_path, issues)
                    if review.get("route_id") != route_id:
                        add_issue(issues, "error", "ROUTE_REVIEW_LINK", f"{review_path.relative_to(ROOT)}: route_id disagrees with manifest")
                    if isinstance(route_id, str):
                        route_reviews.setdefault(route_id, []).append(review)
        if value.get("status") == "completed" and isinstance(route_id, str) and re.fullmatch(r"R[0-9]+", str(run_id or "")):
            route_history.setdefault(route_id, []).append((int(str(run_id)[1:]), str(run_id), str(value.get("route_signal", "not_assessed"))))
        for task_path in sorted(directory.glob("T[0-9]*.json")):
            try:
                task = load_json(task_path)
            except SystemExit as exc:
                add_issue(issues, "error", "TASK_RECORD_JSON", str(exc))
                continue
            validate_task_record(task, task_path, issues)
            if task.get("run_id") != value.get("run_id") or task.get("task_id") != task_path.stem:
                add_issue(issues, "error", "TASK_RECORD_LINK", f"{task_path.relative_to(ROOT)}: identifiers disagree with manifest or filename")
        transition = directory / "state-transition.json"
        if transition.is_file():
            try:
                transition_value = load_json(transition)
            except SystemExit as exc:
                add_issue(issues, "error", "TRANSITION_JSON", str(exc))
            else:
                validate_state_transition(transition_value, transition, issues)
                if transition_value.get("run_id") != value.get("run_id"):
                    add_issue(issues, "error", "TRANSITION_LINK", f"{transition.relative_to(ROOT)}: run_id disagrees with manifest")

    for route_id, entries in route_history.items():
        entries.sort()
        reviews = route_reviews.get(route_id, [])
        closed_reviewed = {
            run_id
            for review in reviews if review.get("status") == "closed"
            for run_id in review.get("reviewed_runs", []) if isinstance(run_id, str)
        }
        cutoff = max((int(run_id[1:]) for run_id in closed_reviewed if re.fullmatch(r"R[0-9]+", run_id)), default=-1)
        consecutive: list[str] = []
        trigger_runs: list[str] = []
        due_at = -1
        for number, run_id, signal in entries:
            if number <= cutoff:
                continue
            if due_at >= 0:
                continue
            if signal == "decisive_support":
                consecutive = []
            elif signal in {"partial_support", "null_result", "scoped_obstruction"}:
                consecutive.append(run_id)
            elif signal == "structural_failure":
                trigger_runs = [run_id]
                due_at = number
            if due_at < 0 and len(consecutive) >= 3:
                trigger_runs = consecutive[-3:]
                due_at = number
        covered = any(set(trigger_runs).issubset(set(review.get("reviewed_runs", []))) for review in reviews) if trigger_runs else False
        if trigger_runs and not covered:
            add_issue(issues, "warning", "ROUTE_REVIEW_DUE", f"{route_id}: review required after {', '.join(trigger_runs)} before another construction run")
        if due_at >= 0 and not covered and any(number > due_at and status in {"running", "gated", "completed"} for number, _, status in route_all_runs.get(route_id, [])):
            add_issue(issues, "error", "ROUTE_REVIEW_BYPASSED", f"{route_id}: a later construction run bypassed the mandatory review triggered at R{due_at:03d}")
        for review in reviews:
            status = review.get("status")
            reviewed_numbers = [int(run_id[1:]) for run_id in review.get("reviewed_runs", []) if isinstance(run_id, str) and re.fullmatch(r"R[0-9]+", run_id)]
            if status != "closed":
                add_issue(issues, "warning", "ROUTE_REVIEW_OPEN", f"{route_id}: route review is {status}; owner-approved continuation is not recorded")
                if reviewed_numbers and any(number > max(reviewed_numbers) and run_status in {"running", "gated", "completed"} for number, _, run_status in route_all_runs.get(route_id, [])):
                    add_issue(issues, "error", "ROUTE_REVIEW_BYPASSED", f"{route_id}: a later completed run bypassed an open route review")


def find_dependency_cycle(claims: dict[str, dict[str, Any]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(claim_id: str) -> list[str] | None:
        if claim_id in visiting:
            start = stack.index(claim_id)
            return stack[start:] + [claim_id]
        if claim_id in visited:
            return None
        visiting.add(claim_id)
        stack.append(claim_id)
        for dependency in claims[claim_id].get("depends_on", []):
            if dependency in claims:
                cycle = visit(dependency)
                if cycle:
                    return cycle
        stack.pop()
        visiting.remove(claim_id)
        visited.add(claim_id)
        return None

    for claim_id in claims:
        cycle = visit(claim_id)
        if cycle:
            return cycle
    return None


def validate_state(state: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    if not SCHEMA_PATH.is_file():
        add_issue(issues, "error", "SCHEMA_MISSING", "missing schema file")
    else:
        validate_json_schema(state, SCHEMA_PATH, issues, "STATE_SCHEMA_RULE", "project-state")
    if state.get("schema_version") != "2.1":
        add_issue(issues, "error", "SCHEMA_VERSION", "expected schema_version 2.1")

    required = {"snapshot", "canonical_files", "claims", "routes", "runs", "edges"}
    for field in sorted(required - state.keys()):
        add_issue(issues, "error", "FIELD_MISSING", f"missing top-level field {field}")
    if not isinstance(state.get("snapshot", {}).get("project_name"), str) or not state.get("snapshot", {}).get("project_name"):
        add_issue(issues, "error", "PROJECT_NAME", "snapshot.project_name is required")

    for record in state.get("canonical_files", []):
        if isinstance(record, dict):
            check_hashed_file(record, issues, "CANONICAL")
        else:
            add_issue(issues, "error", "CANONICAL_RECORD", "canonical file record is not an object")

    claim_list = state.get("claims", [])
    route_list = state.get("routes", [])
    run_list = state.get("runs", [])
    if not isinstance(claim_list, list):
        add_issue(issues, "error", "CLAIMS_TYPE", "claims must be an array")
        claim_list = []
    if not isinstance(route_list, list):
        add_issue(issues, "error", "ROUTES_TYPE", "routes must be an array")
        route_list = []
    if not isinstance(run_list, list):
        add_issue(issues, "error", "RUNS_TYPE", "runs must be an array")
        run_list = []

    claims: dict[str, dict[str, Any]] = {}
    for claim in claim_list:
        if not isinstance(claim, dict):
            add_issue(issues, "error", "CLAIM_RECORD", "claim record is not an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.startswith("P"):
            add_issue(issues, "error", "CLAIM_ID", f"invalid claim id {claim_id!r}")
            continue
        if claim_id in claims:
            add_issue(issues, "error", "CLAIM_DUPLICATE", f"duplicate claim {claim_id}")
            continue
        claims[claim_id] = claim
        if claim.get("status") not in CLAIM_STATUSES:
            add_issue(
                issues,
                "error",
                "CLAIM_STATUS",
                f"{claim_id}: invalid status {claim.get('status')!r}",
            )
        if not isinstance(claim.get("blocking"), bool):
            add_issue(issues, "error", "CLAIM_BLOCKING", f"{claim_id}: blocking must be boolean")
        dependencies = claim.get("depends_on", [])
        if not isinstance(dependencies, list):
            add_issue(issues, "error", "CLAIM_DEPENDENCIES", f"{claim_id}: depends_on must be an array")
            continue
        if len(dependencies) != len(set(dependencies)):
            add_issue(issues, "error", "CLAIM_DEPENDENCY_DUPLICATE", f"{claim_id}: duplicate dependency")

    for claim_id, claim in claims.items():
        for dependency in claim.get("depends_on", []):
            if dependency not in claims:
                add_issue(
                    issues,
                    "error",
                    "CLAIM_DEPENDENCY_MISSING",
                    f"{claim_id}: unknown dependency {dependency}",
                )
        for evidence in claim.get("evidence", []):
            if isinstance(evidence, dict):
                check_hashed_file(evidence, issues, "EVIDENCE")

    cycle = find_dependency_cycle(claims)
    if cycle:
        add_issue(
            issues,
            "error",
            "CLAIM_DEPENDENCY_CYCLE",
            " -> ".join(cycle),
        )

    routes: dict[str, dict[str, Any]] = {}
    evidence_ids: set[str] = set()
    for route in route_list:
        if not isinstance(route, dict):
            add_issue(issues, "error", "ROUTE_RECORD", "route record is not an object")
            continue
        route_id = route.get("id")
        if not isinstance(route_id, str) or not re.fullmatch(r"route:[A-Za-z0-9][A-Za-z0-9._-]*", route_id):
            add_issue(issues, "error", "ROUTE_ID", f"invalid route id {route_id!r}")
            continue
        if route_id in routes:
            add_issue(issues, "error", "ROUTE_DUPLICATE", f"duplicate route {route_id}")
            continue
        routes[route_id] = route
        if route.get("canonical_status") not in CANONICAL_ROUTE_STATUSES:
            add_issue(issues, "error", "ROUTE_CANONICAL_STATUS", f"{route_id}: invalid canonical status")
        if route.get("operational_status") not in OPERATIONAL_ROUTE_STATUSES:
            add_issue(issues, "error", "ROUTE_OPERATIONAL_STATUS", f"{route_id}: invalid operational status")
        for claim_id in route.get("target_claims", []):
            if claim_id not in claims:
                add_issue(issues, "error", "ROUTE_TARGET_MISSING", f"{route_id}: unknown target {claim_id}")
        evidence_records = route.get("evidence", [])
        if route.get("operational_status") == "rejected":
            if not route.get("scope"):
                add_issue(issues, "error", "ROUTE_SCOPE", f"{route_id}: rejected route needs an exact scope")
            if not any(item.get("verdict") == "rejects_route" for item in evidence_records if isinstance(item, dict)):
                add_issue(issues, "error", "ROUTE_REJECTION_EVIDENCE", f"{route_id}: missing rejects_route evidence")
        for evidence in evidence_records:
            if not isinstance(evidence, dict):
                add_issue(issues, "error", "EVIDENCE_RECORD", f"{route_id}: evidence is not an object")
                continue
            evidence_id = evidence.get("id")
            if not isinstance(evidence_id, str):
                add_issue(issues, "error", "EVIDENCE_ID", f"{route_id}: invalid evidence id")
            elif evidence_id in evidence_ids:
                add_issue(issues, "error", "EVIDENCE_DUPLICATE", f"duplicate evidence {evidence_id}")
            else:
                evidence_ids.add(evidence_id)
            if evidence.get("verdict") not in EVIDENCE_VERDICTS:
                add_issue(issues, "error", "EVIDENCE_VERDICT", f"{evidence_id}: invalid verdict")
            check_hashed_file(evidence, issues, "EVIDENCE")
            if evidence.get("verdict") == "rejects_route" and not evidence.get("scope"):
                add_issue(issues, "error", "EVIDENCE_SCOPE", f"{evidence_id}: rejection needs exact scope")

        canonical_status = route.get("canonical_status")
        operational_status = route.get("operational_status")
        if canonical_status == "active" and operational_status in {"completed", "rejected"}:
            add_issue(
                issues,
                "warning",
                "PENDING_CANONICAL_SYNC",
                f"{route_id}: operational result is {operational_status}, canonical route remains active",
            )

    runs: dict[str, dict[str, Any]] = {}
    for run in run_list:
        if not isinstance(run, dict):
            add_issue(issues, "error", "RUN_RECORD", "run record is not an object")
            continue
        run_id = run.get("id")
        if not isinstance(run_id, str) or not re.fullmatch(r"R[0-9]+", run_id):
            add_issue(issues, "error", "RUN_ID", f"invalid run id {run_id!r}")
            continue
        if run_id in runs:
            add_issue(issues, "error", "RUN_DUPLICATE", f"duplicate run {run_id}")
            continue
        runs[run_id] = run
        if run.get("status") not in RUN_STATUSES:
            add_issue(issues, "error", "RUN_STATUS", f"{run_id}: invalid status {run.get('status')!r}")
        route_id = run.get("route_id")
        if route_id is not None and route_id not in routes:
            add_issue(issues, "error", "RUN_ROUTE_MISSING", f"{run_id}: unknown route {route_id}")
        if "manifest" in run:
            check_hashed_file(run["manifest"], issues, "RUN_MANIFEST")

    snapshot = state.get("snapshot", {})
    theorem_targets = snapshot.get("theorem_targets")
    if not isinstance(theorem_targets, list):
        add_issue(issues, "error", "THEOREM_TARGETS", "snapshot.theorem_targets must be an array")
        theorem_targets = []
    for target_claim in theorem_targets:
        if target_claim not in claims:
            add_issue(issues, "error", "THEOREM_TARGET_MISSING", f"unknown theorem target {target_claim}")
    if theorem_targets and all(target_claim in claims for target_claim in theorem_targets):
        strict_prerequisites: set[str] = set()
        for target_claim in theorem_targets:
            strict_prerequisites.update(dependency_closure(claims, target_claim))
        expected_blockers = {claim_id for claim_id in strict_prerequisites if claims[claim_id].get("status") not in RESOLVED_CLAIM_STATUSES}
        actual_blockers = {claim_id for claim_id, claim in claims.items() if claim.get("blocking") is True}
        if expected_blockers != actual_blockers:
            add_issue(
                issues,
                "error",
                "BLOCKING_DERIVATION",
                f"blocking flags differ from unresolved strict prerequisites; expected {sorted(expected_blockers)}, recorded {sorted(actual_blockers)}",
            )
    elif claims:
        add_issue(issues, "warning", "THEOREM_TARGET_UNMAPPED", "blocking flags cannot be derived until snapshot.theorem_targets is human-mapped")
    active_route = snapshot.get("active_route")
    active_run = snapshot.get("active_run")
    if active_route is not None and active_route not in routes:
        add_issue(issues, "error", "ACTIVE_ROUTE_MISSING", f"snapshot references unknown route {active_route}")
    if active_run is not None and active_run not in runs:
        add_issue(issues, "error", "ACTIVE_RUN_MISSING", f"snapshot references unknown run {active_run}")
    if active_route is not None and active_run is not None and runs.get(active_run, {}).get("route_id") not in {None, active_route}:
        add_issue(issues, "error", "ACTIVE_ROUTE_RUN_MISMATCH", f"{active_run} belongs to {runs[active_run].get('route_id')}, not {active_route}")

    nodes = set(claims) | set(routes) | set(runs)
    for edge in state.get("edges", []):
        if not isinstance(edge, dict):
            add_issue(issues, "error", "EDGE_RECORD", "edge is not an object")
            continue
        source = edge.get("from")
        target = edge.get("to")
        if edge.get("type") == "depends_on":
            add_issue(issues, "error", "EDGE_DEPENDENCY_DUPLICATE", "strict dependencies belong only in claim.depends_on")
        if source not in nodes:
            add_issue(issues, "error", "EDGE_SOURCE_MISSING", f"unknown edge source {source}")
        if target not in claims:
            add_issue(issues, "error", "EDGE_TARGET_MISSING", f"unknown edge target {target}")

    validate_run_sidecars(issues)
    report_paths = (REPORT_MD_PATH, REPORT_TEX_PATH, REPORT_PDF_PATH)
    if not all(path.is_file() for path in report_paths):
        add_issue(issues, "warning", "READABLE_REPORT_MISSING", "the consolidated Markdown, LaTeX, and PDF research summary has not yet been generated")
    else:
        newest_source = max((ROOT / relative).stat().st_mtime for relative in CORE_RESEARCH_FILES if (ROOT / relative).is_file())
        if any(path.stat().st_mtime < newest_source for path in report_paths):
            add_issue(issues, "warning", "READABLE_REPORT_STALE", "the readable research summary predates a core mathematical file")
    return issues


def issue_counts(issues: list[dict[str, str]]) -> Counter[str]:
    return Counter(issue["severity"] for issue in issues)


def print_validation(issues: list[dict[str, str]]) -> int:
    counts = issue_counts(issues)
    for issue in issues:
        print(f"[{issue['severity'].upper()}] {issue['code']}: {issue['message']}")
    print(
        f"validation: {counts['error']} error(s), "
        f"{counts['warning']} warning(s)"
    )
    return 1 if counts["error"] else 0


def claim_index(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in state["claims"]}


def command_status(state: dict[str, Any], claim_id: str) -> int:
    claims = claim_index(state)
    claim = claims.get(claim_id)
    if claim is None:
        print(f"unknown claim: {claim_id}", file=sys.stderr)
        return 2
    print(f"{claim_id} — {claim['title']}")
    print(f"status: {claim['status']}; blocking: {'yes' if claim['blocking'] else 'no'}")
    print(f"depends on: {', '.join(claim['depends_on']) or 'none'}")
    print(f"note: {claim['note']}")
    routes = [route["id"] for route in state["routes"] if claim_id in route["target_claims"]]
    print(f"tested by: {', '.join(routes) or 'none'}")
    return 0


def dependency_closure(claims: dict[str, dict[str, Any]], root: str) -> set[str]:
    seen: set[str] = set()

    def walk(claim_id: str) -> None:
        for dependency in claims[claim_id].get("depends_on", []):
            if dependency not in seen:
                seen.add(dependency)
                walk(dependency)

    walk(root)
    return seen


def command_blockers(state: dict[str, Any], claim_id: str) -> int:
    claims = claim_index(state)
    if claim_id not in claims:
        print(f"unknown claim: {claim_id}", file=sys.stderr)
        return 2
    unresolved = [
        claims[item]
        for item in dependency_closure(claims, claim_id)
        if claims[item]["blocking"]
        and claims[item]["status"] not in RESOLVED_CLAIM_STATUSES
    ]
    unresolved.sort(key=lambda item: int(item["id"][1:]))
    print(f"Blocking dependency closure for {claim_id} — {claims[claim_id]['title']}")
    if not unresolved:
        print("none recorded")
        return 0
    for claim in unresolved:
        print(f"- {claim['id']} [{claim['status']}]: {claim['title']} — {claim['note']}")
    return 0


def command_summary(state: dict[str, Any], issues: list[dict[str, str]]) -> int:
    statuses = Counter(claim["status"] for claim in state["claims"])
    snapshot = state["snapshot"]
    print(
        f"state {snapshot['state_version']} | active route {snapshot.get('active_route') or 'none'} | "
        f"active run {snapshot['active_run'] or 'none'} | "
        f"human review {snapshot['human_reviewed_at']}"
    )
    print("claim statuses: " + ", ".join(f"{key}={value}" for key, value in sorted(statuses.items())))
    blocking = [claim["id"] for claim in state["claims"] if claim["blocking"]]
    print("blocking claims: " + ", ".join(blocking))
    return print_validation(issues)


def validate_mapping_proposal(proposal: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    validate_json_schema(proposal, SCHEMA_BY_KIND["mapping"], issues, "PROPOSAL_SCHEMA_RULE", "mapping-proposal")
    required = {"schema_version", "proposal_id", "status", "source_files", "candidate_state", "unresolved_mappings"}
    for field in sorted(required - proposal.keys()):
        add_issue(issues, "error", "PROPOSAL_FIELD", f"missing top-level field {field}")
    if proposal.get("schema_version") != "1.0" or proposal.get("status") != "proposal_only":
        add_issue(issues, "error", "PROPOSAL_AUTHORITY", "mapping proposal must use schema 1.0 and status proposal_only")
    if not re.fullmatch(r"MAP-[A-Za-z0-9._-]+", str(proposal.get("proposal_id", ""))):
        add_issue(issues, "error", "PROPOSAL_ID", "invalid proposal_id")
    source_files = proposal.get("source_files", [])
    if not isinstance(source_files, list):
        add_issue(issues, "error", "PROPOSAL_SOURCES", "source_files must be an array")
    else:
        for record in source_files:
            if isinstance(record, dict):
                check_hashed_file(record, issues, "PROPOSAL_SOURCE")
            else:
                add_issue(issues, "error", "PROPOSAL_SOURCE_RECORD", "source file reference is not an object")
    unresolved = proposal.get("unresolved_mappings", [])
    if not isinstance(unresolved, list):
        add_issue(issues, "error", "PROPOSAL_UNRESOLVED", "unresolved_mappings must be an array")
    else:
        for index, item in enumerate(unresolved):
            fields = {"field", "source_value", "candidates", "conservative_default", "reason", "owner_decision_required"}
            if not isinstance(item, dict) or not fields.issubset(item) or item.get("owner_decision_required") is not True:
                add_issue(issues, "error", "PROPOSAL_MAPPING", f"unresolved_mappings[{index}] lacks a complete owner-decision record")
    candidate = proposal.get("candidate_state")
    if isinstance(candidate, dict):
        issues.extend(validate_state(candidate))
    else:
        add_issue(issues, "error", "PROPOSAL_CANDIDATE", "candidate_state must be an object")
    add_issue(issues, "warning", "PROPOSAL_NONCANONICAL", "this file is a review proposal and cannot update canonical state")
    return issues


def command_dashboard(
    state: dict[str, Any],
    issues: list[dict[str, str]],
    *,
    output_path: Path = DASHBOARD_PATH,
    mode_label: str = "CANONICAL MIRROR · HUMAN-GATED",
    source_label: str = "research/machine/project-state.json",
) -> int:
    if any(issue["severity"] == "error" for issue in issues):
        print_validation(issues)
        print("dashboard not rebuilt because validation failed", file=sys.stderr)
        return 1
    try:
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"missing dashboard template: {TEMPLATE_PATH.relative_to(ROOT)}", file=sys.stderr)
        return 1
    state_json = json.dumps(state, ensure_ascii=False).replace("</", "<\\/")
    validation_json = json.dumps(issues, ensure_ascii=False).replace("</", "<\\/")
    rendered = (
        template.replace("__STATE_JSON__", state_json)
        .replace("__VALIDATION_JSON__", validation_json)
        .replace("__GENERATED_AT__", datetime.now(timezone.utc).isoformat(timespec="seconds"))
        .replace("__MODE_LABEL__", mode_label)
        .replace("__STATE_SOURCE__", source_label)
    )
    output_path.write_text(rendered, encoding="utf-8")
    print(output_path)
    return 0


def _latex_escape_prose(text: str) -> str:
    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = text.replace("`", "")
    pieces = re.split(r"(\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]|\\\(.*?\\\))", text)
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for index in range(0, len(pieces), 2):
        pieces[index] = "".join(replacements.get(character, character) for character in pieces[index])
    return "".join(pieces)


def _markdown_to_latex(text: str) -> list[str]:
    output: list[str] = []
    in_code = False
    in_items = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_items:
                output.append(r"\end{itemize}")
                in_items = False
            output.append(r"\end{Verbatim}" if in_code else r"\begin{Verbatim}[breaklines=true,breakanywhere=true,fontsize=\small]")
            in_code = not in_code
            continue
        if in_code:
            output.append(line.replace("\\end{Verbatim}", r"\textbackslash{}end\{Verbatim\}"))
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            if in_items:
                output.append(r"\end{itemize}")
                in_items = False
            command = "subsection" if len(heading.group(1)) == 1 else "subsubsection"
            output.append(rf"\{command}*{{{_latex_escape_prose(heading.group(2))}}}")
            continue
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        if bullet:
            if not in_items:
                output.append(r"\begin{itemize}")
                in_items = True
            output.append(rf"\item {_latex_escape_prose(bullet.group(1))}")
            continue
        if in_items:
            output.append(r"\end{itemize}")
            in_items = False
        if not line:
            output.append(r"\par")
        elif line.strip().startswith("$$") or line.strip().startswith(r"\["):
            output.append(line)
        else:
            output.append(_latex_escape_prose(line) + " ")
    if in_items:
        output.append(r"\end{itemize}")
    if in_code:
        output.append(r"\end{Verbatim}")
    return output


def command_report() -> int:
    missing = [relative for relative in CORE_RESEARCH_FILES if not (ROOT / relative).is_file()]
    if missing:
        print("cannot build the research summary; missing: " + ", ".join(missing), file=sys.stderr)
        return 1
    sections = [(relative, (ROOT / relative).read_text(encoding="utf-8")) for relative in CORE_RESEARCH_FILES]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    md = ["# Consolidated mathematical research summary", "", "This document gathers the current core mathematical record. Authority remains with the source files named below.", ""]
    for relative, content in sections:
        md.extend([f"## {relative}", "", content.rstrip(), ""])
    REPORT_MD_PATH.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
    tex = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[margin=1in]{geometry}",
        r"\usepackage{fontspec}",
        r"\usepackage{xeCJK}",
        r"\usepackage{fvextra}",
        r"\setlength{\parindent}{0pt}",
        r"\title{Consolidated Mathematical Research Summary}",
        r"\date{}",
        r"\begin{document}",
        r"\maketitle",
        r"The source files named in each section remain authoritative.",
    ]
    for relative, content in sections:
        safe_title = relative.replace("_", r"\_")
        tex.append(rf"\section*{{{safe_title}}}")
        tex.extend(_markdown_to_latex(content.rstrip()))
    tex.append(r"\end{document}")
    REPORT_TEX_PATH.write_text("\n".join(tex) + "\n", encoding="utf-8")
    engine = shutil.which("xelatex")
    if not engine:
        print(f"wrote {REPORT_MD_PATH} and {REPORT_TEX_PATH}; xelatex is required to generate the PDF", file=sys.stderr)
        return 1
    command = [engine, "-interaction=nonstopmode", "-halt-on-error", "-output-directory", str(REPORT_DIR), str(REPORT_TEX_PATH)]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    for suffix in (".aux", ".log", ".out"):
        auxiliary = REPORT_TEX_PATH.with_suffix(suffix)
        if auxiliary.exists():
            auxiliary.unlink()
    if result.returncode or not REPORT_PDF_PATH.is_file():
        print(result.stdout[-4000:], file=sys.stderr)
        print("LaTeX could not generate the readable PDF", file=sys.stderr)
        return 1
    print(REPORT_MD_PATH)
    print(REPORT_TEX_PATH)
    print(REPORT_PDF_PATH)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="check schema invariants, references, hashes, and DAG")
    subparsers.add_parser("summary", help="print the machine-state summary")
    status_parser = subparsers.add_parser("status", help="show one proof claim")
    status_parser.add_argument("claim_id")
    blockers_parser = subparsers.add_parser("blockers", help="show the blocking dependency closure")
    blockers_parser.add_argument("claim_id")
    subparsers.add_parser("dashboard", help="validate and rebuild dashboard/index.html")
    subparsers.add_parser("report", help="generate the consolidated Markdown, LaTeX, and PDF research summary")
    proposal_parser = subparsers.add_parser("validate-proposal", help="validate a non-canonical state-mapping proposal")
    proposal_parser.add_argument("path", nargs="?", default=str(PROPOSAL_PATH))
    preview_parser = subparsers.add_parser("dashboard-proposal", help="build a visibly non-canonical proposal preview")
    preview_parser.add_argument("path", nargs="?", default=str(PROPOSAL_PATH))
    args = parser.parse_args()

    if args.command in {"validate-proposal", "dashboard-proposal"}:
        proposal_path = Path(args.path).expanduser().resolve()
        proposal = load_json(proposal_path)
        proposal_issues = validate_mapping_proposal(proposal)
        if args.command == "validate-proposal":
            return print_validation(proposal_issues)
        candidate = proposal.get("candidate_state", {})
        return command_dashboard(
            candidate,
            proposal_issues,
            output_path=PROPOSAL_DASHBOARD_PATH,
            mode_label="PROPOSAL PREVIEW · NOT CANONICAL",
            source_label=str(proposal_path),
        )

    if args.command == "report":
        return command_report()

    state = load_json(STATE_PATH)
    issues = validate_state(state)
    if args.command == "validate":
        return print_validation(issues)
    if args.command == "summary":
        return command_summary(state, issues)
    if args.command == "status":
        return command_status(state, args.claim_id)
    if args.command == "blockers":
        return command_blockers(state, args.claim_id)
    if args.command == "dashboard":
        return command_dashboard(state, issues)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
