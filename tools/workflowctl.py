#!/usr/bin/env python3
"""Install and upgrade the reusable proof-ledger workflow kernel safely."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


KERNEL_VERSION = "2.7.0"
SCHEMA_VERSION = "2.1"
CONFIG_PATH = ".research-workflow.json"
REPORT_DIR = "research/machine"
LIBRARY_MARKER_PATH = ".research-workflow-library.json"
LIBRARY_KIND = "standalone-proof-ledger-research-workflow-library"
LIBRARY_ID = "ai-research-workflow-kernel"

FULL_TEMPLATE_FILES = (
    "runs/_template/brief.md",
    "runs/_template/task-brief.md",
    "runs/_template/learning-note-Txxx.md",
    "runs/_template/status.md",
    "runs/_template/amendments.md",
    "runs/_template/resolution-Txxx.md",
    "runs/_template/state_update_proposal.md",
    "runs/_template/director-run-summary.md",
    "runs/_template/manifest.json",
    "runs/_template/Txxx.json",
    "runs/_template/state-transition.json",
    "runs/_template/orchestration.json",
    "runs/_template/route-review.md",
    "runs/_template/route-review.json",
)

MANAGED_FILES = (
    "WORKFLOW-LICENSE",
    "tools/researchctl.py",
    "tools/workflowctl.py",
    "tools/evidencectl.py",
    "tests/test_workflow_kernel.py",
    "schemas/research-state.schema.json",
    "schemas/run-manifest.schema.json",
    "schemas/task-evidence.schema.json",
    "schemas/state-transition.schema.json",
    "schemas/state-mapping-proposal.schema.json",
    "schemas/run-hydration-proposal.schema.json",
    "schemas/workspace-roles.schema.json",
    "schemas/orchestration.schema.json",
    "schemas/route-review.schema.json",
    "research/machine/_template/project-state.proposal.json",
    "research/machine/_template/workspace-roles.json",
    "dashboard/template.html",
    "docs/research-workflow-prompts.md",
    "docs/evidence-bundles.md",
    "docs/research-workflow-prompts.en.md",
    "literature/source_note_template.md",
    ".agents/skills/research-workflow/SKILL.md",
    ".agents/skills/research-workflow/references/state-model.md",
    ".agents/skills/research-workflow/references/reuse-and-upgrades.md",
) + FULL_TEMPLATE_FILES

# Project documents remain project-owned except for these explicitly delimited blocks.
BLOCK_SPECS = (
    ("WORKFLOW.md", "owner-gates"),
    ("WORKFLOW.md", "project-inception"),
    ("WORKFLOW.md", "peer-role-tasks"),
    ("WORKFLOW.md", "director-return-loop"),
    ("WORKFLOW.md", "route-evidence-review"),
    ("WORKFLOW.md", "readable-research-record"),
    ("WORKFLOW.md", "candidate-preflight"),
    ("WORKFLOW.md", "notation-disclosure"),
    ("WORKFLOW.md", "mathematics-only-review-output"),
    ("WORKFLOW.md", "machine-control"),
    ("AGENTS.md", "project-owner-gates"),
    ("agents/protocol.md", "peer-role-topology"),
    ("agents/protocol.md", "role-return-and-route-review"),
    ("agents/protocol.md", "mathematics-only-human-output"),
    ("agents/protocol.md", "notation-disclosure"),
    ("agents/protocol.md", "dispatch-evidence"),
    ("agents/protocol.md", "run-close-and-route-gates"),
    ("agents/protocol.md", "candidate-preflight"),
    ("agents/director.md", "director-owner-gates"),
    ("agents/director.md", "director-orchestration"),
    ("agents/director.md", "mathematics-only-output"),
    ("agents/director.md", "notation-disclosure"),
    ("agents/director.md", "candidate-preflight"),
    ("agents/researcher.md", "role-return"),
    ("agents/researcher.md", "candidate-preflight"),
    ("agents/critic.md", "role-return"),
    ("agents/critic.md", "candidate-preflight"),
    ("agents/mathematical-review-template.md", "review-output-boundary"),
    ("agents/state_manager.md", "readable-research-record"),
)

INIT_SOURCE_FILES = (
    "WORKFLOW.md",
    "agents/protocol.md",
    "agents/critic.md",
    "agents/director.md",
    "agents/experimenter.md",
    "agents/mathematical-review-template.md",
    "agents/planner.md",
    "agents/researcher.md",
    "agents/runtime_config.md",
    "agents/state_manager.md",
)

INIT_TEXT_FILES = {
    "AGENTS.md": """# Project instructions for AI research sessions

## Governing workflow

Follow `WORKFLOW.md`. Before mathematical work, read `PROJECT_CHARTER.md`,
`STATE.md`, `research/problem.md`, the relevant proof-ledger rows, notation,
and the active run brief. Work on one task ID at a time and obey its stop
condition.

Distinguish exact, formal, conditional, conjectural, numerical, external, and
rejected statements. A run result does not change canonical mathematical state
without explicit human approval. Every technical-route selection or change
also requires explicit owner approval. Do not edit `paper/main.tex` unless the
task explicitly requests manuscript work and the supporting claim has passed
its evidence gate.

Run `python3 tools/researchctl.py validate` before dispatch, after evidence
returns, before a state proposal, and after an approved synchronization.

For a new project, first assess the owner's initial information, feasibility,
value, precise target, literature, and competing routes. Obtain owner approval
of the target and route before freezing the proof framework. The current task
is `0 Director`; create only the two independent top-level peers
`1 Researcher` and `2 Critic` in the same saved project.

After every approved mathematical advance, update the core mathematical files
and research log, then run `python3 tools/researchctl.py report` to rebuild the
Markdown, LaTeX, and PDF reading copies.

## Project-specific guardrails

- Replace this section with the equation, parameter, phase, notation, and
  theorem-specific restrictions approved for this project.
""",
    "PROJECT_CHARTER.md": """# Project charter

## Ideal objective

## Present project objective

## Current phase target

## Smallest attackable bottleneck

## Explicit non-goals

## Human-approved scope

Status: draft; no mathematical target is approved yet.
""",
    "STATE.md": """# Project state S0

No theorem target, proof claim, route, or active run has been approved yet.
Initialize the project through the literature, problem, and route-selection
gates in `WORKFLOW.md` before opening R001.
""",
    "research/problem.md": "# Problem specification\n\nStatus: draft.\n",
    "research/proof_ledger.md": "# Proof ledger\n\nNo claims registered.\n",
    "research/proof_map.md": "# Proof map\n\nNo dependency graph registered.\n",
    "research/route_matrix.md": "# Route matrix\n\nNo routes approved.\n",
    "research/notation.md": "# Notation\n\nNo global notation approved.\n",
    "research/assumptions.md": "# Assumptions\n\nNo assumptions approved.\n",
    "research/failed_approaches.md": "# Failed approaches\n\nNone registered.\n",
    "research/research_log.md": "# Research log\n\n",
    "research/task_index.md": "# Task index\n\nNo tasks registered.\n",
    "research/open_questions.md": "# Open questions\n\n",
    "research/baseline_checks.md": "# Baseline checks\n\n",
    "research/core_difficulties.md": "# Core difficulties\n\n",
    "research/objectives.md": "# Objectives\n\nSee `PROJECT_CHARTER.md`.\n",
}


def migrate_state_1_0_to_1_1(state: dict[str, Any]) -> dict[str, Any]:
    migrated = json.loads(json.dumps(state))
    migrated["schema_version"] = "1.1"
    return migrated


def route_slug(old_id: str) -> str:
    if old_id.startswith("route:"):
        return old_id
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", old_id).strip("-").lower() or "legacy"
    return f"route:{slug}"


def migrate_state_1_1_to_2_0(state: dict[str, Any]) -> dict[str, Any]:
    """Split legacy combined R-identifiers into route and run namespaces."""
    migrated = json.loads(json.dumps(state))
    id_map: dict[str, str] = {}
    runs: list[dict[str, Any]] = []
    for route in migrated.get("routes", []):
        old_id = str(route.get("id", "legacy"))
        new_id = route_slug(old_id)
        id_map[old_id] = new_id
        route["id"] = new_id
        if re.fullmatch(r"R[0-9]+", old_id):
            route["legacy_id"] = old_id
            operational = route.get("operational_status")
            run_status = operational if operational in {"planned", "running", "gated", "completed", "rejected"} else "completed"
            runs.append({
                "id": old_id,
                "route_id": new_id,
                "status": run_status,
                "state_in": None,
                "note": "Structural migration of the legacy combined route/run record; mathematical content is unchanged.",
            })
    for edge in migrated.get("edges", []):
        if edge.get("from") in id_map:
            edge["from"] = id_map[edge["from"]]
    snapshot = migrated.setdefault("snapshot", {})
    legacy_active = snapshot.get("active_run")
    snapshot["active_route"] = id_map.get(legacy_active) if isinstance(legacy_active, str) else None
    if isinstance(legacy_active, str) and not any(item["id"] == legacy_active for item in runs):
        runs.append({
            "id": legacy_active,
            "route_id": None,
            "status": "running",
            "state_in": None,
            "note": "Active run preserved during namespace migration; no route relation was inferable.",
        })
    migrated["runs"] = runs
    migrated["schema_version"] = "2.0"
    return migrated


def migrate_state_2_0_to_2_1(state: dict[str, Any]) -> dict[str, Any]:
    """Add theorem-target mapping without inferring a mathematical target."""
    migrated = json.loads(json.dumps(state))
    migrated.setdefault("snapshot", {}).setdefault("theorem_targets", [])
    migrated["schema_version"] = "2.1"
    return migrated


STATE_MIGRATIONS = {
    "1.0": ("1.1", migrate_state_1_0_to_1_1),
    "1.1": ("2.0", migrate_state_1_1_to_2_0),
    "2.0": ("2.1", migrate_state_2_0_to_2_1),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"expected a JSON object in {path}")
    return value


def marker(block_id: str, edge: str) -> str:
    return f"<!-- research-workflow:block {block_id} {edge} -->"


def extract_block(source: str, block_id: str) -> str:
    start, end = marker(block_id, "start"), marker(block_id, "end")
    if source.count(start) != 1 or source.count(end) != 1:
        raise RuntimeError(f"source block {block_id!r} is missing or duplicated")
    remainder = source.split(start, 1)[1]
    body = remainder.split(end, 1)[0]
    return f"{start}{body}{end}"


def extract_existing_block(current: str, block_id: str) -> str | None:
    start, end = marker(block_id, "start"), marker(block_id, "end")
    if current.count(start) == 0 and current.count(end) == 0:
        return None
    if current.count(start) != 1 or current.count(end) != 1:
        raise ValueError("malformed or duplicated managed block")
    remainder = current.split(start, 1)[1]
    body = remainder.split(end, 1)[0]
    return f"{start}{body}{end}"


def merge_block(current: str, block: str, block_id: str) -> tuple[str | None, str]:
    start, end = marker(block_id, "start"), marker(block_id, "end")
    if current.count(start) == 0 and current.count(end) == 0:
        separator = "" if not current else "\n" if current.endswith("\n") else "\n\n"
        return current + separator + block + "\n", "append block"
    if current.count(start) != 1 or current.count(end) != 1:
        return None, "malformed or duplicated managed block"
    prefix, remainder = current.split(start, 1)
    suffix = remainder.split(end, 1)[1]
    merged = prefix + block + suffix
    return merged, "update block" if merged != current else "unchanged"


class FileTransaction:
    """Restore every known destination if an applied operation fails."""

    def __init__(self, target: Path, relatives: set[str], backup_root: Path) -> None:
        self.target = target
        self.relatives = relatives
        self.backup_root = backup_root
        self.temp_root: Path | None = None
        self.existed: set[str] = set()
        self.target_existed = target.exists()

    def __enter__(self) -> "FileTransaction":
        self.temp_root = Path(tempfile.mkdtemp(prefix="research-workflow-transaction-"))
        for relative in self.relatives:
            problem = destination_safety_issue(self.target, relative)
            if problem:
                raise OSError(f"unsafe destination {relative}: {problem}")
            path = self.target / relative
            if path.is_file() and not path.is_symlink():
                self.existed.add(relative)
                saved = self.temp_root / relative
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, saved)
        return self

    def rollback(self) -> list[str]:
        if self.temp_root is None:
            return []
        failures: list[str] = []
        for relative in sorted(self.relatives, key=lambda item: item.count("/"), reverse=True):
            path = self.target / relative
            try:
                if relative in self.existed:
                    saved = self.temp_root / relative
                    if path.is_file() and not path.is_symlink() and sha256_path(path) == sha256_path(saved):
                        continue
                    path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(saved, path)
                elif path.is_file() and not path.is_symlink():
                    path.unlink()
            except OSError as exc:
                failures.append(f"{relative}: {exc}")
        if self.backup_root.is_dir():
            try:
                shutil.rmtree(self.backup_root)
            except OSError as exc:
                failures.append(f"{self.backup_root}: {exc}")
        for parent in sorted({(self.target / item).parent for item in self.relatives}, key=lambda p: len(p.parts), reverse=True):
            try:
                parent.rmdir()
            except OSError:
                pass
        if not self.target_existed:
            try:
                self.target.rmdir()
            except OSError:
                pass
        return failures

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> bool:
        rollback_failures: list[str] = []
        if exc_type is not None:
            rollback_failures = self.rollback()
        if self.temp_root is not None:
            shutil.rmtree(self.temp_root, ignore_errors=True)
        if rollback_failures:
            detail = "; ".join(rollback_failures)
            raise RuntimeError(f"rollback restored all reachable targets but failed for: {detail}") from exc
        return False


def backup_file(path: Path, target: Path, backup_root: Path) -> None:
    if not path.exists() or path.is_symlink():
        return
    destination = backup_root / path.relative_to(target)
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)


def destination_safety_issue(target: Path, relative: str) -> str | None:
    """Reject traversal and every symlink that can redirect a managed write."""
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        return "path must remain inside the project"
    if target.is_symlink():
        return "project target itself is a symlink"
    current = target
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            return f"{current.relative_to(target)} is a symlink"
    resolved_target = target.resolve(strict=False)
    resolved_parent = (target / rel).parent.resolve(strict=False)
    try:
        resolved_parent.relative_to(resolved_target)
    except ValueError:
        return "resolved parent escapes the project"
    return None


def record_action(actions: list[dict[str, str]], path: str, action: str, detail: str = "") -> None:
    actions.append({"path": path, "action": action, "detail": detail})


def library_identity(source_root: Path) -> dict[str, str]:
    """Return a verified standalone-library identity or stop before installation."""
    marker = source_root / LIBRARY_MARKER_PATH
    try:
        value = json.loads(marker.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"refusing unverified workflow source {source_root}: missing {LIBRARY_MARKER_PATH}"
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid workflow-library identity at {marker}: {exc}") from exc
    expected = {
        "schema_version": "1.0",
        "kind": LIBRARY_KIND,
        "library_id": LIBRARY_ID,
    }
    if value != expected:
        raise RuntimeError(f"unrecognized workflow-library identity at {marker}")
    if (source_root / CONFIG_PATH).exists():
        raise RuntimeError(
            f"refusing {source_root}: a standalone workflow library must not be an installed mathematical project"
        )
    return expected


def render_managed_content(source_root: Path, relative: str, content: str) -> str:
    """Render machine-local values only in installed copies, not in the source template."""
    if relative in {"docs/research-workflow-prompts.md", "docs/research-workflow-prompts.en.md"}:
        return content.replace("<WORKFLOW_LIBRARY>", str(source_root))
    return content


def write_candidate(*, target: Path, relative: str, content: str, mode: str,
                    previous_hash: str | None, apply: bool, backup_root: Path,
                    actions: list[dict[str, str]]) -> bool:
    destination = target / relative
    safety_issue = destination_safety_issue(target, relative)
    if safety_issue:
        record_action(actions, relative, "conflict", f"unsafe destination: {safety_issue}")
        return False
    encoded, desired_hash = content.encode("utf-8"), sha256_bytes(content.encode("utf-8"))
    if not destination.exists():
        record_action(actions, relative, "create")
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(encoded)
        return True
    if not destination.is_file():
        record_action(actions, relative, "conflict", "target exists and is not a file")
        return False
    actual_hash = sha256_path(destination)
    if actual_hash == desired_hash:
        record_action(actions, relative, "unchanged")
        return True
    tracked_clean = previous_hash is not None and actual_hash == previous_hash
    legacy_template = relative in FULL_TEMPLATE_FILES and previous_hash is None and mode in {"migrate", "upgrade"}
    if (mode == "upgrade" and tracked_clean) or legacy_template:
        detail = "replace versioned legacy template" if legacy_template else f"{actual_hash[:12]} -> {desired_hash[:12]}"
        record_action(actions, relative, "update", detail)
        if apply:
            backup_file(destination, target, backup_root)
            destination.write_bytes(encoded)
        return True
    record_action(actions, relative, "conflict", "local content differs from the installed kernel; merge deliberately")
    return False


def seed_missing_file(target: Path, relative: str, content: str, apply: bool,
                      actions: list[dict[str, str]]) -> None:
    destination = target / relative
    safety_issue = destination_safety_issue(target, relative)
    if safety_issue:
        record_action(actions, relative, "conflict", f"unsafe destination: {safety_issue}")
        return
    if destination.exists() or destination.is_symlink():
        record_action(actions, relative, "preserve", "project-owned file already exists")
        return
    record_action(actions, relative, "create", "new-project skeleton")
    if apply:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


def apply_document_block(*, source_root: Path, target: Path, relative: str,
                         block_id: str, previous_hash: str | None, apply: bool,
                         backup_root: Path, actions: list[dict[str, str]]) -> bool:
    source_path, target_path = source_root / relative, target / relative
    if not source_path.is_file():
        raise RuntimeError(f"kernel source is missing {relative}")
    block = extract_block(source_path.read_text(encoding="utf-8"), block_id)
    safety_issue = destination_safety_issue(target, relative)
    if safety_issue:
        record_action(actions, relative, "conflict", f"unsafe destination: {safety_issue}")
        return False
    current = target_path.read_text(encoding="utf-8") if target_path.is_file() else ""
    try:
        existing = extract_existing_block(current, block_id)
    except ValueError as exc:
        record_action(actions, relative, "conflict", str(exc))
        return False
    desired_hash = sha256_bytes(block.encode("utf-8"))
    if existing is not None:
        actual_hash = sha256_bytes(existing.encode("utf-8"))
        if actual_hash != desired_hash and (previous_hash is None or actual_hash != previous_hash):
            record_action(actions, relative, "conflict", f"managed block {block_id} was locally modified")
            return False
    merged, detail = merge_block(current, block, block_id)
    if merged is None:
        record_action(actions, relative, "conflict", detail)
        return False
    if merged == current:
        record_action(actions, relative, "unchanged", f"managed block {block_id}")
        return True
    record_action(actions, relative, "update" if current else "create", f"managed block {block_id}")
    if apply:
        if target_path.exists():
            backup_file(target_path, target, backup_root)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(merged, encoding="utf-8")
    return True


def detected_ids(target: Path) -> dict[str, list[str]]:
    texts: list[str] = []
    for relative in ("STATE.md", "research/proof_ledger.md", "research/proof_map.md", "research/route_matrix.md"):
        path = target / relative
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8", errors="replace"))
    joined = "\n".join(texts)
    claims = sorted(set(re.findall(r"(?<![A-Za-z0-9])P\d+(?![A-Za-z0-9])", joined)), key=lambda item: int(item[1:]))
    run_ids = sorted({path.name for path in (target / "runs").glob("R[0-9]*") if path.is_dir()}, key=lambda item: int(item[1:])) if (target / "runs").is_dir() else []
    route_labels: set[str] = set()
    stopwords = {"matrix", "history", "selection", "status", "comparison", "map"}
    for line in joined.splitlines():
        if re.match(r"^\s*#+\s*Route\s+Matrix\s*$", line, re.IGNORECASE):
            continue
        for label in re.findall(r"\bRoute\s+([A-Za-z][A-Za-z0-9._-]*)", line):
            if label.lower() not in stopwords:
                route_labels.add(label)
    return {"claim_ids": claims, "run_ids": run_ids, "route_labels": sorted(route_labels)}


def empty_state(target: Path, project_name: str) -> dict[str, Any]:
    canonical_files = []
    for relative in ("STATE.md", "research/proof_ledger.md", "research/proof_map.md"):
        path = target / relative
        if path.is_file():
            canonical_files.append({"path": relative, "sha256": sha256_path(path)})
    return {
        "schema_version": SCHEMA_VERSION,
        "snapshot": {"project_name": project_name, "state_version": "S0", "human_reviewed_at": datetime.now(timezone.utc).date().isoformat(),
                     "theorem_targets": [], "active_route": None, "active_run": None, "authority": "machine_mirror",
                     "note": f"Empty S0 scaffold for {project_name}; no mathematical target or route is approved."},
        "canonical_files": canonical_files, "claims": [], "routes": [], "runs": [], "edges": [],
    }


def upgrade_state_schema(*, target: Path, apply: bool, backup_root: Path,
                         actions: list[dict[str, str]]) -> bool:
    relative, path = "research/machine/project-state.json", target / "research/machine/project-state.json"
    if not path.exists():
        return False
    if path.is_symlink() or not path.is_file():
        record_action(actions, relative, "conflict", "state path is not a regular file")
        return False
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        record_action(actions, relative, "conflict", f"cannot parse state: {exc}")
        return False
    version, start_version, visited = state.get("schema_version"), state.get("schema_version"), set()
    if version == SCHEMA_VERSION:
        if state.setdefault("snapshot", {}).get("project_name"):
            record_action(actions, relative, "unchanged", f"schema {SCHEMA_VERSION}")
            return True
        state["snapshot"]["project_name"] = target.name
        record_action(actions, relative, "update", f"schema {SCHEMA_VERSION}; add project display name")
        if apply:
            backup_file(path, target, backup_root)
            path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return True
    while version != SCHEMA_VERSION:
        if not isinstance(version, str) or version in visited or version not in STATE_MIGRATIONS:
            record_action(actions, relative, "conflict", f"no registered schema migration from {version!r} to {SCHEMA_VERSION}")
            return False
        visited.add(version)
        next_version, transform = STATE_MIGRATIONS[version]
        state, version = transform(state), next_version
    state.setdefault("snapshot", {}).setdefault("project_name", target.name)
    record_action(actions, relative, "update", f"schema {start_version} -> {SCHEMA_VERSION}; registered structural migrations only")
    if apply:
        backup_file(path, target, backup_root)
        path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def upgrade_workspace_roles(*, target: Path, apply: bool, backup_root: Path,
                            actions: list[dict[str, str]]) -> bool:
    relative = "research/machine/workspace-roles.json"
    path = target / relative
    if not path.exists():
        record_action(actions, relative, "preserve", "role registry not yet created")
        return True
    safety_issue = destination_safety_issue(target, relative)
    if safety_issue:
        record_action(actions, relative, "conflict", f"unsafe destination: {safety_issue}")
        return False
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        record_action(actions, relative, "conflict", f"cannot parse role registry: {exc}")
        return False
    version = value.get("schema_version")
    if version == "1.1":
        record_action(actions, relative, "unchanged", "role registry schema 1.1")
        return True
    if version != "1.0" or not isinstance(value.get("roles"), list):
        record_action(actions, relative, "conflict", f"no registered role migration from {version!r} to '1.1'")
        return False
    expected_titles = {"director": "0 Director", "researcher": "1 Researcher", "critic": "2 Critic"}
    roles = value["roles"]
    if len(roles) != 3 or {item.get("role") for item in roles if isinstance(item, dict)} != set(expected_titles):
        record_action(actions, relative, "conflict", "legacy role registry does not contain exactly the three known roles")
        return False
    migrated = copy.deepcopy(value)
    migrated["schema_version"] = "1.1"
    for record in migrated["roles"]:
        role = record["role"]
        record["title"] = expected_titles[role]
        record["is_current_task"] = role == "director"
    record_action(actions, relative, "update", "role registry 1.0 -> 1.1; preserve task identities")
    if apply:
        backup_file(path, target, backup_root)
        path.write_text(json.dumps(migrated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def print_actions(actions: list[dict[str, str]], apply: bool) -> None:
    print(f"mode: {'apply' if apply else 'preview'}")
    for item in actions:
        detail = f" — {item['detail']}" if item["detail"] else ""
        print(f"[{item['action'].upper()}] {item['path']}{detail}")


def hydrate_run(args: argparse.Namespace) -> int:
    """Propose machine sidecars for one historical run without rewriting it."""
    target = Path(args.target).expanduser().absolute()
    if not target.is_dir():
        raise SystemExit(f"target project does not exist: {target}")
    if not args.proposal_only:
        raise SystemExit("hydrate-run requires --proposal-only; canonical sidecars need owner review")
    run_id = args.run_id
    if not isinstance(run_id, str) or not re.fullmatch(r"R[0-9]+", run_id):
        raise SystemExit("run_id must have the form R<number>")
    runs_root = target / "runs"
    matches = [path for path in runs_root.iterdir() if path.is_dir() and re.search(rf"(?:^|-)({re.escape(run_id)})$", path.name)] if runs_root.is_dir() else []
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one historical directory for {run_id}; found {len(matches)}")
    run_dir = matches[0]
    relative_dir = run_dir.relative_to(target)
    output = run_dir / "run-hydration.proposal.json"
    safety_issue = destination_safety_issue(target, str(output.relative_to(target)))
    if safety_issue:
        print(f"[CONFLICT] {output.relative_to(target)} — unsafe destination: {safety_issue}")
        return 1
    artifacts: list[dict[str, str]] = []
    task_ids: set[str] = set()
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file() or path.is_symlink() or path == output:
            continue
        relative = str(path.relative_to(target))
        artifacts.append({"path": relative, "sha256": sha256_path(path)})
        task_ids.update(re.findall(r"T[0-9]+", path.name))
        if path.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml"}:
            task_ids.update(re.findall(r"(?<![A-Za-z0-9])T[0-9]+(?![A-Za-z0-9])", path.read_text(encoding="utf-8", errors="replace")))
    ordered_tasks = sorted(task_ids, key=lambda item: int(item[1:]))
    proposal = {
        "schema_version": "1.1",
        "status": "proposal_only",
        "run_id": run_id,
        "source_directory": str(relative_dir),
        "source_artifacts": artifacts,
        "detected_task_ids": ordered_tasks,
        "proposed_sidecars": {
            "manifest": str(relative_dir / "manifest.json"),
            "task_records": [str(relative_dir / f"{task_id}.json") for task_id in ordered_tasks],
            "state_transition": str(relative_dir / "state-transition.json"),
            "orchestration": str(relative_dir / "orchestration.json"),
            "route_review": str(relative_dir / "route-review.json"),
        },
        "unresolved_mappings": [
            "state_in must be confirmed from the canonical state at run opening",
            "route_id and its owner approval reference must be confirmed",
            "run status and every task verdict/evidence class must be reviewed",
            "derivation roots and independence claims must be reconstructed from decisive mathematics",
            "a state transition may be materialized only if an authoritative decision artifact exists",
            "route signal and any route-review trigger must be reconstructed from the mathematical outcomes",
        ],
    }
    encoded = json.dumps(proposal, indent=2, ensure_ascii=False) + "\n"
    action = "create" if not output.exists() else "unchanged" if output.read_text(encoding="utf-8") == encoded else "conflict"
    print(f"target: {target}\nrun: {run_id}\nmode: {'apply' if args.apply else 'preview'}")
    print(f"[{action.upper()}] {output.relative_to(target)} — proposal-only; {len(artifacts)} source artifact(s), {len(ordered_tasks)} task ID(s)")
    if action == "conflict":
        print("result: existing hydration proposal differs; preserve it for deliberate review")
        return 1
    if args.apply and action == "create":
        backup_root = target / ".research-workflow" / "backups" / utc_stamp()
        with FileTransaction(target, {str(output.relative_to(target))}, backup_root):
            output.write_text(encoded, encoding="utf-8")
    elif not args.apply:
        print("preview only; rerun with --apply to write the proposal")
    return 0


def _operate_once(args: argparse.Namespace) -> int:
    source_root = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
    target = Path(args.target).expanduser().absolute()
    if target == Path("/"):
        raise SystemExit("refusing to use the filesystem root as a project target")
    if not source_root.is_dir():
        raise SystemExit(f"kernel source is not a directory: {source_root}")
    identity = library_identity(source_root)
    profile = load_json(target / "profile.json")
    if profile.get("profile") == "ai4s":
        raise RuntimeError("AI4S is an experimental separate profile; AI4Math init/migrate/upgrade/status do not apply")
    if args.mode in {"migrate", "upgrade", "status"} and not target.is_dir():
        raise SystemExit(f"target project does not exist: {target}")
    config_file = target / CONFIG_PATH
    previous = load_json(config_file)
    if args.mode == "upgrade" and not previous:
        raise SystemExit("target has no .research-workflow.json; run migrate first")
    if args.mode == "status":
        installed = previous.get("kernel_version", "not installed")
        print(f"target: {target}\ninstalled kernel: {installed}\navailable kernel: {KERNEL_VERSION}\nstate mapping: {previous.get('state_mapping', 'unknown')}")
        return 0 if installed == KERNEL_VERSION else 1

    apply, stamp = bool(args.apply), utc_stamp()
    backup_root = target / ".research-workflow" / "backups" / stamp
    report_relative = f"{REPORT_DIR}/workflow-{args.mode}-{stamp}.json"
    known_paths = set(MANAGED_FILES) | {item[0] for item in BLOCK_SPECS} | set(INIT_SOURCE_FILES) | set(INIT_TEXT_FILES) | {
        CONFIG_PATH, "research/machine/project-state.json", "research/machine/workspace-roles.json", report_relative,
    }
    unsafe = [(relative, destination_safety_issue(target, relative)) for relative in sorted(known_paths)]
    unsafe = [(relative, problem) for relative, problem in unsafe if problem]
    if unsafe:
        print(f"source: {source_root}\ntarget: {target}\nkernel: {KERNEL_VERSION}")
        for relative, problem in unsafe:
            print(f"[CONFLICT] {relative} — unsafe destination: {problem}")
        print(f"result: {len(unsafe)} unsafe destination(s); no files written")
        return 1
    context = FileTransaction(target, known_paths, backup_root) if apply else None

    def execute() -> int:
        actions: list[dict[str, str]] = []
        prior_hashes = previous.get("managed_files", {}) if isinstance(previous.get("managed_files"), dict) else {}
        prior_blocks = previous.get("managed_blocks", {}) if isinstance(previous.get("managed_blocks"), dict) else {}
        if args.mode == "init":
            if apply:
                target.mkdir(parents=True, exist_ok=True)
            for relative in INIT_SOURCE_FILES:
                source_path = source_root / relative
                if not source_path.is_file():
                    raise RuntimeError(f"kernel source is missing {relative}")
                seed_missing_file(target, relative, source_path.read_text(encoding="utf-8"), apply, actions)
            for relative, content in INIT_TEXT_FILES.items():
                seed_missing_file(target, relative, content, apply, actions)

        installed_hashes: dict[str, str] = dict(prior_hashes)
        for relative in MANAGED_FILES:
            source_path = source_root / relative
            if not source_path.is_file():
                raise RuntimeError(f"kernel source is missing {relative}")
            content = render_managed_content(
                source_root, relative, source_path.read_text(encoding="utf-8")
            )
            accepted = write_candidate(target=target, relative=relative, content=content, mode=args.mode,
                                       previous_hash=prior_hashes.get(relative), apply=apply,
                                       backup_root=backup_root, actions=actions)
            if accepted:
                installed_hashes[relative] = sha256_bytes(content.encode("utf-8"))

        # Rebuild from the current block registry so retired block ownership is
        # not carried forward indefinitely.
        block_hashes: dict[str, str] = {}
        for relative, block_id in BLOCK_SPECS:
            accepted = apply_document_block(source_root=source_root, target=target, relative=relative,
                                            block_id=block_id, previous_hash=prior_blocks.get(block_id),
                                            apply=apply, backup_root=backup_root, actions=actions)
            if accepted:
                block = extract_block((source_root / relative).read_text(encoding="utf-8"), block_id)
                block_hashes[block_id] = sha256_bytes(block.encode("utf-8"))

        state_path = target / "research/machine/project-state.json"
        state_mapping = "ready" if upgrade_state_schema(target=target, apply=apply, backup_root=backup_root, actions=actions) else "required"
        upgrade_workspace_roles(target=target, apply=apply, backup_root=backup_root, actions=actions)
        if args.mode == "init" and not state_path.exists():
            record_action(actions, "research/machine/project-state.json", "create", "empty S0 mirror")
            if apply:
                state_path.parent.mkdir(parents=True, exist_ok=True)
                state_path.write_text(json.dumps(empty_state(target, args.project_name or target.name), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            state_mapping = "ready"

        conflicts = [item for item in actions if item["action"] == "conflict"]
        if apply and conflicts:
            raise RuntimeError(f"preflight race: {len(conflicts)} conflict(s) appeared during apply")
        report = {
            "operation": args.mode, "applied": apply, "transactional": True, "kernel_version": KERNEL_VERSION,
            "source_root": str(source_root), "target_root": str(target), "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "state_mapping": state_mapping, "detected": detected_ids(target) if target.is_dir() else {"claim_ids": [], "run_ids": [], "route_labels": []},
            "actions": actions, "conflicts": conflicts,
            "next_gate": "Review and construct research/machine/project-state.json from canonical files." if state_mapping == "required" else "Run python3 tools/researchctl.py validate and review any warnings.",
        }
        if apply:
            config = {"kernel_version": KERNEL_VERSION, "schema_version": SCHEMA_VERSION,
                      "installed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "source_hint": str(source_root),
                      "source_library_id": identity["library_id"],
                      "state_mapping": state_mapping, "managed_files": installed_hashes, "managed_blocks": block_hashes}
            config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            report_path = target / report_relative
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            record_action(actions, CONFIG_PATH, "write", f"kernel {KERNEL_VERSION}")
            record_action(actions, report_relative, "write", "operation report")
        print(f"source: {source_root}\ntarget: {target}\nkernel: {KERNEL_VERSION}")
        print_actions(actions, apply)
        print(f"result: {len(conflicts)} conflict(s); state mapping {state_mapping}")
        if not apply:
            print("preview only; rerun with --apply to write these changes")
        return 1 if conflicts else 0

    if context is None:
        return execute()
    with context:
        return execute()


def operate(args: argparse.Namespace) -> int:
    if args.mode == "init-ai4s":
        # AI4S is a fresh-workspace profile, never a migration of mathematical state.
        source_root = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
        try:
            library_identity(source_root)
            command = [sys.executable, str(source_root / "tools/scaffold_ai4s.py"), args.target,
                       "--project-name", args.project_name or Path(args.target).name]
            if args.apply:
                command.append("--apply")
            return subprocess.run(command, check=False).returncode
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"AI4S scaffold failed: {exc}", file=sys.stderr)
            return 1
    if args.mode == "identify":
        source_root = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
        try:
            identity = library_identity(source_root)
        except RuntimeError as exc:
            print(f"identity check failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps({**identity, "kernel_version": KERNEL_VERSION, "path": str(source_root)}, ensure_ascii=False))
        return 0
    if args.mode == "self-check":
        source_root = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
        return self_check(source_root)
    if args.mode == "hydrate-run":
        return hydrate_run(args)
    try:
        if args.apply and args.mode != "status" and not getattr(args, "_preflight_done", False):
            preview = copy.copy(args)
            preview.apply = False
            preview._preflight_done = True
            result = _operate_once(preview)
            if result:
                print("apply cancelled: preflight reported conflicts; no target files were written", file=sys.stderr)
                return result
            print("preflight passed; beginning transactional apply")
        return _operate_once(args)
    except (OSError, RuntimeError) as exc:
        print(f"apply failed and was rolled back: {exc}", file=sys.stderr)
        return 1


def self_check(source_root: Path) -> int:
    """Check the reusable kernel without pretending it is a research project."""
    problems: list[str] = []
    required = set(MANAGED_FILES) | set(INIT_SOURCE_FILES) | {
        "AGENTS.md", "WORKFLOW.md", "README.md", "CHANGELOG.md", "workflow",
        ".github/workflows/kernel-check.yml", LIBRARY_MARKER_PATH,
        "LICENSE", "README.zh-CN.md", "tools/publication_check.py", "tools/scaffold_ai4s.py",
        "profiles/ai4s/template/WORKFLOW.md", "profiles/ai4s/template/AGENTS.md",
        "examples/ai4math/verify.py", "examples/ai4s/experiment.py",
    }
    for relative in sorted(required):
        path = source_root / relative
        if not path.is_file() or path.is_symlink():
            problems.append(f"missing or linked kernel source: {relative}")
    for path in sorted((source_root / "schemas").glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"invalid schema {path.relative_to(source_root)}: {exc}")
            continue
        if value.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            problems.append(f"wrong schema dialect: {path.relative_to(source_root)}")
    for relative, block_id in BLOCK_SPECS:
        try:
            extract_block((source_root / relative).read_text(encoding="utf-8"), block_id)
        except (OSError, ValueError) as exc:
            problems.append(f"invalid managed block {relative}:{block_id}: {exc}")
    for relative in sorted(required):
        path = source_root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"/(?:Users|home)/[A-Za-z0-9._-]+/", text):
            problems.append(f"personal home-directory path in {relative}")
    try:
        library_identity(source_root)
    except RuntimeError as exc:
        problems.append(str(exc))
    run_entries = {
        path.name for path in (source_root / "runs").iterdir()
        if path.name not in {".DS_Store"}
    } if (source_root / "runs").is_dir() else set()
    if run_entries != {"README.md", "_template"}:
        problems.append(f"source runs directory contains project data: {sorted(run_entries)}")
    if problems:
        for problem in problems:
            print(f"[ERROR] {problem}")
        print(f"self-check: {len(problems)} error(s)")
        return 1
    publication = subprocess.run(
        [sys.executable, str(source_root / "tools/publication_check.py"), str(source_root)],
        text=True, capture_output=True, check=False,
    )
    print(publication.stdout, end="")
    if publication.returncode:
        print(publication.stderr, end="", file=sys.stderr)
        return publication.returncode
    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests"]
    result = subprocess.run(command, cwd=source_root, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        print("self-check: automated tests failed")
        return result.returncode
    print(f"self-check: kernel {KERNEL_VERSION} is internally consistent")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("init", "init-ai4s", "migrate", "upgrade", "status", "hydrate-run", "identify", "self-check"))
    parser.add_argument("target", nargs="?", help="project directory; omitted for identify and self-check")
    parser.add_argument("run_id", nargs="?", help="historical run ID for hydrate-run")
    parser.add_argument("--source", help="root of the newer workflow kernel; defaults to this script's project")
    parser.add_argument("--project-name", help="new-project display name; defaults to the directory name")
    parser.add_argument("--apply", action="store_true", help="apply only after a successful no-write preflight")
    parser.add_argument("--proposal-only", action="store_true", help="required safety gate for hydrate-run")
    args = parser.parse_args()
    if args.mode not in {"identify", "self-check"} and not args.target:
        parser.error("target is required unless mode is identify or self-check")
    return operate(args)


if __name__ == "__main__":
    raise SystemExit(main())
