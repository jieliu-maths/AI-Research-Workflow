# Executable candidate checks (teaching example)

From the source or installed project root, choose a fresh output directory:

```bash
python3 examples/ai4math/checks/make_plan.py --output-dir calculations/check-demo
python3 tools/checkctl.py calculations/check-demo/polynomial-plan.json
python3 tools/checkctl.py calculations/check-demo/polynomial-plan.json --run --output calculations/check-demo/polynomial-result.json
python3 tools/checkctl.py calculations/check-demo/scale-plan.json --run --output calculations/check-demo/scale-result.json
```

The polynomial check passes by exact rational coefficient comparison. The scale
check fails: the ratio of the specified monomials is unbounded as the parameter
tends to zero. That failure does not exclude a broader proof route or certify
anything about general nonlinear terms. A failed check returns CLI exit code 1
while preserving its result; inspection alone never executes a command.

The evaluator is a small standard-library example, not a CAS, Lean checker, or
certified analytic library. Keep candidate/evaluator inputs frozen and review
checker correctness separately. Raw execution metadata is not proof by itself.
