# Machine state model

`research/machine/project-state.json` is a machine-readable mirror of the
human-approved state. It does not outrank `STATE.md` or
`research/proof_ledger.md` in kernel 3.1.

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

## Historical single-window sessions (kernel 3.0, unchanged)

Manifest v1.2 needs a frozen brief, optional indexed evidence, a summary link
(which may be work.md itself), route signal, and declared key-review requirement.
It has no mandatory role registry or orchestration. An ordinary session needs
only brief.md, work.md, and manifest.json. No transition exists until a formal
change is proposed. Txxx.json is for submitted durable evidence, not every step.

A critical review has separate hashed question, independent baseline, candidate,
and comparison artifacts. It records baseline-before-disclosure, reviewer/context,
derivation roots and overlap, and verdict. Independence is an auditable declared
process, not something a schema proves. Self-check never clears the independent
gate; decisive support and formal claim/manuscript changes require a surviving
independent review tied to the exact final work artifact. Owner approval remains
a separate gate; a review verdict never promotes canonical state.

Historical manifests, tasks, and role registries are checked when present but
are not rewritten. No project-state schema migration is needed for the new
execution model. Optional reports are generated views, not additional authority.

For v1.2 formal transition proposals, evidence_records contains local Txxx IDs
indexed by the manifest's hashed task_records. Each cited record names the exact
reviewed final work and nonempty derivation roots. Pending or unindexed evidence
cannot support a promotion. Explicit provisional planning entries may use status
(e.g. open) or after.status without triggering a proof audit; canonical changes
still require owner approval. Unknown change forms are reviewed conservatively.
Historical role-registry diagnostics are warnings, never research prerequisites.

## Feedback sessions (kernel 3.1)

New manifests use 1.3. Three ordinary files remain sufficient; meaning_audit and
progress record correspondence and information gained, with conditional arrays
claim_records, critical_reviews, checks and compute_steps. No canonical claim
status semantics change; project-state schema remains 2.1.

claim-evidence 1.0 freezes a provisional claim ID/revision, target reference,
statement, quantifiers, domain/topology, hypotheses, excluded weakenings, source
comparison, meaning/novelty standing, proof hash, roots and versioned prerequisite
references. Review 1.1 binds both that record and its exact proof, not summary.
A changed statement needs new review even when proof bytes are identical.
Substantive supersedes links make transitive old-version dependents pending
recheck for future formal use. Canonical status is never silently changed.

Formal transition evidence remains local Txxx IDs in the manifest index, with
proof_items covering changed claim IDs and artifacts equal to their reviewed
proof snapshots. Unrelated reviews cannot cover another claim. Open planning
entries retain the lighter approval-only path.

check-result references its frozen plan and candidate, with scope, raw output,
actual exit/time/timeout and integrity. Metadata cannot certify checker truth.
compute_steps record bounded intentions/observations; only local check timeouts
are enforced automatically. Unknown costs remain null.

progress is a declared mathematical delta, not a similarity/novelty oracle. Two
consecutive none entries trigger route review earlier than the existing three-
session limit. Human approval and fresh primary literature remain mandatory
for the post-review route decision. No old run or review is rewritten.
