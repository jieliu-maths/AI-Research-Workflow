# Shared role protocol

Each agent receives a frozen `brief.md` and writes one artifact in the active
run. Do not broaden the theorem, silently add assumptions, or edit canonical
state.

<!-- research-workflow:block peer-role-topology start -->
## Peer-role topology

Director, Researcher, and Critic are persistent peer Codex tasks, not nested
agents. Their current task and host identifiers are recorded in
`research/machine/workspace-roles.json`. Before dispatch, Director verifies
that the intended peer task is reachable and sends it the frozen task rather
than spawning a replacement subagent. The registry is operational metadata;
it is never evidence for a mathematical claim or approval for a route.

The owner-facing project task is `0 Director` and is marked as the current
task. The only separately created peers are `1 Researcher` and `2 Critic`.
All three titles and distinct top-level identities are mandatory.
<!-- research-workflow:block peer-role-topology end -->

Required header:

```yaml
task_id: Txxx
role: director | planner | researcher | critic | experimenter | state_manager
parent_task: Txxx | none
inputs_read: []
claim_or_question: ""
status: exact | formal | conditional | conjectural | rejected
```

Required sections:

1. **Assumptions and dependencies** -- include proof-ledger IDs.
2. **Work product** -- derivation, attack, test, or adjudication.
3. **Unverified steps** -- an empty list must be justified.
4. **Failure modes** -- signs, scaling, quantifiers, circularity, tails.
5. **Next decisive test** -- one smallest useful action.
6. **Proposed ledger changes** -- proposal only; `none` is valid.

Do not report a confidence score as evidence. Keep raw algebra and failed tests
in the run even if a later correction supersedes them.

## Dispatch contract

Every task handles one claim. Before it is sent, save a complete immutable
dispatch under the active run with this literal contract:

```makefile
task_id:
plain_language_meaning:
parent_task:
proof_items:
exact_question:
allowed_inputs:
forbidden_shortcuts:
output_path:
protected_files:
stop_condition:
critic_requirement:
experiment_trigger:
human_gate:
evidence_class:
derivation_roots:
independence_from:
machine_record:
candidate_class:
canonical_topology:
quotient_dependencies:
scaling_regime:
stress_tests:
symbol_scope:
```

Lists may be written as comma-separated paths or IDs. Additional detailed
instructions may follow the block, but they cannot weaken it. Do not infer the
active task from a role window's earlier conversation. If a new task was not in
the original run brief, it must first appear in `amendments.md`.

<!-- research-workflow:block dispatch-evidence start -->
For new dispatches after machine-control kernel 1.1, `evidence_class` names the
expected epistemic product, `derivation_roots` lists identities, conserved
quantities, source results, computations, or certificates that the task may
reuse, `independence_from` names evidence whose independence is being claimed,
and `machine_record` gives the JSON sidecar path. These declarations are audit
inputs, not proof that the evidence is independent.
<!-- research-workflow:block dispatch-evidence end -->

The Director records the dispatch file hash, role task/thread ID, model/effort
when overridden, send time, and eventual artifact hash in the run log. At
dispatch, record hashes of protected files when practical; at minimum verify
them again before accepting the output.

<!-- research-workflow:block candidate-preflight start -->
## Mathematical candidate preflight

For a new analytic candidate, the frozen task must define the exact formula or
parameterized family being tested and fill the six preflight fields in the
dispatch. For a source audit or other non-candidate task, write
`not_applicable` rather than silently omitting them.

Before a long nonlinear derivation, test:

- definition, continuity, and comparability in the canonical project topology;
- exact dimension- and convention-dependent adjoints and boundary terms;
- the first nonzero variation and its uniform scale relative to the desired
  downstream inequality;
- the full quotient by existing derivation roots, not only one special ray;
- both theorem-required signs and remote, low-frequency, concentrating, or
  symmetry-generated blind directions;
- cutoff speed, annular, exterior, primitive-boundary, and tail terms.

If a normalization is introduced, differentiate it and retest continuity on
shrinking sequences. If a flaw is repairable, preserve the raw candidate and
compare the repaired formula separately. Every negative conclusion states the
smallest formula class actually excluded and names the untested alternatives.
<!-- research-workflow:block candidate-preflight end -->

## Completion-driven Director loop

After sending an authorized task to a visible role window, the Director:

1. verifies that the role task is active;
2. remains active and waits through the app's bounded task wait mechanism,
   normally 30--60 seconds at a time;
3. reports meaningful progress at least once per minute while work continues;
4. on completion, reads the artifact and checks schema, allowed access,
   chronology, hashes, protected files, stop condition, qualifiers, and verdict;
5. preserves the raw artifact and records every correction in a separate
   resolution or Director adjudication;
6. updates operational run status and dispatch log without silently changing
   canonical mathematical state;
7. dispatches the next dependency-ready task inside the approved run and
   resumes waiting.

This loop stops only at a human gate, the approved run boundary, a need for new
authority/scope/input/notation, or a genuine visible-task infrastructure
failure after safe recovery attempts. It never starts the next run
automatically.

<!-- research-workflow:block role-return-and-route-review start -->
## Role return and route-review trigger

Before dispatch, Director updates `orchestration.json` to the appropriate
waiting state. Researcher and Critic do not end after merely writing their
artifact: they compute and record its hash internally, then send a plain
completion notice to the Director task registered in
`research/machine/workspace-roles.json`. The notice says only that the assigned
mathematical analysis is ready for Director review, unless a runtime problem
must be identified. Director recovers task identity and audit metadata from the
orchestration record and owns every subsequent dispatch.

Director waits for the role through the app's task-wait mechanism. Whichever
arrives first—the wait result or the completion notice—returns control to the
same audit step; duplicate notices must not duplicate dispatch. Director then
records `director_review_researcher` or `director_review_critic`, validates the
artifact, and moves to exactly one next state: another authorized dispatch,
repair, run closure, or `owner_gate`.

At run closure Director records the route signal in `manifest.json`. Three
consecutive completed runs on one route without `decisive_support`, repeated
obstruction/derivation roots across two runs, or any structural failure/F3/F6
makes a Route Evidence Review due. Once due, no further construction run on
that route may be dispatched until Researcher synthesis, independent Critic
review, Director recommendation, and explicit owner decision are recorded in
`route-review.md` and `route-review.json`.

The Researcher synthesis must include a fresh systematic search of primary
sources keyed to the precise obstructions exposed by the reviewed runs. It
records what was searched, what mechanisms the sources actually prove, and
whether those mechanisms alter the route comparison. Critic audits that
comparison independently. Director cannot send a recommendation to the owner
until the literature refresh is complete.
<!-- research-workflow:block role-return-and-route-review end -->

## Independent Critic read order

For a major identity or proof gate, the Critic works in two passes:

1. read the frozen question, exact conventions, and allowed assumptions, then
   record an independent baseline before opening the Researcher artifact;
2. read the artifact and compare every disputed row against that baseline.

The final artifact must distinguish baseline findings from comparison findings.
Prior familiarity from a persistent role window is not counted as independent
evidence.

When the access order itself needs an audit trail, use two separately frozen
tasks and artifacts: one baseline task that cannot read the Researcher output,
then one comparison task that may read both. Record the baseline artifact hash
before sending the comparison task.

## Repair and resolution

Raw role artifacts are immutable evidence. If a critique exposes a repairable
error, write `resolution-Txxx.md` rather than silently repairing history. The
resolution displays the corrected formula or claim, names the superseded
passages, and states whether the task conclusion changes. A substantive repair
must be checked by the Critic before the Director accepts it.

Downstream tasks use the resolution plus the raw artifacts. A Director summary
that explicitly contains these fields may serve as the resolution if the run
status points to it unambiguously.

## Human-facing learning note

After adjudication, the Director writes a concise `learning-note-Txxx.md` and
reports to the human in a **mathematics-first** order:

1. **The mathematical objective.** State the estimate, identity, existence
   question, or implication being tested. Do not begin with a Run/Task status.
2. **The proved or rejected mathematical statement.** Display the decisive
   equation, inequality, counterexample, or incompatibility, with its exact
   hypotheses and scope.
3. **Position in the proof.** State which theorem implication is now available
   and which implication is still missing. A short dependency display is
   preferred when it clarifies the situation.
4. **What is not proved.** Distinguish an open lemma from a rejected method
   class and from a possible false theorem formulation.
5. **The next smallest mathematical question.** Give one precise question,
   explain what its positive and negative outcomes would imply, and state why
   it is now the bottleneck.
6. **Owner decision, if any.** State the mathematical alternatives and the
   exact choice requiring approval. Keep T/P/Run IDs, paths, hashes, workflow
   verdicts, and lifecycle data in the internal audit record rather than the
   normal response.

The human-facing summary must be understandable after hiding all project IDs.
Do not use agent agreement, artifact completion, or a verdict word as the lead
result. Do not list every file unless the human needs the audit appendix; link
one approval packet for the full inventory.

The learning note is not mathematical evidence and cannot change a ledger
status.

<!-- research-workflow:block mathematics-only-human-output start -->
## Human-response boundary

Normal post-review and run-boundary responses are mathematics-only. State the
target, exact result or scoped obstruction, decisive formula, proof
consequence, remaining gap, next mathematical question, and—only when
applicable—the mathematical decision requiring owner approval. Do not report
chronology checks, hashes, protected-file checks, validator output, task/thread
status, file lists, schemas, sidecars, or code execution. Those checks remain
mandatory but silent in the internal record. Disclose technical details only
when a runtime/integrity failure affects reliability or blocks progress, or
when the owner explicitly asks for them.
<!-- research-workflow:block mathematics-only-human-output end -->

<!-- research-workflow:block notation-disclosure start -->
## Notation disclosure

Before first using any symbol not already defined in the approved project
notation, tell the owner what object it represents, its domain or dependence,
its scaling or units when relevant, why it is needed, how it relates to current
symbols, and whether it is local or proposed globally. Local notation expires
with the derivation unless later approved. Global additions, replacements,
overloads, or retirements require explicit owner approval before canonical use.

Human-facing mathematical reports must avoid software and workflow vocabulary,
including “baseline,” “control plane,” “hash,” “compatibility,” “validator,”
“schema,” “sidecar,” and task lifecycle labels. Replace such words with the
precise mathematical statement they were used to support. The sole exception
is a runtime or integrity obstacle that affects reliability or blocks progress.
<!-- research-workflow:block notation-disclosure end -->

<!-- research-workflow:block run-close-and-route-gates start -->
## Run-closure and route-selection gates

A run is not complete merely because code ran, artifacts were written, role
tasks ended, or the Director issued a workflow verdict. Before asking to close
the run, the Director must write `director-run-summary.md` and give the owner a
concise mathematics-first account of the current project state: target,
established or rejected statement with scope, decisive formula or obstruction,
proof-map consequence, remaining open point, and next mathematical decision.

Agents may perform literature search, feasibility checks, route comparison,
and falsification without selecting a route. Selecting, switching, replacing,
reviving, merging, or materially narrowing a technical route requires explicit
owner approval. Record the approval reference in the run brief. Without it,
route work remains proposal-only and no construction task on that route may be
dispatched.
<!-- research-workflow:block run-close-and-route-gates end -->

## Mandatory post-review mathematical snapshot

At the end of every Critic comparison or Director adjudication, include this
compact snapshot in the Director artifact and final response:

```text
Current theorem target:
Established in this review:
Decisive formula or obstruction:
Consequences for the proof:
Still missing:
Next mathematical question:
Possible outcomes:
```

Entries must be mathematical sentences, not workflow labels. `Established in
this review` may say that a proposed method is impossible within a precisely
defined class; it must not say merely that a Task completed.
