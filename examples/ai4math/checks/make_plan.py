#!/usr/bin/env python3
"""Prepare two frozen teaching-check plans; never executes them."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import checkctl
import evidencectl

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output-dir", required=True, help="fresh project-relative directory")
args = parser.parse_args()
directory = checkctl.output_path(ROOT, args.output_dir)
directory.mkdir()
for name, kind, candidate, scope in (
    ("polynomial", "symbolic", "polynomial.json", "Exact equality of two supplied rational-coefficient polynomials"),
    ("scale", "scale", "scale-failure.json", "Bounded ratio for specified positive monomials as epsilon tends to zero"),
):
    plan = {"schema_version": "1.0", "kind": kind, "scope": scope,
            "candidate": evidencectl.file_ref(ROOT, "examples/ai4math/checks/" + candidate),
            "evaluator": evidencectl.file_ref(ROOT, "examples/ai4math/checks/evaluator.py"),
            "inputs": [], "command": ["{python}", "{evaluator}", "{candidate}"],
            "timeout_seconds": 10, "evaluator_review": "Teaching implementation; independently audit before mathematical reliance",
            "limitations": ["Checks only the exact supplied algebra or monomials; not a PDE or universal analytic proof"]}
    (directory / (name + "-plan.json")).write_text(json.dumps(plan, indent=2) + "\n")
print(directory)
