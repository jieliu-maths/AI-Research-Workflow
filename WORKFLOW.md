# Mathematical research workflow

Default: one research window, light records, independent review at key evidence gates.

<!-- research-workflow:block project-inception start -->
## Start a project

Use the current chat as the main research window; no role tasks, titles, or
workspace registry are required. Record the owner's question, constraints,
known sources, and open choices. Search primary sources and compare genuinely
different mechanisms with their cheapest discriminating tests. The number and
length of notes should fit the question, not a fixed document quota.

Obtain approval of the exact target, main route, assumptions, and exploration
scope before construction. Drafts and cheap feasibility or falsification checks
may inform this decision, but never activate an unapproved main route.
Initialize an empty S0 record without importing another project's mathematics.
<!-- research-workflow:block project-inception end -->

<!-- research-workflow:block owner-gates start -->
## Owner approval and evidence

Only explicit human approval changes canonical mathematical conclusions, claim
status, the theorem target, main route, hypotheses, global notation, or manuscript.
The owner may approve a bounded exploration scope once. Local candidates,
computations, repairs, and source checks inside that scope need no repeated
permission. Selecting or materially changing the main mechanism, narrowing the
theorem, or exceeding the approved scope requires a new owner decision.

Exploration records are provisional. Distinguish exact, formal, formal_exact,
conditional, conjectural, numerical, external, and rejected statements. A passed
validator, model consensus, or independent critique does not establish a theorem.
Preserve exact hypotheses, quantifiers, dependencies, derivation roots, failure
scope, and original evidence. Formal certificates still need an audited mapping
to the informal statement. Manuscript edits require explicit authorization and
the supporting evidence gate. Independent review is required for a key identity,
core estimate, claimed proof-gap closure, or promotion of a formal conclusion.
If review is unavailable, continue unrelated authorized exploration but leave
that conclusion pending; never substitute self-review for independent evidence.
<!-- research-workflow:block owner-gates end -->

<!-- research-workflow:block peer-role-tasks start -->
## Single-window execution

The main window owns continuous reasoning, local calculations, source checks,
repairs, and reporting. Director/Researcher/Planner are optional names for
activities, not required agents. Do not create or rename chats, maintain a role
registry, or wait for peer-role readiness as a prerequisite to research.

Independent review is an on-demand activity in a fresh, appropriately isolated
context or by a human reviewer. An existing separate chat can be used when
available; creating a new chat requires the user's explicit request. Delegation
is optional and subject to host permissions. A copied conversation, a new role
name, or the same reasoning roots do not establish independence.
<!-- research-workflow:block peer-role-tasks end -->

<!-- research-workflow:block director-return-loop start -->
## One bounded research session

Read `STATE.md` first: it is the short approved-state entry point, containing
target, assumptions, established results and evidence links, failed candidate
scopes, smallest open gap, active session, and next test. Then read the charter,
relevant proof-ledger rows, notation, and active brief as needed. Do not load all
history by default. Start by running `python3 tools/researchctl.py validate`.

If later work lives outside the approved records, use the optional
`research/current-work.md` as a navigation note. Show the approved state
version separately from each working series and exact source version. Link
the latest applicable review, its coverage and status, the question to resume,
and any mismatch with STATE or a series index. Verify paths before reuse. A
newer draft can be read or audited inside the authorized scope. Any change to
approved mathematics still needs a separate proposal and owner decision.

Keep one active mathematical question. A session needs only `brief.md` (question,
approved scope, assumptions, cheapest test, stop condition), `work.md` (continuous
provisional derivation and final mathematical summary), and `manifest.json`
(index, frozen references, evidence and route signal). Use the v1.3 manifest;
`summary` may reference `work.md` itself. No orchestration, per-role dispatch,
status, learning-note, or duplicate summary is required. Do not copy the whole
template directory: review and transition templates are conditional.

Within the approved scope, append local candidates, cheap preflight checks,
computations, sources, and scoped failures to `work.md`. Use `Txxx.json` only
when indexing durable evidence for review or a state proposal; its `dispatch`
may reference the session brief, and its artifact may reference `work.md`.
Freeze the submitted statement/proof version when key evidence is sent for
review. Keep work.md appendable and link that version; a new discussion or
summary does not revise the proof. Preserve earlier submitted evidence bytes.

At a stop condition, summarize the exact result or scoped obstruction, proof
consequence, remaining gap, and next mathematical question in `work.md` and the
owner response. Close a session without a state proposal when no formal change
is sought. Do not auto-open a later session beyond the owner's approved scope.
Validate after freezing evidence, before a proposal, and after approved sync.
<!-- research-workflow:block director-return-loop end -->

## Meaning and prior-work check before a long derivation

In the existing brief, state exactly what answers the question: quantifiers,
parameter/dimension range, function space, uniformity, and allowed hypotheses.
Name easier or narrower assertions that do not count. Match every imported
source theorem to its exact location and assumptions; say what remains beyond
it. Distinguish correctness, applicability, and novelty. A known consequence may
be useful without being new. Record the conclusion in manifest.meaning_audit;
only the owner approves changes to the target, hypotheses, or main route.

Use the following details in the existing brief or work note when relevant:

- For an identity or estimate, name the exact functional or quantity, time
  variable, differentiated pieces, terms to retain, and target inequality.
  Compare decisive cancellations with known derivations before crediting a
  second mechanism.
- For a change of coordinates, name what is held fixed, give the composition
  map, and check the regularity, domain and uniformity needed by that map. For
  tangential analyticity, bound the induced complex normal displacement in the
  available complex domain. Record exactly the estimate, model or candidate
  class excluded by a failed test.
- For a load-bearing source, record what was actually read, the exact theorem
  or proof location, its applicable hypotheses, the step it supplies, and the
  remaining mismatch. Record a later analogy separately from the source or
  mathematical obstacle that motivated the original construction.

## Computation proportional to the question

Use the owner's current model/settings by default. Before increasing reasoning,
changing model, comparing independent candidates, or invoking an external
verifier, record a short compute_steps entry only when such escalation is used:
why, expected new information, time/optional USD limit, and stop condition.
Stay within existing permissions; do not silently override saved settings or
create chats. Record observed time, actual known cost (unknown is null), and
outcome. Escalation is a testable choice, not evidence of correctness. Budget
metadata alone does not enforce model usage or billing; checkctl enforces only
its local subprocess timeout. A completed step that overruns must be marked
stopped rather than called a successful in-budget run.

<!-- research-workflow:block candidate-preflight start -->
### Candidate preflight before long derivations

Before investing in a new functional, coordinate, multiplier, correction,
bootstrap norm, or localization law, perform the cheapest decisive tests on
the explicit candidate as written:

1. **Canonical topology.** State the approved function space and norm. Prove
   the candidate is defined and continuous there. A comparison with a newly
   introduced stronger norm does not establish continuity in the project
   topology. Test remote, low-frequency, concentrating, and symmetry-generated
   sequences when relevant.
2. **Exact operator calculus.** Recompute adjoints, commutators, integration by
   parts, boundary terms, and dimension-dependent constants from the current
   equations. Do not inherit an identity from another dimension, convention,
   or cutoff geometry without derivation.
3. **Linearized scale and units.** Compute the first nonzero variation at the
   reference solution before estimating nonlinear errors. Compare its size to
   the exact margin required downstream, uniformly in every small or large
   parameter. If renormalization repairs the derivative scale, retest endpoint
   continuity and differentiate the normalization itself.
4. **Independence quotient.** Subtract the complete tangent covectors of every
   conserved, modulation, orthogonality, or virial identity declared as an
   existing derivation root. Agreement on one test direction does not prove
   independence, and a small quotient upper bound does not prove exact
   dependence.
5. **Quantifier and blind-direction tests.** Test every side required by the
   theorem, special solutions, admissible radiation, far-field packets, and
   limiting parameter regimes. A sectorwise sign mechanism also needs a
   coverage argument for the transition set.
6. **Localization ledger.** Display cutoff velocity, annular commutators,
   physical and rescaled radii, exterior bulk, primitive boundary terms, and
   tail quantities. Profile decay alone cannot control arbitrary radiation in
   an open energy neighborhood.
7. **Scope of failure.** Distinguish the formula as written, a locally repaired
   formula, the precisely parameterized candidate class, and untested
   alternatives. A counterexample to one candidate is not a route-level
   impossibility theorem.

The run brief states which of these tests apply and places them before the
full construction task whenever they can decide the candidate more cheaply.
Symbols introduced for a preflight remain local unless the owner separately
approves a global notation change.
<!-- research-workflow:block candidate-preflight end -->

## Executable candidate checks

Prefer a reusable exact check when it can decide a sign, coefficient, scale,
finite construction, or counterexample. Freeze a check plan with candidate,
evaluator, and input hashes; separate candidate generation from evaluator
maintenance, review the evaluator, and include adversarial or withheld cases.
Within approved scope use tools/checkctl.py to inspect the plan, and --run with
--output to execute it once without a shell. Retain raw output, exit status,
measured time, timeout, scope, and post-run integrity. Failed execution is
inconclusive, not a counterexample. A valid numerical result remains numerical;
finite checks never prove an unbounded statement. Lean/CAS commands can be
attached only when their tools exist and their formal statement/assumptions
have been matched; no general prover or CAS is bundled.

## Frozen claim versions and reusable evidence

At a key evidence gate create a conditional claim-evidence.json record for the
exact claim/revision. Freeze its statement, hypotheses, quantifiers, parameter
range, topology, target reference, prior-work comparison, proof, and any versioned
dependencies. It is provisional evidence, not a new source of canonical truth.
The review binds this record and its proof, not work.md or the summary. Reuse
an exact version by reference across sessions instead of copying its proof.

A substantive correction creates a new revision with supersedes pointing to
the old record. Dependencies on superseded versions trigger a transitive recheck
warning and cannot clear a formal evidence gate until re-established. Editorial
changes do not automatically invalidate unrelated proofs. The affected query
reports downstream canonical claims read-only; no canonical status is silently
demoted. Human approval is still required for formal state changes. Version
labels and hashes cannot certify that a declared change was merely editorial.

## On-demand independent review

Trigger review for a key identity, core estimate, a claimed proof-gap closure,
a formal claim promotion, or an owner request. Routine exploration uses
self-checks and does not need a reviewer. Mark the trigger in the manifest's
`critical_review_required`; when proposing claim promotion the gate also applies
regardless of that flag.

1. Freeze the question, hypotheses, conventions, and permitted inputs in a
   reviewer brief that does not reveal the candidate proof or researcher verdict.
2. In a fresh context or with a human reviewer, save an independent derivation
   or attack and its hash before disclosing the candidate proof.
3. Then compare against the frozen candidate. Record dependencies, overlapping
   derivation roots, discrepancies, exact scope, and unresolved issues.
4. Save a v1.1 `review.json` linking the question, baseline, candidate, assessment,
   and the exact claim-evidence record (claim ID and revision). Index that record
   in `claim_records` and its review in `critical_reviews` in the manifest.
   Use `review_kind: independent` only when that read order was actually
   respected; otherwise record `self_check`. Metadata cannot enforce isolation.

Verdicts are `reject`, `uncertain`, or `survives_current_attacks`. The last is
necessary for accepting the submitted mathematical conclusion, not a proof
certificate. For a negative result, review the exact counterexample or scoped
obstruction as the submitted conclusion, rather than the disproved assertion. A substantive
repair needs a new frozen candidate and renewed comparison; review of an older
hash cannot cover it. Missing or rejected review leaves the claim provisional.

<!-- research-workflow:block route-evidence-review start -->
## Review routes when evidence stalls

After two consecutive sessions explicitly reporting no information gain, three
consecutive sessions on one route without independently reviewed
decisive support, or sooner after repeated obstructions or derivation roots,
structural failure, circularity, or an owner request, pause new construction on
that route. Preserve the original claim and distinguish a failed formula, a
repaired formula, the exact excluded candidate class, and untested alternatives.

Perform a fresh primary-source search driven by the actual obstruction before
recommending continuation or change. Keep one `route-review.md` with the
mathematical synthesis and independent assessment, plus `route-review.json` for
the indexed decision. No Researcher/Critic/Director role handoffs are required.
Only the owner approves continuation, repair, narrowing, suspension, rejection,
or a main-route switch after this review. Ordinary local repairs within the
existing approved scope do not themselves select a new main route.
<!-- research-workflow:block route-evidence-review end -->

## Information gained and workflow evaluation

At closure record progress in the manifest: a closed gap, a new excluded class,
a new external input, a useful distinction, or explicitly no new information.
Explain the exact mathematical delta in work.md. Changing notation or repeating
the same roots is not new evidence. Give a reason for any deliberate repetition.
Two consecutive no-information sessions trigger route review before more
construction; the existing three-session and structural-failure limits remain.
Both positive and negative results can supply useful information. These are
declared research judgments; the validator cannot determine novelty from prose.

Before adding further process, compare representative owner-supplied historical
tasks under frozen inputs and budgets. Isolate the factor being tested: keep
model and reasoning fixed when comparing workflows, then test model/effort
changes separately. Include valid derivations, hidden errors, wrong citations,
scoped failures, and unresolved tasks. Use tools/benchctl.py for input-only
packets, blinded answer labels, and separate human scores for correctness,
meaning, exposition, attribution, reproducibility, review time, wall time, and
known cost. Record every case/configuration including abstentions and budget
overruns. Reference answers and expected outcomes stay in owner-only packets;
host isolation must prevent runners from reading them. Mechanics-only examples
are not evidence that this workflow improves research productivity.

<!-- research-workflow:block readable-research-record start -->
## Approved mathematical record

`STATE.md` is the short entry point; `research/proof_ledger.md` owns exact claim
status, hypotheses, necessary dependencies, and evidence links. Keep detailed
proofs in linked artifacts. The machine mirror enables deterministic queries;
it does not outrank these files. Do not manually repeat the same result in a
proof map, task index, failed-approach list, research log, and learning note.
Use links; create a specialized note only when it adds mathematical content.
Existing detailed project records remain available and are never deleted by an
upgrade. Generate dashboards and consolidated reports from the approved record.

When a formal change is sought, add `state_update_proposal.md` and
`state-transition.json` only then. State the exact change, evidence, review,
remaining dependencies, and requested approval. Formal promotions and manuscript
claims cite local Txxx evidence IDs in `evidence_records`; each indexed record
links the reviewed proof version and its derivation roots. Explicitly provisional
planning entries (for example an open lemma) need no proof review, but still
need approval before entering canonical state. Until explicit owner approval,
keep canonical files and their hashes unchanged. After approval update only the
affected canonical records, synchronize their machine mirror, and validate.
The short STATE entry is an approved summary, not an automatic promotion path.
Run `python3 tools/researchctl.py report` when a consolidated reading copy is
wanted or at a sharing milestone. Markdown is the normal reading form; LaTeX
and PDF are optional exports. PDF tooling is not a prerequisite for research.
<!-- research-workflow:block readable-research-record end -->

<!-- research-workflow:block notation-disclosure start -->
## Notation

Define a new symbol before using it: object, domain or dependence, relevant
scale, relation to existing notation, and whether its scope is local or global.
Use short local abbreviations when helpful. Changes to global notation require
owner approval before updating the canonical notation or manuscript.
<!-- research-workflow:block notation-disclosure end -->

<!-- research-workflow:block mathematics-only-review-output start -->
## Mathematical reporting

Normal research replies explain the theorem target, exact result or scoped
obstruction, decisive argument, proof consequence, remaining gap, and next
question. Keep routine files, hashes, execution labels, and validator details
internal. Technical details belong in the response only when requested or when
a runtime/integrity problem affects mathematical reliability. Workflow
maintenance requests may be answered in software terms.
<!-- research-workflow:block mathematics-only-review-output end -->

<!-- research-workflow:block machine-control start -->
## Tools and compatibility (kernel 3.1.0)

The installer is preview-first and transactional. Run `workflow init TARGET`,
`workflow migrate TARGET`, or `workflow upgrade TARGET`, inspect changes, then
apply with `--apply` within the user's authorization. Project mathematics is
never copied from the source library or overwritten during an upgrade. Locally
modified managed documents are conflicts, not permission to discard changes.

New runs use manifest schema 1.3 without orchestration or workspace roles.
Legacy v1.0/v1.1/v1.2 manifests, task records, and historical role/orchestration
records remain readable and are checked when present; do not rewrite old runs
to fit the new model. Recognized legacy delivery manifests are reported as
historical and excluded from run evidence. Incomplete research manifests
still need deliberate review. The project-state schema remains 2.1 with its
distinct statuses and strict dependency semantics. An absent role registry is normal.
Upgrading tools does not approve a mathematical state change.

Use `python3 tools/researchctl.py validate`, `summary`, `status CLAIM_ID`,
`blockers CLAIM_ID`, `affected CLAIM_ID`, `dashboard`, or `report`. Mapping proposals use
`validate-proposal` and `dashboard-proposal` and remain visibly noncanonical.
Only `formal_exact`, `established`, and `verified` discharge strict prerequisites.
Claim `depends_on` holds necessary dependencies; typed graph edges express
support, tests, blocking relations, and circularity warnings. A route rejection
never rejects its theorem target automatically. Validation establishes
structural consistency only, not mathematical correctness.
<!-- research-workflow:block machine-control end -->

Implementation and commands: [Research feedback guide](docs/research-feedback.md).
