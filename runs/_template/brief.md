# Run brief

```yaml
template_version: 2.4.0
run_id: Rxxx
route_id: route:slug | none
state_in: Sx
task_ids: []
ledger_items: []
theorem_targets: []
machine_record: runs/Rxxx/manifest.json
orchestration_record: runs/Rxxx/orchestration.json
route_approval_reference: proposal-only | exact owner approval reference
```

`run_id` identifies an execution. `route_id` identifies the mathematical
method being tested; the two namespaces must never be reused for one another.
`proposal-only` permits comparison, source research, feasibility checks, and
falsification, but not route activation or construction work.

## Exact mathematical question

## Mathematical state entering the run

Explain `state_in` in ordinary mathematical language.

## Approved route and approval scope

## Allowed inputs and assumptions

## Forbidden shortcuts

## Tasks and evidence plan

| Task | Mathematical decision | Evidence class | Derivation roots | Independence claim | Machine record |
| --- | --- | --- | --- | --- | --- |
| Txxx |  |  |  | none | `runs/Rxxx/Txxx.json` |

## Candidate preflight plan

For every new functional, coordinate, multiplier, correction, norm, or
localization law, record before the long derivation:

| Candidate class | Canonical topology | Exact operator/adjoint test | Required scale | Quotient dependencies | Stress and blind-direction tests | Localization ledger | Symbol scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exact formula or parameterized class | approved norm/space | dimension, boundary, commutator | uniform downstream margin | complete existing covectors | both signs; remote/low-frequency/concentrating/symmetry tests | cutoff speed; annulus; exterior; boundary; tail | existing or explicitly local |

State which cheap test can stop the candidate before a full construction. A
repairable formula error creates a separate repaired candidate; it does not
erase the raw calculation.

## Dependency and blocker semantics

List only logically necessary prerequisites in claim `depends_on`. Record
heuristic support, tests, scoped obstructions, and circularity warnings as
typed proof-map edges. A `blocking` flag means an unresolved strict prerequisite
of an explicitly owner-reviewed `theorem_targets` entry; it is not a synonym
for “important” or “currently being studied.”

## Success, failure, and stop conditions

## Owner gates

## Required closing artifacts

- `status.md`
- `amendments.md`
- role artifacts and any `resolution-Txxx.md`
- `director-run-summary.md`
- `learning-note-Txxx.md`
- `state_update_proposal.md`
- `state-transition.json`
- `orchestration.json`
- `route-review.md` and `route-review.json` when the review trigger is met
