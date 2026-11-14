---
name: research-workflow
description: Initialize, migrate, upgrade, operate, or inspect the single-window mathematical research workflow, evidence lineage, proposals, and proof-map dashboard. Never auto-approve mathematical claims or manuscript changes.
---

# Research workflow

Follow `AGENTS.md` and `WORKFLOW.md`. Default to the current research window;
no Director/Researcher/Critic tasks, fixed titles, role registry, or
orchestration loop is required. Do not create or rename chats unless explicitly
requested. Retired role files are optional activity references, not prerequisites.

## Start and recover

In the standalone workflow source run `./workflow self-check`. In an installed
project run `python3 tools/researchctl.py validate`. Stop canonical mutation on
drift; do not refresh hashes silently. Read the short `STATE.md` first, then
the relevant charter, problem, ledger, notation, and active brief as needed.
Load long derivations and historical records only when the question needs them.
Work on one mathematical question at a time.
When history has moved beyond STATE, read the optional project-owned
`research/current-work.md` for exact working series, drafts, review coverage and
the next question. Keep its navigation status separate from approved mathematics.

## Initialize, migrate, and upgrade

Read [reuse-and-upgrades.md](references/reuse-and-upgrades.md) before lifecycle
operations. Resolve and verify the standalone library, preview changes, then
apply within the user's authorization. Preserve mathematical state, submitted
artifacts, and project-specific guardrails. Never import another project's
claims, routes, hashes, or assumptions.

For a new project assess the owner's question, primary sources, feasibility,
exact target, alternative mechanisms, and cheap tests. Obtain approval of the
target, main route, assumptions, and exploration scope before construction.
The empty S0 scaffold is not mathematical approval. Do not create role tasks.

## Continuous research

An ordinary session uses only `brief.md`, `work.md`, and a v1.3 `manifest.json`.
Do not copy the whole template directory. Local candidates, cheap falsification
checks, calculations, source notes, repairs, and the closing mathematical
summary belong in one continuous work note. No per-step dispatch, status,
learning-note, or separate role report is required. Run candidate preflight
before long construction: canonical topology, exact operator/boundary calculus,
first-variation scale, quotient by existing derivation roots, quantifiers and
blind directions, localization, and exact failure scope.

Index durable evidence in `Txxx.json` only when needed for review or a proposal;
the brief may serve as dispatch. For formal use, the artifact is the frozen
reviewed proof snapshot rather than the continuous work note. Freeze submitted
claim/proof snapshots and preserve their raw bytes. Work notes remain appendable;
link exact snapshots rather than binding review to the whole note. Mathematical
corrections need a new version. Validate after freezing evidence.

## Mathematical feedback before and during exploration

Read [research-feedback.md](../../../docs/research-feedback.md) when using
executable checks, claim revisions or task comparisons. Before long derivation,
fill the brief's intended-answer contract: quantifiers, parameter/dimension
regime, topology, uniformity, hypotheses and excluded easier interpretations.
Check exact source locations and assumption matches; keep correctness,
applicability and novelty distinct. Record meaning_audit without changing the
approved theorem target.
For a long calculation or a change of coordinates, use the identity, coordinate
transfer and source-matching prompts in WORKFLOW.md in the existing brief or
work note. Record the scope of failed tests and separate a source that motivated
the construction from an analogy found later.

For useful sign, algebra, scale or finite counterexample checks, freeze a
candidate/evaluator/input plan. Inspect with checkctl.py; use --run --output only
inside existing authorization. This explicitly executes the trusted evaluator,
without a shell, with timeout/raw-output/input-integrity receipts. A runtime
failure is inconclusive; a numerical/finite check never becomes a general proof.
No CAS/Lean toolchain or mathematical certificate is bundled. Separate evaluator
maintenance from candidate search and consider withheld/adversarial tests.

Retain the owner's current model/settings. Add compute_steps only when escalating:
reason, expected information, time/optional cost limit, stop condition and actual
observed outcome. Unknown cost is null. No automatic model/delegation/chat changes
or model budget enforcement is implied; host permissions and owner scope apply.
Record overruns as stopped, and stop when there is no credible information gain.

At closure record progress: closed gap, new exclusion, external result, useful
distinction or explicitly none, with exact mathematical explanation. Reused roots
or renamed candidates do not count as new evidence. Two none sessions trigger
route review before more construction; structural and three-session limits stay.

Before adding process, compare representative owner-supplied tasks under frozen
inputs and budgets. benchctl.py prepares input-only packets, blinded labels and
separate human scores for correctness, target meaning, exposition, attribution,
reproducibility, review time and compute cost. Keep model/effort fixed when
comparing workflows; include every failure/abstention. Host context/filesystem
isolation is required to keep owner reference answers out of runner access.
Tools never call models or grade proofs; mechanics-only examples establish no
research-productivity benefit. Keep private project material out of this source.

## Independent review at key gates

Review is required for a key identity, core estimate, claimed gap closure,
formal claim promotion, or owner request. Routine exploration uses self-checks.
Mark `critical_review_required` in the manifest. In a fresh context or by a human
reviewer, freeze a baseline from only the question, conventions, and allowed
inputs before disclosing the proof. Then compare against the frozen candidate.
Record v1.1 `review.json`, with question, baseline, proof candidate and assessment
hashes, reviewer/context, roots/overlap and verdict. Bind claim_id, revision and
claim_record to an exact provisional claim-evidence snapshot. Index snapshots
in claim_records and reviews in critical_reviews. The candidate equals that
snapshot's proof; summary/work may be a different mutable note. Exact versions
and assessments may be reused across sessions by reference. A substantive
revision names supersedes; transitive dependents require recheck before new
formal use, without automatic canonical promotion or demotion.

A role name, model change, fresh context, or validator success is not evidence
of mathematical independence. Disclose overlapping roots and any prior proof
exposure. Mark `self_check` when the independent read order was not respected.
Only independent review with `survives_current_attacks` can support decisive
support or a formal promotion proposal; critique alone never proves a claim.
If a required review is unavailable leave the conclusion pending; continue
unrelated authorized exploration, without treating self-check as a substitute.

## Closure, proposals, and route review

Close with the target, exact result or scoped obstruction, decisive argument,
proof consequence, remaining gap, and next question in the work note and owner
reply. A session without a proposed formal change needs no transition files.
When seeking a change, add `state_update_proposal.md` and `state-transition.json`,
link exact frozen evidence and independent review, and validate. Use local Txxx
evidence IDs in evidence_records for formal changes; each indexed record links
the exact reviewed proof version and its derivation roots, covering every
changed proof item. Explicitly provisional planning entries need owner approval but no independent proof audit. Do not change
canonical conclusions, claim status, main route, hypotheses, global notation,
or manuscript without explicit human approval. Manuscript work needs specific
authorization and the supporting evidence gate.

Inside approved exploration scope proceed without repeated approval. Material
changes to target, main route, hypotheses, or scope need a new owner decision.
After two declared no-information sessions, three sessions without independently
reviewed decisive support, repeated obstruction/roots, structural failure, circularity, or an owner request, pause
new construction and perform route review with an obstruction-driven primary
literature refresh and independent assessment. Use one route-review note plus
its decision index; no permanent role handoffs. Only the owner approves the
post-review continuation or route decision.

After approval update affected canonical records and their machine mirror,
then validate. Avoid manually repeating the same mathematical result across
indexes, logs, maps, and summaries; use links. `report` generates an optional
Markdown reading copy; `report --format tex` or `--format pdf` exports additional
formats when requested. PDF tooling never blocks ordinary research.

## Read-only inspection and evidence rules

Use `summary`, `status CLAIM_ID`, `blockers CLAIM_ID`, and `dashboard` for the
approved mirror; `validate-proposal` and `dashboard-proposal` for visibly
noncanonical mapping previews. The dashboard language switch does not translate
or modify claims. The ledger and STATE remain authoritative over the mirror.
Preserve exact/formal/conditional/conjectural/numerical/external/rejected status,
scoped route failures, evidence lineage, and strict dependencies. Only
`formal_exact`, `established`, and `verified` discharge strict prerequisites.
A route rejection never rejects its target theorem automatically.

Read [state-model.md](references/state-model.md) when changing records or schemas.
Normal research replies contain mathematics; mention technical details only
when requested or necessary to explain a reliability problem. Workflow
maintenance requests can be answered in software terms.
