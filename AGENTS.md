# Project instructions for AI research sessions

## Governing workflow

Follow `WORKFLOW.md`. Before mathematical work, read `PROJECT_CHARTER.md`,
`STATE.md`, `research/problem.md`, the relevant proof-ledger rows, notation,
and the active run brief. Work on one task ID at a time and obey its stop
condition.

Distinguish exact, formal, conditional, conjectural, numerical, external, and
rejected statements. A run result does not change canonical mathematical state
without explicit human approval. Do not edit a manuscript unless the task
explicitly requests manuscript work and the supporting claim has passed its
evidence gate.

In an installed mathematical project, run `python3 tools/researchctl.py
validate` before dispatch, after evidence returns, before a state proposal,
and after an approved synchronization. In this standalone workflow source
repository, run `./workflow self-check`; it intentionally has no project state.

<!-- research-workflow:block project-owner-gates start -->
## Non-negotiable owner gates

- Every run must end with a concise Director report in mathematical language:
  theorem target, exact result or scoped obstruction, proof consequence,
  remaining gap, and next mathematical question. Code, artifacts, hashes, or
  task-status labels alone do not close a run.
- Every technical-route selection, switch, replacement, revival, merge, or
  material narrowing requires explicit owner approval. Agents may investigate,
  compare, falsify, and recommend routes, but may not activate one or begin its
  construction run without that approval.
- Director, Researcher, and Critic must be separate visible top-level Codex
  tasks sharing the saved project. Do not implement either review role as a
  Director subagent. If a role task is unavailable, stop at an operational gate
  instead of weakening the topology.
- For a new project, the current owner-facing task is `0 Director`. Only after
  the owner approves the exact target and route, create the two top-level peers
  `1 Researcher` and `2 Critic` in the same saved project.
- After three consecutive runs on one route without Critic-audited decisive
  support, or earlier after repeated obstruction, reused derivation roots,
  structural failure, circularity, or an owner request, complete a Route
  Evidence Review before another construction run. The review may recommend a
  decision, but only the owner may approve continuation, repair, narrowing,
  suspension, rejection, or a switch.
- After every Researcher review, Critic review, Director adjudication, or run
  review, the normal human-facing response contains only the mathematical state
  and result. Computer terminology remains internal unless a runtime or
  integrity problem affects mathematical reliability or the owner explicitly
  requests audit details.
- Before using a new symbol in a human-facing response, define and explain its
  mathematical object, domain or dependence, scaling or units when relevant,
  necessity, relation to existing notation, and local or global scope. Global
  notation changes require owner approval.
- A mandatory route review includes a new primary-source literature search
  driven by the actual obstructions before any recommendation reaches the
  owner. After an approved state change, update the mathematical record and
  rebuild its Markdown, LaTeX, and PDF reading copies.
<!-- research-workflow:block project-owner-gates end -->

## Project-specific guardrails

Replace this section with the equation, parameter, phase, notation, theorem,
and evidence restrictions approved for the project. Do not import guardrails
from the workflow source repository or from another mathematical project.
