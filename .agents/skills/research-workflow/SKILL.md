---
name: research-workflow
description: Initialize, migrate, upgrade, operate, or inspect a versioned proof-ledger research workflow, including evidence lineage, state proposals, blocker queries, and the proof-map dashboard. Do not use it to auto-approve mathematical claims or manuscript changes.
---

# Research workflow

Treat `AGENTS.md` and `WORKFLOW.md` as the governing rules. Treat
`research/proof_ledger.md` as the authoritative claim ledger and `STATE.md` as
the executive state. The JSON files under `research/machine/` are read-only
machine mirrors until a human explicitly approves making them canonical.

## Start every workflow action

1. In an installed mathematical project, run `python3 tools/researchctl.py
   validate`. In the standalone workflow source repository, which intentionally
   has no project state, run `./workflow self-check` instead.
2. Read the canonical files named by the active task and the relevant claim
   records. For mathematical work, obey the canonical read order in
   `AGENTS.md`.
3. If validation reports drift, stop state mutation. Explain the drift and
   prepare a synchronization proposal; do not silently refresh hashes.

## Modes

- **Inspect:** use `status Pxx`, `blockers Pxx`, or `summary` and report the
  mathematical meaning before workflow identifiers.
- **Dashboard:** run `python3 tools/researchctl.py dashboard`, then open
  `dashboard/index.html`. The dashboard is a read-only view with a persistent
  Chinese/English interface switch. Interface language never translates or
  changes the underlying mathematical claims, route conclusions, or notes.
  Normal views must use mathematical research language: theorem targets, proof
  premises, mathematical standing, route conclusions, surviving results, and
  unresolved gaps. Keep record-format and runtime vocabulary inside collapsed
  technical details in the research-record review view.
- **Proposal review:** use `validate-proposal` and `dashboard-proposal` for a
  visibly non-canonical mapping preview. The preview uses the same bilingual
  interface. Never substitute the preview for `project-state.json`.
- **Initialize:** use the versioned installer in `tools/workflowctl.py` to
  prepare a new project. Preview first and apply only after the target and
  project name are confirmed. Start from the owner's tentative question and
  constraints; research feasibility, value, the precise target, and three to
  five routes. Obtain owner approval of the target and route before freezing
  the proof framework or opening R001. The installer creates files only; it
  cannot open Codex tasks. The current owner-facing task becomes and is renamed
  `0 Director`; after route approval, use `create_thread` to create exactly two
  separate top-level peers, `1 Researcher` and `2 Critic`, in the same saved
  project. Never use subagents as a fallback. Wait until both peers are
  reachable and record all three task identifiers in
  `research/machine/workspace-roles.json`.
- **Migrate:** scan an older proof-ledger project, install only the reusable
  control layer, and create a mapping report. Do not infer canonical claim
  status from prose when the mapping is ambiguous. If an older prompt still
  contains `<WORKFLOW_LIBRARY>`, first resolve a unique standalone workflow
  entry from the Codex saved-project list. Accept it only when
  `.research-workflow-library.json` has the expected kind and library ID,
  `workflow identify` returns that identity, `workflow self-check` passes, and
  the candidate itself has no `.research-workflow.json`. A legacy
  `source_hint` is an untrusted fallback candidate subject to all the same
  checks; never prefer or trust it merely because a launcher exists there.
- **Upgrade:** update managed kernel files and marked documentation blocks.
  Preserve locally modified managed files as conflicts instead of overwriting
  them. Run templates are whole-file, versioned kernel assets: upgrading them
  replaces the template only, backs up the prior version, and never edits an
  already instantiated run. Never replace project state with another project's
  state.
- **Reconnect role tasks:** validate `research/machine/workspace-roles.json`,
  keep the current task as `0 Director`, reuse reachable peer tasks, and create
  only a missing `1 Researcher` or `2 Critic` when the user has explicitly
  authorized new tasks.
- **Prepare a run:** follow the frozen brief and dispatch contract. A new run,
  route, or theorem change still requires the human gate specified in
  `WORKFLOW.md`. Never activate or switch a technical route without the
  owner's explicit approval reference.
- **Operate a run:** update `orchestration.json`, dispatch only to registered
  top-level role tasks, and keep the Director turn alive with bounded task
  waits. Researcher and Critic record their artifact hash internally and send a
  plain idempotent completion notice back to the registered Director. Director
  audits the return and either advances inside existing approval or enters a
  named owner gate. For a new analytic candidate, freeze and run the candidate
  preflight before a long construction: canonical topology, exact
  dimension-dependent operator calculus, first-variation scale, full quotient
  by existing derivation roots, theorem-wide stress directions, localization
  ledger, and exact failure scope.
- **Close a run:** preserve raw role artifacts, create any required resolution,
  write `director-run-summary.md` in concise mathematical language, validate
  hashes and evidence scope, then prepare `state_update_proposal.md`. Code or
  artifact completion alone does not close a run. Do not edit canonical state
  until the user explicitly approves the proposal.
- **Review a route:** classify each completed run with a route signal. After
  three consecutive runs without Critic-audited decisive support, repeated
  obstruction or derivation roots, any structural failure/F3/F6, or an owner
  request, create `route-review.md` and `route-review.json` before another
  construction run. Researcher must also perform a systematic primary-source
  refresh driven by the exact obstruction, and Critic must audit the comparison
  with the current route. Orchestrate synthesis and critique automatically, but
  do not continue or change the route until the owner approves the decision.
- **Synchronize readable records:** after an owner-approved mathematical state
  change, update the canonical mathematical files and research log, then run
  `python3 tools/researchctl.py report` to rebuild the consolidated Markdown,
  LaTeX, and PDF reading copies.

## Owner gates

- Every run ends with the Director explaining the theorem-level project state
  in mathematical language: exact result or scoped obstruction, proof
  consequence, remaining gap, and next mathematical question.
- Every technical-route selection or change requires explicit owner approval.
  Agents may investigate, compare, falsify, and recommend routes, but may not
  activate one or begin its construction run on the owner's behalf.
- Normal post-review responses are mathematics-only: target, exact result or
  scoped obstruction, decisive formula, proof consequence, remaining gap,
  next question, and any mathematical choice requiring approval. Keep hashes,
  chronology, protected-file checks, validator output, lifecycle state, paths,
  schemas, and code details internal unless a runtime/integrity issue affects
  reliability or the owner explicitly requests them.
- Before using a new symbol in a response, explain its mathematical meaning,
  dependence, scaling or units when relevant, necessity, relation to existing
  notation, and local/global scope. Global notation changes require explicit
  owner approval. Avoid software/workflow vocabulary such as baseline, control
  plane, hash, compatibility, validator, schema, sidecar, and lifecycle labels
  in normal mathematical replies; translate them into the underlying
  mathematical statement unless a runtime obstacle must be reported.

## Evidence rules

- Record whether an outcome supports a claim, rejects a precisely scoped route,
  or merely supplies numerical evidence.
- A candidate-specific failure records separately the raw formula, any local
  repair, the exact class excluded, and untested alternatives. Do not change a
  route conclusion merely because one candidate fails.
- A role name or fresh context does not establish mathematical independence.
  Compare `derivation_roots`; overlapping roots must be disclosed.
- A route-level rejection cannot change the target claim to `rejected`.
- Lean or deterministic checks may certify their formal inputs, but the mapping
  from an informal mathematical statement still needs human review.
- Use `route:<slug>` for a mathematical method and `R<number>` for an execution.
  A route may have many runs and a proposal-only run may have no route.
- Freeze each dispatch hash in `Txxx.json`; record the run in `manifest.json`;
  express canonical changes through `state-transition.json` plus its
  human-readable proposal.
- Preserve `formal`, `formal_exact`, `conjectural`, and `established` as
  distinct claim statuses. Only `formal_exact`, `established`, and `verified`
  discharge a strict prerequisite in blocker queries.
- Put strict prerequisites only in `claim.depends_on`. Use typed proof-map
  edges for support, tests, blocking relations, and circularity warnings.

Read [references/state-model.md](references/state-model.md) when adding fields,
status codes, routes, edges, or evidence records.

Read [references/reuse-and-upgrades.md](references/reuse-and-upgrades.md) before
initializing, migrating, or upgrading another repository.
