# Frozen-task comparison mechanics

This four-case teaching suite exercises exact algebra, quantifier drift, source
applicability and scoped failure. It is **not** a study of research productivity,
model performance or private historical research tasks.

```bash
python3 tools/benchctl.py prepare examples/benchmark/suite.json --output-dir evaluation/teaching-packets
```

Only inputs/configuration/case packets go to runners. Keep owner/ and the source
references out of their accessible context. The tool makes no model calls.
After recording all eight answers/abstentions and actual known time/cost, use
benchctl blind and score as described in [the guide](../../docs/research-feedback.md).
A comparison of real workflows needs owner-provided representative historical
tasks and independent human grading. Change only the declared comparison factor.
