# Machine state model

`research/machine/project-state.json` is a machine-readable mirror of the
human-approved state. It does not outrank `STATE.md` or
`research/proof_ledger.md` in kernel 2.1.

## Separate axes

- `claim.status` is epistemic. In particular, `formal` is not
  `formal_exact`, `conjectural` is unresolved, and `established` is a
  scope-specific resolved status. Migration preserves these words rather than
  normalizing them.
- `route.canonical_status` records the human-approved route state.
- `route.operational_status` records what the run artifacts currently show.
  These may differ while a state proposal awaits approval.
- `scope` states exactly which method class an obstruction covers.
- `route.id` uses `route:<slug>` and names a mathematical method.
- `run.id` uses `R<number>` and names one execution. `run.route_id` records the
  optional many-runs-to-one-route relationship. `snapshot.active_route` and
  `snapshot.active_run` are independent fields.

## Dependencies and blockers

`claim.depends_on` is the sole machine source for logically necessary
prerequisites. Proof-map edges instead use `supports`, `tests`, `blocks`, `surveys`, or
`warns_circularity`. Once `snapshot.theorem_targets` is human-reviewed, the
validator derives `blocking` as unresolved claims in the strict dependency
closure. Without mapped theorem targets it warns instead of guessing.

## Evidence lineage

Use `derivation_roots` for the identities, source results, conserved
quantities, computations, or formal certificates from which an evidence item
descends. Two artifacts produced by different agents are not independent when
their decisive derivation roots coincide.

## State transitions

Agents may append evidence and prepare a transition proposal. Only an explicit
human approval authorizes updating canonical state or refreshing canonical
hashes. A validator success means the records are structurally consistent; it
does not mean that a mathematical statement is true.

## Run sidecars

- `runs/<run>/manifest.json` records run identity, state input, route approval,
  task-record hashes, and closing artifacts.
- `runs/<run>/Txxx.json` records evidence class, derivation roots, claimed
  independence, and the frozen dispatch/artifact hashes.
- `runs/<run>/state-transition.json` is a machine-checkable proposal. Its
  `proposal_only`, `owner_approved`, and `applied` statuses are distinct.

`project-state.proposal.json` has its own schema and an explicit
`unresolved_mappings` ledger. Its dashboard is rendered separately as
`dashboard/proposal-preview.html` with a non-canonical warning.
