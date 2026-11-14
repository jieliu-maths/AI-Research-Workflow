#!/usr/bin/env python3
"""Exact teaching checks only: polynomial identity or a monomial scale condition."""
import json
from fractions import Fraction
from pathlib import Path
import sys

candidate = json.loads(Path(sys.argv[1]).read_text())
if candidate["check"] == "polynomial_identity":
    # Equality of coefficient vectors is exact over the rational numbers.
    left, right = ([Fraction(str(x)) for x in candidate[key]] for key in ("left", "right"))
    length = max(len(left), len(right))
    left += [Fraction(0)] * (length - len(left))
    right += [Fraction(0)] * (length - len(right))
    differences = [str(a - b) for a, b in zip(left, right)]
    passed = left == right
    result = {"outcome": "passed" if passed else "failed", "coefficient_difference": differences,
              "scope": "Only the supplied rational coefficient polynomials; no PDE statement is certified."}
elif candidate["check"] == "monomial_scale":
    # For 0 < epsilon <= 1, epsilon^a <= C epsilon^b uniformly as epsilon -> 0
    # has a bounded ratio exactly when a >= b, assuming fixed positive constants.
    actual, required = (Fraction(str(candidate[key])) for key in ("actual_exponent", "required_exponent"))
    result = {"outcome": "passed" if actual >= required else "failed", "ratio_exponent": str(actual - required),
              "scope": "Necessary scale comparison for the specified positive monomials, not a nonlinear estimate."}
else:
    raise ValueError("unknown teaching check")
print(json.dumps(result))
