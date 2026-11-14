#!/usr/bin/env python3
"""Prepare frozen task comparisons and blind reviews; never call models or grade proofs."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import random
import re
import shutil
import sys
from typing import Any

import checkctl
import evidencectl


def number(value: Any, *, positive: bool = False) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and (value > 0 if positive else value >= 0)


def save(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")


def load_suite(reference: dict, root: Path) -> dict:
    suite = json.loads(checkctl.read_reference(root, reference).read_text())
    if not isinstance(suite, dict):
        raise ValueError("suite must be an object")
    if suite.get("schema_version") != "1.0" or suite.get("purpose") not in {"real_tasks", "mechanics_only"}:
        raise ValueError("expected a version 1.0 suite with an explicit evidence purpose")
    if not isinstance(suite.get("suite_id"), str) or not suite["suite_id"].strip():
        raise ValueError("suite_id is required")
    if suite.get("comparison") not in {"matched_budget", "exploratory"}:
        raise ValueError("declare matched_budget or exploratory comparison")
    if suite.get("factor") not in {"workflow", "model", "reasoning_effort", "exploratory"}:
        raise ValueError("declare the comparison factor")
    budget = suite.get("budget", {})
    if not isinstance(budget, dict):
        raise ValueError("budget must be an object")
    if not number(budget.get("max_seconds"), positive=True) or (budget.get("max_cost_usd") is not None and not number(budget["max_cost_usd"])):
        raise ValueError("declare a finite positive time budget and optional nonnegative USD budget")
    cases, configurations = suite.get("cases"), suite.get("configurations")
    if not isinstance(cases, list) or not cases or not isinstance(configurations, list) or len(configurations) < 2:
        raise ValueError("a comparison needs cases and at least two configurations")
    for collection in (cases, configurations):
        ids = []
        for item in collection:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not re.fullmatch(r"[A-Za-z0-9_-]+", item["id"]):
                raise ValueError("case/configuration IDs must be simple unique names")
            ids.append(item["id"])
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate case/configuration ID")
    for config in configurations:
        for field in ("model", "reasoning_effort", "workflow"):
            if not isinstance(config.get(field), str) or not config[field].strip():
                raise ValueError("configuration needs model, reasoning_effort, and workflow")
        configured_budget = config.get("budget", budget)
        if not isinstance(configured_budget, dict) or not number(configured_budget.get("max_seconds"), positive=True) or (configured_budget.get("max_cost_usd") is not None and not number(configured_budget["max_cost_usd"])):
            raise ValueError("invalid configuration budget")
        if suite["comparison"] == "matched_budget" and configured_budget != budget:
            raise ValueError("matched-budget configurations must share the same declared budget")
    held_fixed = {"workflow": ("model", "reasoning_effort"), "model": ("workflow", "reasoning_effort"),
                  "reasoning_effort": ("model", "workflow"), "exploratory": ()}[suite["factor"]]
    if held_fixed and len({tuple(item[field] for field in held_fixed) for item in configurations}) != 1:
        raise ValueError("hold other configuration factors fixed for an attributable comparison")
    for case in cases:
        if case.get("expected_disposition") not in {"accepted", "rejected", "conditional", "open"}:
            raise ValueError("case needs an owner-reviewed expected disposition")
        if not isinstance(case.get("category"), str) or not case["category"].strip() or not isinstance(case.get("context", []), list):
            raise ValueError("case needs a category and context list")
        for reference in [case["question"], case["reference"], *case.get("context", [])]:
            checkctl.read_reference(root, reference)
        if any(reference["sha256"] == case["reference"]["sha256"] for reference in [case["question"], *case.get("context", [])]):
            raise ValueError("hidden reference content must not be included in runner inputs")
    return suite


def _fresh_directory(root: Path, relative: str) -> Path:
    # The same output guard as the check runner refuses traversal, links and replacement.
    path = checkctl.output_path(root, relative)
    path.mkdir()
    return path


def prepare(reference: dict, root: Path, output: str) -> Path:
    suite = load_suite(reference, root)
    destination = _fresh_directory(root, output)
    try:
        for config in suite["configurations"]:
            for index, case in enumerate(suite["cases"], 1):
                packet = destination / "inputs" / config["id"] / f"case-{index:03d}"
                packet.mkdir(parents=True)
                question = checkctl.read_reference(root, case["question"])
                (packet / "question.md").write_bytes(question.read_bytes())
                contexts = []
                for n, context in enumerate(case.get("context", []), 1):
                    name = f"context-{n:03d}.md"
                    (packet / name).write_bytes(checkctl.read_reference(root, context).read_bytes())
                    contexts.append(evidencectl.file_ref(packet, name))
                save(packet / "task.json", {"case_id": case["id"], "configuration": config,
                     "budget": config.get("budget", suite["budget"]),
                     "question": evidencectl.file_ref(packet, "question.md"), "context": contexts})
        owner = destination / "owner"
        owner.mkdir()
        save(owner / "suite.json", suite)
        save(owner / "source.json", {"suite": reference, "note": "Give a runner only its input packet. References and expected outcomes are for graders; filesystem isolation must be supplied by the host."})
    except Exception:
        shutil.rmtree(destination)
        raise
    return destination


def submissions(reference: dict, root: Path) -> tuple[dict, dict]:
    value = json.loads(checkctl.read_reference(root, reference).read_text())
    if not isinstance(value, dict) or not isinstance(value.get("submissions"), list):
        raise ValueError("submission record needs a submissions array")
    suite = load_suite(value["suite"], root)
    expected = {(case["id"], config["id"]) for case in suite["cases"] for config in suite["configurations"]}
    seen = set()
    for entry in value.get("submissions", []):
        if not isinstance(entry, dict):
            raise ValueError("submission must be an object")
        pair = entry["case_id"], entry["configuration_id"]
        if pair not in expected or pair in seen:
            raise ValueError("unknown or duplicate submission pair")
        seen.add(pair)
        if entry.get("disposition") not in {"accepted", "rejected", "conditional", "open", "abstain"}:
            raise ValueError("invalid submission disposition")
        checkctl.read_reference(root, entry["answer"])
        usage = entry.get("usage", {})
        if not isinstance(usage, dict):
            raise ValueError("usage must be an object")
        if not number(usage.get("wall_seconds")) or (usage.get("cost_usd") is not None and not number(usage["cost_usd"])):
            raise ValueError("record measured wall_seconds; unknown USD cost is null, never zero-imputed")
    if seen != expected:
        raise ValueError("incomplete comparison: include every case/configuration, including explicit abstentions")
    return value, suite


def blind(reference: dict, root: Path, output: str, seed: int | None = None) -> Path:
    value, suite = submissions(reference, root)
    cases = {case["id"]: case for case in suite["cases"]}
    entries = list(value["submissions"])
    (random.SystemRandom() if seed is None else random.Random(seed)).shuffle(entries)
    destination = _fresh_directory(root, output)
    try:
        review = destination / "review"
        owner = destination / "owner"
        review.mkdir()
        owner.mkdir()
        answers, keys, grades = [], [], []
        for index, entry in enumerate(entries, 1):
            anonymous_id = f"answer-{index:04d}"
            case = cases[entry["case_id"]]
            answers.append({"id": anonymous_id, "question": checkctl.read_reference(root, case["question"]).read_text(),
                            "context": [checkctl.read_reference(root, item).read_text() for item in case.get("context", [])],
                            "answer": checkctl.read_reference(root, entry["answer"]).read_text()})
            keys.append({"id": anonymous_id, "case_id": entry["case_id"], "configuration_id": entry["configuration_id"]})
            grades.append({"id": anonymous_id, "correctness": None, "exposition": None, "attribution": None,
                           "meaning_matched": None, "gap_closed": None, "reproducible": None, "review_minutes": None})
        save(review / "answers.json", answers)
        save(review / "grades-template.json", grades)
        save(owner / "key.json", {"schema_version": "1.0", "submissions": reference, "mapping": keys})
    except Exception:
        shutil.rmtree(destination)
        raise
    return destination


def score(key: dict, grades: list, root: Path) -> dict:
    if not isinstance(key, dict) or not isinstance(key.get("mapping"), list) or not all(isinstance(item, dict) for item in key["mapping"]):
        raise ValueError("blind key needs a mapping array")
    value, suite = submissions(key["submissions"], root)
    entries = {(item["case_id"], item["configuration_id"]): item for item in value["submissions"]}
    mappings = {item["id"]: (item["case_id"], item["configuration_id"]) for item in key["mapping"]}
    if len(mappings) != len(entries) or set(mappings.values()) != set(entries):
        raise ValueError("blind key must map every submission exactly once")
    if not isinstance(grades, list) or len(grades) != len(entries) or {item.get("id") for item in grades if isinstance(item, dict)} != set(mappings):
        raise ValueError("every blinded answer needs one independent grade")
    cases = {case["id"]: case for case in suite["cases"]}
    configurations = {config["id"]: config for config in suite["configurations"]}
    totals = {config: {"cases": 0, "fully_correct": 0, "verified_gap_closures": 0, "false_accepts": 0, "meaning_mismatches": 0, "reference_disagreements": 0,
             "exposition_total": 0, "attribution_total": 0, "reproducible": 0, "wall_seconds": 0,
             "known_cost_usd": 0, "unknown_cost_cases": 0, "review_minutes": 0, "budget_overruns": 0} for config in configurations}
    for grade in grades:
        if any(type(grade.get(field)) is not int or grade[field] not in {0, 1, 2} for field in ("correctness", "exposition", "attribution")):
            raise ValueError("correctness, exposition and attribution require human grades 0, 1 or 2")
        if any(type(grade.get(field)) is not bool for field in ("meaning_matched", "gap_closed", "reproducible")) or not number(grade.get("review_minutes")):
            raise ValueError("record target correspondence, reproducibility and measured review minutes")
        if grade["gap_closed"] and (grade["correctness"] != 2 or not grade["meaning_matched"]):
            raise ValueError("a verified gap closure needs a fully correct answer to the intended question")
        case_id, config_id = mappings[grade["id"]]
        entry, total = entries[(case_id, config_id)], totals[config_id]
        total["cases"] += 1
        total["fully_correct"] += int(grade["correctness"] == 2 and grade["meaning_matched"])
        total["verified_gap_closures"] += int(grade["gap_closed"])
        total["false_accepts"] += int(entry["disposition"] == "accepted" and (grade["correctness"] < 2 or not grade["meaning_matched"] or cases[case_id]["expected_disposition"] == "rejected"))
        total["meaning_mismatches"] += int(not grade["meaning_matched"])
        total["reference_disagreements"] += int(entry["disposition"] != cases[case_id]["expected_disposition"])
        total["exposition_total"] += grade["exposition"]
        total["attribution_total"] += grade["attribution"]
        total["reproducible"] += int(grade["reproducible"])
        usage = entry["usage"]
        total["wall_seconds"] += usage["wall_seconds"]
        total["review_minutes"] += grade["review_minutes"]
        if usage.get("cost_usd") is None:
            total["unknown_cost_cases"] += 1
        else:
            total["known_cost_usd"] += usage["cost_usd"]
        budget = configurations[config_id].get("budget", suite["budget"])
        total["budget_overruns"] += int(usage["wall_seconds"] > budget["max_seconds"] or (usage.get("cost_usd") is not None and budget.get("max_cost_usd") is not None and usage["cost_usd"] > budget["max_cost_usd"]))
    return {"suite_id": suite["suite_id"], "purpose": suite["purpose"], "comparison": suite["comparison"],
            "configurations": totals, "grading": "Human judgments, not automated mathematical certification.",
            "limitation": "Mechanics-only examples do not measure research productivity. No claim of training-data independence; report task provenance and all failures."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "blind", "score"))
    parser.add_argument("record", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", help="fresh root-relative packet directory")
    parser.add_argument("--grades", type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        reference = evidencectl.file_ref(root, checkctl.relative_path(args.root, args.record))
        if args.command == "score":
            if args.grades is None:
                parser.error("score requires --grades")
            print(json.dumps(score(json.loads(checkctl.read_reference(root, reference).read_text()), json.loads(args.grades.read_text()), root), indent=2))
        else:
            if not args.output_dir:
                parser.error("prepare/blind requires --output-dir")
            print((prepare if args.command == "prepare" else blind)(reference, root, args.output_dir))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print("[ERROR] " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
