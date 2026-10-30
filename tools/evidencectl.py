#!/usr/bin/env python3
"""Inspect portable evidence bundles; never execute their commands or approve claims."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


KINDS = {"finite_check", "formal_certificate", "numerical_experiment", "source_audit"}
FIELDS = {"schema_version", "status", "kind", "statement", "scope", "derivation_roots",
          "files", "execution", "outcome", "limitations", "review_required", "formal"}


def file_ref(root: Path, relative: str) -> dict[str, str]:
    """Make a content reference for an already trusted, project-relative file."""
    path = safe_file(root, relative)
    return {"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def safe_file(root: Path, relative: str) -> Path:
    parts = PurePosixPath(relative)
    if (not relative or parts.is_absolute() or ".." in parts.parts or "\\" in relative
            or ":" in relative or relative != parts.as_posix()):
        raise ValueError("file path must be a normalized relative POSIX path")
    root = root.resolve(strict=True)
    path = root
    for part in parts.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("file path crosses a symbolic link")
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError("file is missing or outside the evidence root")
    return path


def inspect(record: Any, root: Path) -> list[str]:
    """Check metadata and content integrity, not the truth of the recorded outcome."""
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors: list[str] = []
    missing = (FIELDS - {"formal"}) - record.keys()
    if missing:
        errors.append(f"missing fields: {', '.join(sorted(missing))}")
    if record.keys() - FIELDS:
        errors.append("unexpected record fields")
    if record.get("schema_version") != "1.0" or record.get("status") != "evidence_only":
        errors.append("expected schema 1.0 and evidence_only status")
    if not isinstance(record.get("kind"), str) or record["kind"] not in KINDS:
        errors.append("unknown evidence kind")
    for key in ("statement", "scope"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            errors.append(f"{key} must be nonempty")
    for key in ("derivation_roots", "limitations", "review_required"):
        value = record.get(key)
        if (not isinstance(value, list) or not value
                or any(not isinstance(x, str) or not x.strip() for x in value)):
            errors.append(f"{key} must list at least one explicit item")
    files = record.get("files")
    if not isinstance(files, list) or not files:
        errors.append("files must contain at least one content reference")
    else:
        seen: set[str] = set()
        for entry in files:
            if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
                errors.append("invalid file reference")
                continue
            relative, digest = entry["path"], entry["sha256"]
            if not isinstance(relative, str) or not isinstance(digest, str):
                errors.append("file path and digest must be strings")
                continue
            if relative in seen:
                errors.append(f"duplicate file reference: {relative}")
            seen.add(relative)
            try:
                actual = file_ref(root, relative)["sha256"]
                if digest != actual:
                    errors.append(f"content mismatch: {relative}")
            except (OSError, ValueError) as exc:
                errors.append(f"{relative}: {exc}")
    outcome = record.get("outcome")
    if not isinstance(outcome, str) or outcome not in {"passed", "failed", "inconclusive"}:
        errors.append("invalid outcome")
    execution = record.get("execution")
    if record.get("kind") == "source_audit":
        if execution is not None:
            errors.append("a source audit uses execution=null; record passages in files")
    elif not isinstance(execution, dict) or set(execution) != {"command", "tool_version", "exit_code"}:
        errors.append("execution requires command, tool_version, and exit_code")
    else:
        command = execution["command"]
        if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x for x in command):
            errors.append("command must be a nonempty argument list")
        if not isinstance(execution["tool_version"], str) or not execution["tool_version"].strip():
            errors.append("tool_version is required")
        code = execution["exit_code"]
        if type(code) is not int or code < 0 or (outcome == "passed" and code != 0):
            errors.append("exit_code must be nonnegative and zero for a passed check")
    formal = record.get("formal")
    if record.get("kind") == "formal_certificate":
        if not isinstance(formal, dict) or set(formal) != {"axioms", "has_placeholders", "theorem"}:
            errors.append("formal certificate requires theorem, axioms, and has_placeholders")
        else:
            if not isinstance(formal["theorem"], str) or not formal["theorem"].strip():
                errors.append("formal theorem identifier is required")
            if not isinstance(formal["axioms"], list) or any(not isinstance(x, str) or not x.strip() for x in formal["axioms"]):
                errors.append("formal axioms must be explicitly listed (possibly empty)")
            if type(formal["has_placeholders"]) is not bool:
                errors.append("has_placeholders must be boolean")
            elif outcome == "passed" and formal["has_placeholders"]:
                errors.append("a certificate with placeholders cannot have outcome=passed")
    elif formal is not None:
        errors.append("formal metadata is reserved for formal_certificate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--root", type=Path, help="evidence file root; defaults to record directory")
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
        errors = inspect(record, args.root or args.record.parent)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        return 1
    print("Evidence metadata and file hashes match. Outcome is self-reported; no command was replayed.")
    print("No mathematical claim or scientific conclusion has been approved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
