#!/usr/bin/env python3
"""Inspect frozen mathematical check plans; execute trusted plans only with --run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time
from typing import Any

import evidencectl

SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"


def schema_errors(value: Any, name: str) -> list[str]:
    import researchctl
    schema = json.loads((SCHEMAS / (name + ".schema.json")).read_text())
    return researchctl._schema_errors(value, schema, schema, name)


def read_reference(root: Path, reference: dict) -> Path:
    if not isinstance(reference, dict) or set(reference) != {"path", "sha256"}:
        raise ValueError("expected a hashed file reference")
    if not isinstance(reference["path"], str) or not isinstance(reference["sha256"], str):
        raise ValueError("reference path and hash must be strings")
    path = evidencectl.safe_file(root, reference["path"])
    if evidencectl.file_ref(root, reference["path"]) != reference:
        raise ValueError("content changed: " + reference["path"])
    return path


def relative_path(root: Path, path: Path) -> str:
    """Preserve links below the declared root while accepting OS root aliases."""
    for base in (root.absolute(), root.resolve(strict=True)):
        try:
            return path.absolute().relative_to(base).as_posix()
        except ValueError:
            pass
    raise ValueError("file must be inside the declared root")


def _reject_nonfinite(value: str) -> None:
    raise ValueError("non-finite JSON number: " + value)


def output_path(root: Path, relative: str) -> Path:
    """Prepare a fresh output inside the root; never overwrite existing records."""
    parsed = PurePosixPath(relative)
    if not relative or parsed.is_absolute() or ".." in parsed.parts or parsed.as_posix() != relative or "\\" in relative or ":" in relative:
        raise ValueError("output must be a normalized project-relative path")
    root = root.resolve(strict=True)
    current = root
    for part in parsed.parts:
        current /= part
        if current.is_symlink():
            raise ValueError("output crosses a symbolic link")
    if current.exists():
        raise ValueError("output already exists; choose a new result version")
    current.parent.mkdir(parents=True, exist_ok=True)
    return current


def expanded_command(plan: dict, root: Path) -> list[str]:
    values = {"{python}": sys.executable,
              "{candidate}": str(read_reference(root, plan["candidate"])),
              "{evaluator}": str(read_reference(root, plan["evaluator"]))}
    for index, reference in enumerate(plan["inputs"]):
        values["{input:" + str(index) + "}"] = str(read_reference(root, reference))
    return [values.get(argument, argument) for argument in plan["command"]]


def inspect_plan(plan: Any, root: Path) -> list[str]:
    errors = schema_errors(plan, "check-plan")
    if errors:
        return errors
    if "{evaluator}" not in plan["command"]:
        errors.append("command must name the frozen evaluator through {evaluator}")
    for reference in [plan["candidate"], plan["evaluator"], *plan["inputs"]]:
        try:
            read_reference(root, reference)
        except (OSError, ValueError, TypeError) as exc:
            errors.append(str(exc))
    return errors


def inspect_result(result: Any, root: Path) -> list[str]:
    errors = schema_errors(result, "check-result")
    if errors:
        return errors
    try:
        plan_path = read_reference(root, result["plan"])
        plan = json.loads(plan_path.read_text())
        errors.extend(inspect_plan(plan, root))
        if errors:
            return errors
        for field in ("candidate", "kind", "scope"):
            if result[field] != plan[field]:
                errors.append("result disagrees with frozen plan: " + field)
        if result["execution"]["command"] != expanded_command(plan, root):
            errors.append("execution command disagrees with frozen plan")
        if result["outcome"] in {"passed", "failed"} and (
            result["execution"]["exit_code"] != 0 or result["execution"]["timed_out"]
            or not result["inputs_unchanged"] or not result["protected_files_unchanged"] or result["evaluation"].get("outcome") != result["outcome"]
        ):
            errors.append("decisive check outcome contradicts its execution or integrity record")
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))
    return errors


def protected_snapshot(root: Path) -> dict[str, str | None]:
    """Detect collateral canonical edits without pretending to sandbox the checker."""
    import researchctl
    names = set(researchctl.CORE_RESEARCH_FILES) | {"paper/main.tex", "research/machine/project-state.json", ".research-workflow.json"}
    state_path = root / "research/machine/project-state.json"
    if state_path.is_file():
        state = json.loads(evidencectl.safe_file(root, "research/machine/project-state.json").read_text())
        if not isinstance(state, dict) or not isinstance(state.get("canonical_files", []), list):
            raise ValueError("invalid canonical-file registry")
        for reference in state.get("canonical_files", []):
            if isinstance(reference, dict) and isinstance(reference.get("path"), str):
                names.add(reference["path"])
    snapshot = {}
    for relative in sorted(names):
        path = root / relative
        if path.exists() or path.is_symlink():
            snapshot[relative] = evidencectl.file_ref(root, relative)["sha256"]
        else:
            snapshot[relative] = None
    return snapshot


def execute(plan_path: Path, root: Path, output: str) -> dict:
    """Run once without a shell. This is not a new sandbox or a proof certificate."""
    relative = relative_path(root, plan_path)
    root = root.resolve(strict=True)
    # safe_file also rejects links in the caller-supplied plan path.
    if plan_path.absolute().is_symlink():
        raise ValueError("plan cannot be a symbolic link")
    plan_ref = evidencectl.file_ref(root, relative)
    plan = json.loads(read_reference(root, plan_ref).read_text())
    errors = inspect_plan(plan, root)
    if errors:
        raise ValueError("; ".join(errors))
    destination = output_path(root, output)
    command = expanded_command(plan, root)
    references = [plan_ref, plan["candidate"], plan["evaluator"], *plan["inputs"]]
    protected_before = protected_snapshot(root)
    started = time.monotonic()
    stdout, stderr, code, timed_out = "", "", None, False
    try:
        completed = subprocess.run(command, cwd=root, text=True, encoding="utf-8", errors="replace",
                                   capture_output=True, timeout=plan["timeout_seconds"], check=False)
        stdout, stderr, code = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
    except OSError as exc:
        stderr = str(exc)
    unchanged = True
    for reference in references:
        try:
            read_reference(root, reference)
        except (OSError, ValueError):
            unchanged = False
    try:
        evaluation = json.loads(stdout, parse_constant=_reject_nonfinite)
        if not isinstance(evaluation, dict):
            evaluation = {}
    except ValueError:
        evaluation = {}
    try:
        protected_unchanged = protected_snapshot(root) == protected_before
    except (OSError, ValueError, TypeError):
        protected_unchanged = False
    outcome = evaluation.get("outcome", "inconclusive")
    if outcome not in {"passed", "failed", "inconclusive"} or code != 0 or timed_out or not unchanged or not protected_unchanged:
        outcome = "inconclusive"
    result = {"schema_version": "1.0", "status": "evidence_only", "plan": plan_ref,
              "candidate": plan["candidate"], "kind": plan["kind"], "scope": plan["scope"],
              "outcome": outcome, "execution": {"command": command, "exit_code": code,
              "elapsed_seconds": time.monotonic() - started, "timed_out": timed_out,
              "runner_version": "Python " + sys.version.split()[0]}, "evaluation": evaluation,
              "stdout": stdout, "stderr": stderr, "inputs_unchanged": unchanged, "protected_files_unchanged": protected_unchanged}
    # Exclusive creation also protects against an evaluator writing the output first.
    serialized = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    destination = output_path(root, output)
    with destination.open("x", encoding="utf-8") as handle:
        handle.write(serialized)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run", action="store_true", help="execute this already-authorized trusted plan once, without a shell")
    parser.add_argument("--output", help="fresh root-relative JSON result path, required for --run")
    args = parser.parse_args()
    if args.run and not args.output:
        parser.error("--run needs --output")
    try:
        if args.run:
            result = execute(args.plan, args.root, args.output)
            print(json.dumps({"outcome": result["outcome"], "output": args.output,
                              "scope": result["scope"], "protected_files_unchanged": result["protected_files_unchanged"]}, ensure_ascii=False))
            return 0 if result["outcome"] == "passed" else 1
        errors = inspect_plan(json.loads(args.plan.read_text()), args.root)
        for message in errors:
            print("[ERROR] " + message)
        if not errors:
            print("Frozen plan and input hashes match. No command executed; use --run only within approved scope.")
        return bool(errors)
    except (OSError, ValueError, TypeError) as exc:
        print("[ERROR] " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
