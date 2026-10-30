# Agentic research workflow

## Governing principle

The unit of progress is a human-approved project-state transition supported by
inspectable evidence. A run is only the execution layer inside the larger
research lifecycle:

$$
\text{literature landscape}
\longrightarrow\text{problem specification}
\longrightarrow\text{route selection and project initialization}
\longrightarrow\text{research runs}
\longrightarrow\text{knowledge and manuscript synchronization}
\longrightarrow\text{milestone review}.
$$

Raw agent output, agent consensus, numerical agreement, and a manuscript claim
do not by themselves change mathematical status.

<!-- research-workflow:block project-inception start -->
## New-project inception

A new project begins with information supplied by the owner: the tentative
question, its intended value, the desired kind of theorem or result, known
literature, constraints, available evidence, and acceptable scope. If any of
these are missing, Director records them as open questions instead of filling
them by assumption.

Before a proof route is activated, Director performs a primary-source
literature study and gives the owner one integrated mathematical assessment:
feasibility, potential value, a precise proposed theorem target, the main
obstructions, three to five genuinely different routes, the cheapest
discriminating tests, and a recommended route with reasons. The owner must
approve the precise target and route. Only after that approval may Director
freeze the proof framework, activate the selected route, and open its first
construction run.

The task in which the owner starts the project becomes the persistent Director
task and is titled `0 Director`. After route approval, create exactly two more
visible top-level tasks in the same saved project: `1 Researcher` and
`2 Critic`. They are peers, not children of Director. If either peer cannot be
created, stop at the workspace gate rather than weakening independent review.
<!-- research-workflow:block project-inception end -->

<!-- research-workflow:block owner-gates start -->
## Non-negotiable owner gates

1. A run is not closed until the Director gives the owner a concise
   mathematics-first project-state report. Code, calculations, generated files,
   agent verdicts, or lifecycle labels alone are not an acceptable run result.
   The report must say what mathematical statement was established, rejected,
   or left conditional; how the proof map changed or did not change; what
   remains open; and the next mathematical decision.
2. Every technical-route selection requires explicit owner approval. This
   includes selecting, switching, replacing, reviving, merging, or materially
   narrowing a proof mechanism. Agents may search, compare, falsify, and
   recommend routes, but no route becomes active and no construction run on it
   begins until the owner approves that route in plain language.
<!-- research-workflow:block owner-gates end -->

## Phase 0: literature landscape

Before selecting a proof architecture, inspect primary sources and record:

- the historical development and present best results;
- exact theorems, hypotheses, dimensions, regimes, and function spaces;
- proof mechanisms and imported lemmas;
- limitations, counterexamples, and unresolved gaps;
- the precise mismatch between each source and the present problem.

The startup artifacts are under `literature/`: `search_protocol.md`,
`historical_timeline.md`, `result_matrix.md`, `technique_map.md`,
`bibliography.md`, `unresolved_literature_questions.md`, and `status.md`.
Source notes follow `literature/source_note_template.md` and record exact
theorem and page locations rather than relying on titles or abstracts.

The literature gate closes only after the human approves the claimed frontier,
external inputs, and novelty risk. A targeted literature refresh is mandatory
after an F3 structural failure, an F5 missing-source finding, a major route
change, or a milestone review that exposes a new mechanism.

## Phase 1: problem specification

Translate the broad topic into a falsifiable project charter. Distinguish the
ideal objective, present project objective, current phase target, smallest
attackable bottleneck, and explicit non-goals. Record the equation or object,
parameter regime, topology, symmetries, conservation laws, baseline examples,
limiting cases, and known counterexamples. State each core difficulty as a
concrete obstruction. The human approves the theorem target, phase boundary,
scope, and external inputs at the problem gate.

## Phase 2: route selection and initialization

The Planner proposes three to five mathematically distinct routes, including a
primary construction, an independent alternative, and a cheap falsification
route. `research/route_matrix.md` compares source or structural motivation,
fit to the present setting, required lemmas, independence from existing
evidence, failure risks, cheapest decisive test, cost, and expected information
gain.

Exploratory source checks and cheap falsification calculations may inform the
comparison, but they do not select a route. The Director must present the
mathematical alternatives and request an explicit owner decision before
activating any technical route or opening its construction run.

Short feasibility calculations may reject a route before a formal run. They
must be labeled as such and stored in `research/baseline_checks.md` or
`calculations/`.

After human route approval, initialize `PROJECT_CHARTER.md`, `STATE.md`, the
proof ledger and proof map, notation, assumptions, core difficulties, agent
role files, and run templates. Only then is R001 opened.

## Phase 3: one research run

Each run is a frozen, inspectable Plan--Construct--Critique--Test--Adjudicate
cycle around one decision gate.

### Freeze the run

Copy `runs/_template/` to `runs/YYYY-MM-DD-RNN/`. The immutable `brief.md`
states one exact question, affected proof items, allowed assumptions, forbidden
shortcuts, planned tasks and gates, deliverables, and a crisp stop condition.
`status.md` is operational. A task absent from the frozen brief requires an
append-only authorization in `amendments.md` before dispatch.

### Plan and dispatch

The Director selects a proof-map bottleneck. Every task has one claim, one
parent, one output path, named dependencies, protected files, an experiment
trigger, and a stop condition. When a T or P identifier is reported to the
human, its mathematical meaning is stated in plain language.

The full frozen contract is the literal `makefile` block in
`agents/protocol.md` and `runs/_template/task-brief.md`. Save and hash that
dispatch before sending it to a visible role window.

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

### Construct

The Researcher fixes conventions from canonical sources, derives the assigned
claim, and labels statements exact, formal, conditional, conjectural,
numerical, external, or rejected. Gaps, counterexamples, and the smallest
missing lemma are exposed rather than smoothed over.

### Independent critique

For a major identity or proof gate, the Critic works in two passes:

1. read only the frozen question, conventions, and allowed assumptions, and
   write an independent baseline;
2. only then read the Researcher artifact and compare every disputed row.

The verdict is `reject`, `uncertain`, or `survives current attacks`. Critique
alone never returns `proved`.

### Targeted experiment

Use the Experimenter only when a reproducible check can change the decision:
a disputed sign or coefficient, scaling, moving cutoff, adjoint or commutator,
nonlocal variable, extreme-parameter limit, asymptotic expansion, or numerical
spectral assertion. Durable inputs, scripts, raw output, and sensitivity checks
belong in `calculations/`. Numerical evidence is not analytic proof.

### Repair and adjudication

Raw role artifacts are immutable. A repair creates `resolution-Txxx.md`, which
displays the corrected formula, names the superseded passages, and states
whether the conclusion changes. A substantive repair requires a new Critic
confirmation. The Director then writes a decision artifact and
`learning-note-Txxx.md` with the task meaning, affected proof items, decisive
evidence, remaining gap, and next human decision.

The corresponding human report is mathematics-first: theorem target, exact
new statement, decisive formula, proof consequence, remaining lemma, and next
mathematical question. Workflow IDs and audit metadata appear only afterward.
The report must remain intelligible if every R/T/P identifier is removed.
Code output, tool output, file inventories, or a statement that tasks completed
cannot substitute for this mathematical project-state explanation.

## Phase 4: knowledge and manuscript synchronization

At run closure the Director performs a distinct State Manager pass and writes
`state_update_proposal.md`. After human approval, synchronize:

1. `STATE.md`;
2. `research/proof_ledger.md`;
3. `research/proof_map.md`;
4. `research/notation.md` and `research/assumptions.md`;
5. `research/failed_approaches.md` and `research/research_log.md`;
6. `research/task_index.md`;
7. `paper/main.tex`, only for specifically approved manuscript content.

Successful attempts record the exact reusable statement, hypotheses,
mechanism, and downstream tasks unlocked. Failed attempts record the tested
method class, obstruction, scope of failure, counterexample, and unexcluded
alternatives.

Manuscript prose contains mathematics for collaborators, not R/T/P labels,
agent discussions, or project-management history. Exact identities and proved
lemmas receive proofs; indispensable open results may be stated explicitly as
unproved. After every manuscript edit, check

$$
\text{STATE}\leftrightarrow\text{proof ledger}
\leftrightarrow\text{proof map}\leftrightarrow\text{notation}
\leftrightarrow\text{assumptions}\leftrightarrow\text{manuscript}.
$$

## Phase 5: milestone review

Review the entire project after three to five runs, an F3/F4 outcome, a major
proof-map change, a new relevant source, a publishable intermediate result, or
several runs that do not reduce the main uncertainty. Decide whether to
continue, change architecture, narrow the theorem, extract an intermediate
paper, pause for an external input, or stop. The review asks whether the proof
map has actually shortened, whether a difficulty was merely renamed, whether
circular dependencies remain, and whether the literature landscape needs
refreshing.

## Evidence gates

| Proposed status | Minimum evidence |
| --- | --- |
| Established algebraic identity | Line-by-line derivation with conventions fixed and independent audit passed |
| Verified analytic lemma | Complete proof with explicit hypotheses, quantifiers, and verified/external dependencies |
| External input | Exact theorem/page citation with hypotheses matched to the project |
| Numerical evidence | Reproducible input/code and convergence or sensitivity check; no promotion to proof |
| Conditional | Every missing prerequisite named by proof-ledger ID |
| Rejected | Explicit contradiction, counterexample, or structural incompatibility recorded |
| Open | No evidence meeting a stronger gate |

## Failure-to-next-action map

| Class | Meaning | Required next action |
| --- | --- | --- |
| F1 | Technical gap or missing lemma | Create the smallest lemma task and dependency |
| F2 | Incompatible parameters or estimates | Reject the regime or reformulate |
| F3 | Structural method failure | Record the obstruction, refresh literature, and change mechanism |
| F4 | False conjecture or identity | Preserve the counterexample/correction and modify the claim |
| F5 | Missing literature, data, or computation | Perform one precise source lookup or experiment |
| F6 | Circularity or reused evidence | Break the dependency and seek an independent information source |

## Human checkpoints

The human approves the literature frontier, problem statement, phase target,
every technical route choice or change, run objective, post-F3/F5 architecture,
bootstrap assumptions,
global notation, proof-ledger promotion, rejection of a major route,
continuation through a conditional gate, manuscript transfer, and milestone
decision.

Dispatch inside an approved gate, reproducible checks, resolution drafts,
state proposals, compilation, and consistency audits may proceed without a new
checkpoint.

## Persistent windows

Use visible persistent Director, Researcher, and Critic windows. Add an
Experimenter window only when triggered. Planner and State Manager are passes
inside the Director window unless an independent process audit is requested.
Role names do not create independence; the frozen brief and two-pass Critic
read order do.

<!-- research-workflow:block peer-role-tasks start -->
### Required Codex task topology

- The current project task is renamed `0 Director`; it remains the coordinating
  task in which the owner started the project. Create only the two missing peer
  tasks, titled exactly `1 Researcher` and `2 Critic`.
- Director, Researcher, and Critic run as three distinct top-level Codex tasks
  that are visible in the sidebar. They are peers sharing the saved project;
  Researcher and Critic are not Director subagents.
- Director creates or reconnects Researcher and Critic only after the owner has
  approved the initial theorem target and route, or has explicitly authorized
  repair of an existing workspace. It must use the Codex new-task capability
  once per missing peer and must never substitute an in-turn
  `spawn_agent`/subagent for a persistent role task.
- All three role tasks use the saved project directly so that frozen briefs,
  artifacts, and hashes are visible to every role. Isolated worktrees require
  separate owner approval because they change the evidence-sharing topology.
- Record returned task and host identifiers in
  `research/machine/workspace-roles.json`. This is an operational registry, not
  canonical mathematical state. It cannot approve a route, claim, run, or
  state transition.
- If a role task cannot be created or reconnected, report the workspace as
  incompletely bootstrapped. Do not silently collapse the role into Director.
<!-- research-workflow:block peer-role-tasks end -->

## Live completion loop

The Director does not end its turn merely because a role task is running. It
verifies the visible task is active, waits in bounded intervals, audits the
returned artifact and protected-file manifest, records a separate resolution
for any defect, and then advances to the next dependency-ready task inside the
same approved run. The loop ends only at a human gate, a run boundary, a need
for new authority or information, or a genuine task-infrastructure failure.
No subsequent run is opened automatically.

<!-- research-workflow:block director-return-loop start -->
### Director return loop

For every dispatched Researcher or Critic task, the Director writes the
current phase, awaited role, active task, next action, and any owner gate to
the active run's `orchestration.json`. The Director then remains in the same
turn and waits for that top-level task. After saving its immutable artifact,
the role sends a completion notice to the registered Director task. Completion
therefore returns control to Director for artifact audit; it does not authorize
the role to dispatch its own successor.

After audit, Director must choose exactly one transition:

1. dispatch the already-authorized next task and resume waiting;
2. send a repair or independent Critic task and resume waiting;
3. close the approved run with its mathematical summary and state proposal; or
4. enter `owner_gate`, explain the mathematical decision, and request approval.

The Director may not finish with a vague “agents completed” state. A run is
either advancing under existing approval, awaiting a named role, at a precise
owner gate, or closed.
<!-- research-workflow:block director-return-loop end -->

<!-- research-workflow:block route-evidence-review start -->
## Route evidence review

Every completed run on an active route receives one operational route signal:
`decisive_support`, `partial_support`, `null_result`, `scoped_obstruction`,
`structural_failure`, or `not_applicable`. `decisive_support` requires
Critic-audited evidence that closes or materially discharges a named blocking
proof item in its stated scope; activity, plausible calculations, numerical
agreement, agent consensus, and additional files do not qualify.

A Route Evidence Review becomes mandatory before another construction run on
the same route when any of the following occurs:

- three consecutive completed runs since the last route review have no
  `decisive_support` signal;
- two runs reproduce substantially the same obstruction or reuse the same
  derivation roots without new information;
- a run reports `structural_failure`, an F3 failure, or an F6 circularity;
- the owner requests a review.

Three runs is the default maximum, not a minimum waiting period: Director or
the owner may trigger review earlier, and a run brief may set a lower threshold.
Raising the threshold above three requires explicit owner approval.

The review is a consolidation checkpoint, not permission to select a route.
Director freezes the route thesis and reviewed run set; Researcher produces an
evidence/obstruction synthesis; Critic independently tests whether the route's
mechanism still has a credible path to the named proof gate; Director then
writes `route-review.md` and `route-review.json`. The packet must separate
decisive support, partial support, null results, scoped obstructions, repeated
derivation roots, remaining bottlenecks, and the cheapest discriminating test.

Before Director recommends any continuation or change, Researcher must perform
a new systematic primary-source search driven by the exact obstructions found
in those runs. The review records the questions searched, the sources checked,
whether they contain a mechanism not yet tested here, and how each candidate
mechanism compares with the current route. Critic audits this literature
comparison independently. A recommendation cannot reach the owner while this
refresh remains incomplete.

Permitted recommendations are: continue unchanged, repair, materially narrow,
branch to a comparison, suspend, reject a precisely scoped route, or refresh
the literature. The review may be generated automatically, but every continue
decision after a mandatory review and every repair, narrowing, switch,
replacement, suspension, revival, merge, or rejection requires explicit owner
approval before the next construction run.
<!-- research-workflow:block route-evidence-review end -->

<!-- research-workflow:block readable-research-record start -->
## Readable mathematical record

The authoritative project files remain Markdown because they are easy to
review and amend. After every owner-approved mathematical advance, also rebuild
one consolidated reading copy in three forms:

- `report/project-summary.md` for direct reading and annotation;
- `report/project-summary.tex` for mathematical typesetting and long-term use;
- `report/project-summary.pdf` for stable reading and sharing.

Run `python3 tools/researchctl.py report` after the canonical synchronization.
These three files are reading views, not independent sources of mathematical
truth. If PDF generation fails, report the obstacle because the required
readable record is incomplete.

Operational progress is recorded immediately in the active run without
changing theorem status. Once the owner approves a mathematical state change,
update `STATE.md`, the proof ledger, proof map, notation and assumptions as
applicable, append the research log, and rebuild all three reading formats in
the same synchronization step. Preserve earlier run artifacts and decisions;
never rewrite them to make the current account look cleaner.
<!-- research-workflow:block readable-research-record end -->

<!-- research-workflow:block notation-disclosure start -->
## New-notation disclosure

Before a new symbol first appears in a response to the owner, explain in
ordinary mathematical language:

1. what mathematical object it denotes;
2. its domain, parameter dependence, and scaling or units when relevant;
3. why existing notation is insufficient;
4. how it relates to existing symbols; and
5. whether it is temporary to one derivation or proposed as global notation.

A temporary local abbreviation may be used after this explanation, but it does
not enter canonical notation. Adding, replacing, overloading, or retiring a
global symbol requires explicit owner approval before editing
`research/notation.md`, canonical state, or the manuscript. If the notation is
not approved, state the result using existing notation whenever possible.
<!-- research-workflow:block notation-disclosure end -->

<!-- research-workflow:block mathematics-only-review-output start -->
## Mathematics-only review output

After a role review, Director adjudication, route review, or run closure, the
normal response to the owner contains only:

1. the mathematical target or current theorem state;
2. the exact result, counterexample, obstruction, or remaining conditional;
3. the decisive formula or argument when one exists;
4. the consequence for the proof;
5. the remaining gap and next mathematical question; and
6. the mathematical choice requiring owner approval, if any.

Do not mention chronology verification, baselines, control planes, artifact
hashes, protected files, compatibility checks, validator results, task/thread
lifecycle, model settings, file inventories, sidecars, schemas, or code
execution in a normal review response. Perform and record those checks
silently. Translate every conclusion into its mathematical meaning—for example,
say which hypotheses cannot hold simultaneously instead of reporting a
compatibility result. Mention technical matters only when a runtime or
integrity problem makes the mathematical conclusion unreliable, blocks
continuation, or requires owner action, or when the owner explicitly asks for
audit details.
<!-- research-workflow:block mathematics-only-review-output end -->

## Automation boundary

Automation may create directories, validate artifact fields, dispatch approved
briefs, run reproducible checks, and prepare proposals. It must not decide
mathematical truth, promote the ledger, change global notation, select a new
architecture after structural failure, or transfer claims into the manuscript.

<!-- research-workflow:block machine-control start -->
## Machine control layer (kernel 2.7.0)

The reusable kernel version and installed-file hashes are recorded in
`.research-workflow.json`. Project mathematical state is deliberately excluded
from kernel upgrades. Preview lifecycle operations before applying them:

```bash
python3 tools/workflowctl.py init TARGET --project-name NAME
python3 tools/workflowctl.py migrate TARGET
python3 tools/workflowctl.py upgrade TARGET --source NEWER_KERNEL_ROOT
```

Add `--apply` only after reviewing the resolved target, planned changes,
conflicts, and state-mapping gate. Apply repeats the no-write preflight and is
transactional: a later write failure rolls back all known target files.
`init` creates an empty S0 scaffold;
`migrate` preserves legacy canonical files and detects IDs for a semantic
mapping pass; `upgrade` replaces only unmodified managed files and marked
documentation blocks. Managed blocks have their own drift hashes. Run templates
are whole-file versioned assets, so the template set upgrades together while
already instantiated runs remain untouched. Changed managed content is reported
as a conflict, with backups stored under `.research-workflow/backups/`.

The project carries a read-only structured mirror under
`research/machine/project-state.json`. In kernel 2.0, `STATE.md` and
`research/proof_ledger.md` remain authoritative; the mirror exists to make
dependencies, scoped route failures, evidence hashes, and operational/canonical
drift deterministically inspectable.

Mathematical routes and executions use separate namespaces. `route:<slug>`
identifies a technical route; `R<number>` identifies one run. A route may be
tested by several runs, and a proposal-only run may have no selected route.
Each new run uses `manifest.json` and `orchestration.json`, each task uses
`Txxx.json`, and each proposed canonical transition uses
`state-transition.json`. A triggered route consolidation uses
`route-review.md` and `route-review.json`; their schemas live under `schemas/`.

Claim vocabulary is conservative. `formal` means an uncontrolled or
model-level formal derivation and remains unresolved; `formal_exact` means an
exact identity in the explicitly stated formal model; `conjectural` remains
unresolved; `established` is resolved only when its scope and evidence gate are
recorded. Never normalize one of these words into another during migration.

The claim ledger owns strict logical dependencies through `depends_on`.
Proof-map edges record only `supports`, `tests`, `blocks`, `surveys`, or
`warns_circularity`. After `snapshot.theorem_targets` is owner-reviewed,
`blocking` is the derived set of unresolved strict prerequisites, not a free
importance label.

Run the control-plane validation before dispatch, after a role artifact returns,
before preparing a state proposal, and after every approved canonical sync:

```bash
python3 tools/researchctl.py validate
```

Useful read-only queries are:

```bash
python3 tools/researchctl.py summary
python3 tools/researchctl.py status CLAIM_ID
python3 tools/researchctl.py blockers CLAIM_ID
python3 tools/researchctl.py dashboard
python3 tools/researchctl.py validate-proposal
python3 tools/researchctl.py report
python3 tools/researchctl.py dashboard-proposal
```

The validator checks canonical and sidecar hashes, dispatch records, run
manifests, state-transition proposals, identifier references,
claim-dependency acyclicity, route rejection scope, and the distinction between
operational and human-approved canonical state. A successful validation
establishes only structural consistency. It is not mathematical evidence.

New dispatches record an evidence class, declared derivation roots, and any
claimed evidence independence. These fields make F6 reuse auditable; different
role names or fresh contexts do not by themselves create independent evidence.
Historical runs need not be rewritten. Their accepted decision artifacts may be
registered incrementally with exact hashes and scopes.

To inventory a historical run without promoting inferred metadata, use:

```bash
python3 tools/workflowctl.py hydrate-run TARGET R001 --proposal-only
```

Review the preview, then add `--apply`. This writes only
`run-hydration.proposal.json`; it hashes existing artifacts and lists unresolved
state, route, status, lineage, and transition mappings. It never creates
canonical sidecars by itself.

After human approval of a canonical transition, update the canonical files
first, then update the machine mirror and its hashes in the same synchronization
pass. Before approval, operational results may appear in the mirror with a
canonical/operational mismatch warning, but they must not change a claim's
canonical status. The generated `dashboard/index.html` is a read-only view and
never writes project state. Its interface can be switched between Chinese and
English. The language choice changes navigation, status labels, legends, and
explanatory text only; mathematical claims, route conclusions, and project
notes remain in their authored language so translation cannot alter their
meaning. The same switch is available in the visibly non-canonical proposal
preview.

The normal Dashboard is written in mathematical research language. Its primary
views describe theorem targets, proof prerequisites, present mathematical
standing, route conclusions, surviving results, and unresolved gaps. Internal
record diagnostics are confined to the research-record review view, with
technical details collapsed unless the user opens them.
<!-- research-workflow:block machine-control end -->
