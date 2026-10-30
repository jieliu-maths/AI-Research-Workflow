#!/usr/bin/env python3
"""Offline teaching example: a bounded arithmetic check is not a universal proof."""

import argparse
import json
from pathlib import Path
import platform
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from evidencectl import file_ref, inspect


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    root = args.output_dir
    # Include the exact executed source, not a mutable path outside the bundle.
    (root / "verify.py").write_bytes(Path(__file__).read_bytes())
    results = [{"n": n, "sum": sum(2 * k + 1 for k in range(n)), "square": n * n}
               for n in range(100)]
    assert all(row["sum"] == row["square"] for row in results)
    (root / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    record = {
        "schema_version": "1.0", "status": "evidence_only", "kind": "finite_check",
        "statement": "The sum of the first n odd positive integers equals n squared for each integer n in [0,99].",
        "scope": "Exactly 100 cases with Python integer arithmetic; no quantification beyond n=99.",
        "derivation_roots": ["enumeration of integers n=0,...,99", "Python integer arithmetic"],
        "files": [file_ref(root, name) for name in ("verify.py", "results.json")],
        "execution": {"command": ["python3", "examples/ai4math/verify.py", "--output-dir", "OUTPUT_DIR"],
                      "tool_version": "Python " + platform.python_version(), "exit_code": 0},
        "outcome": "passed",
        "limitations": ["The universal identity still requires a proof, for example induction.",
                        "This checker and its outputs are not a Lean certificate."],
        "review_required": ["Audit the code and bounded scope; an owner decides any ledger promotion."],
    }
    (root / "evidence.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    errors = inspect(record, root)
    if errors:
        raise ValueError(errors)
    print("100 exact finite cases passed. Universal theorem remains unproved by this computation.")
    print("Teaching fixture only: no canonical research state was changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
