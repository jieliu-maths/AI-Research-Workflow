#!/usr/bin/env python3
"""Offline synthetic experiment with model selection and one held-out evaluation."""

import argparse
import json
from pathlib import Path
import platform
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from evidencectl import file_ref, inspect


def dataset(seed: int, count: int) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    return [(x := rng.uniform(-1, 1), 2 * x + 1 + rng.gauss(0, .1)) for _ in range(count)]


def mse(data: list[tuple[float, float]], slope: float, intercept: float) -> float:
    return sum((slope * x + intercept - y) ** 2 for x, y in data) / len(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.output_dir
    root.mkdir(parents=True, exist_ok=False)
    (root / "experiment.py").write_bytes(Path(__file__).read_bytes())
    train, validation = dataset(11, 100), dataset(22, 40)
    mean_x = sum(x for x, _ in train) / len(train)
    mean_y = sum(y for _, y in train) / len(train)
    slope = sum((x - mean_x) * (y - mean_y) for x, y in train) / sum((x - mean_x) ** 2 for x, _ in train)
    candidates = {"constant": (0.0, mean_y), "linear": (slope, mean_y - slope * mean_x)}
    scores = {name: mse(validation, *model) for name, model in candidates.items()}
    selected = min(scores, key=scores.get)
    # Test data is generated and evaluated only after the selection is frozen.
    test = dataset(33, 40)
    result = {"data": "synthetic y=2*x+1+Gaussian(0,0.1)",
              "seeds": {"train": 11, "validation": 22, "test": 33},
              "sample_counts": {"train": 100, "validation": 40, "test": 40},
              "models": candidates, "validation_mse": scores, "selected_model": selected,
              "held_out_mse": mse(test, *candidates[selected]),
              "test_accesses": 1,
              "scope": "One synthetic split. No real-world, causal, or statistical-significance claim."}
    (root / "data.json").write_text(json.dumps({"train": train, "validation": validation, "test": test}, indent=2) + "\n", encoding="utf-8")
    (root / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    record = {
        "schema_version": "1.0", "status": "evidence_only", "kind": "numerical_experiment",
        "statement": "Compare constant and linear predictors on a specified synthetic regression task.",
        "scope": result["scope"],
        "derivation_roots": ["specified synthetic data generator", "ordinary least squares", "seeds 11,22,33"],
        "files": [file_ref(root, name) for name in ("experiment.py", "data.json", "results.json")],
        "execution": {"command": ["python3", "examples/ai4s/experiment.py", "--output-dir", "OUTPUT_DIR"],
                      "tool_version": "Python " + platform.python_version(), "exit_code": 0},
        "outcome": "passed",
        "limitations": ["Single synthetic split; repeat with predeclared independent seeds before robustness claims.",
                        "Floating-point results may vary slightly across runtimes; no analytic proof is produced."],
        "review_required": ["Audit data separation, selection rule, baselines, and scope before accepting any conclusion."],
    }
    (root / "evidence.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    errors = inspect(record, root)
    if errors:
        raise ValueError(errors)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
