# Changelog

## 3.1.0

- Add a noncanonical recovery note convention for parallel proof series and
  working drafts. Recognize historical manuscript delivery records without
  admitting them as research evidence or weakening research-manifest checks.
- Extend existing preflight prompts for exact calculation targets,
  coordinate transfer, scoped counterexamples, and source provenance.
- Add intended-question/quantifier/regime/topology and exact source-applicability
  checks before long derivations, separate from correctness and novelty claims.
- Add explicit opt-in frozen evaluator execution, raw receipts, timeout and input
  integrity checks, plus rational-polynomial and scale teaching examples.
- Record bounded compute escalation only when used; unknown cost stays unknown.
- Add manifest 1.3, provisional claim/proof revisions and review 1.1, independent
  of mutable work summaries. Bind formal changes to exact reviewed claim IDs.
- Detect substantive prerequisite revisions transitively without changing
  canonical status; add a read-only affected-claim query.
- Trigger earlier route review after two declared no-information sessions;
  preserve three-session/structural-failure limits and owner decisions.
- Add frozen input packets, label-blind human grading and separate quality,
  error, reproducibility, time and cost comparison metrics. Demonstrations test
  mechanics only; no research-effectiveness result is claimed.
- Preserve historical manifests/reviews, project-state schema 2.1, raw evidence,
  mathematical guardrails and human approval during transactional upgrades.

## 3.0.0

- Make one research window the default; remove permanent three-role task setup,
  role-registry prerequisites, dispatch/return loops, and duplicated run reports.
- Use brief.md, work.md (including the mathematical summary), and manifest.json
  for ordinary sessions. Evidence, review, transition, and route-review files
  are conditional. Move retired templates into a legacy reference directory.
- Add manifest schema 1.2 and independent review records tied to frozen question,
  baseline, candidate, and assessment. Self-checks cannot clear a key evidence
  gate; formal claim changes still require review and explicit human approval.
- Reduce the new-project skeleton and recover from short approved STATE first.
  Keep source proofs, hypotheses, quantifiers, derivation roots, scoped failures,
  strict dependencies, candidate preflight, and obstruction-driven route review.
- Make Markdown reading copies optional; LaTeX/PDF are explicit report exports.
- Preserve historical manifests, task records, role registries, mathematical
  state, and instantiated runs. Adopt exact v2.7.0 protocol documents as managed
  assets; locally edited protocols conflict instead of losing guardrails.
- Keep project-state schema 2.1 and existing mathematical status semantics.
  This is a workflow refactor, not measured evidence of better theorem solving.

## 2.7.0

- Position the public release around AI4Math with portable English/Chinese
  documentation, role prompts, a primary-source landscape review, and MIT licensing.
- Add a portable evidence-bundle inspector; it checks metadata and file integrity,
  never replays commands or promotes mathematical/scientific claims.
- Add a primary-source applicability template for exact theorem locations,
  hypothesis-by-hypothesis matching, derivation roots, and independent review.
- Add offline bounded-arithmetic and synthetic held-out experiment examples.
- Add a separate, experimental fresh-directory AI4S scaffold with a scientific
  protocol, provenance, baselines, uncertainty, and frozen experiment plans.
  AI4S migration, managed upgrades, graph validation, and dashboards are not supported.
- Check common publication leaks across the source tree and configure CI for
  Python 3.10/3.12 on macOS/Linux. Preserve existing AI4Math state semantics.

## 2.6.2

- Give the standalone workflow repository a source-only identity marker and a
  `workflow identify` check; installed mathematical projects never receive the
  marker.
- Reject installation or upgrade from a directory that is not the verified
  standalone library, even if an older project's `source_hint` points there.
- Resolve portable prompts from a verified Codex saved project before treating
  a legacy `source_hint` as a candidate.

## 2.6.1

- Render the actual standalone-library path into prompt files installed in a
  project, so copied prompts contain executable commands instead of an
  unresolved `<WORKFLOW_LIBRARY>` placeholder.
- Let the portable source prompt resolve the library from an installed
  project's `source_hint` or the Codex saved-project list before asking the
  owner for a path.
- Ignore Finder's `.DS_Store` metadata during standalone source checks.
- Preserve validation of older task-order prerequisites and undecided route
  reviews while keeping new mathematical dependencies in `claim.depends_on`.

## 2.6.0

- Made the current owner-facing task `0 Director` and restricted new task
  creation to the two top-level peers `1 Researcher` and `2 Critic`, after
  owner approval of the exact target and route.
- Added a mandatory primary-source refresh to route evidence reviews before a
  continuation or route-change recommendation reaches the owner.
- Added real Draft 2020-12 subset validation for every shipped project-state,
  proposal, role, run, task, orchestration, transition, and route-review
  schema.
- Refused managed writes through symlinked destination ancestors and added a
  regression test proving that no outside file is created.
- Added `workflow self-check` for the standalone source repository.
- Added consolidated Markdown, LaTeX, and PDF research summaries through
  `researchctl report`, with freshness checks after mathematical updates.
- Upgraded the complete Markdown run-template set to version 2.4.0 and the
  route-review record to schema 1.1.

## 2.5.1

- Made rollback continue across an unwritable unchanged managed file, restoring
  every other reachable destination before reporting any residual failure.
- Restricted standalone-source tests to the source repository so the same
  managed test suite remains valid after installation into a mathematical
  project with project-specific guardrails.

## 2.5.0

- Extracted the reusable workflow into a standalone, project-neutral source
  repository.
- Added the `workflow` launcher so callers do not need to specify Python or a
  source-project path.
- Removed source-project paths, theorem identifiers, formulas, and examples
  from reusable prompts and role templates.
- Added regression tests for project neutrality and standalone initialization.
- Preserved the 2.4.1 bilingual mathematical dashboard, peer-role task model,
  Director return loop, route evidence review, candidate preflight, owner
  route gates, notation disclosure, and mathematics-only human reporting.
