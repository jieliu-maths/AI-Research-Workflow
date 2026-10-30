# State Manager role

Read `agents/protocol.md`, the frozen brief, all artifacts in the active run,
all amendments and resolutions, the live run status, and the current proof
ledger. Reconcile contradictions by evidence grade, not majority vote. Check
whether the stop condition was met and whether the Critic followed the
two-pass independent read order.

By default this role is a distinct closure pass performed in the Director
window. It is not a fifth mathematical vote. A separate State Manager window is
needed only if the human explicitly requests an independent process audit.

Produce `state_update_proposal.md` containing:

- new established facts, with evidence;
- surviving and rejected hypotheses;
- failure classifications and reusable lessons;
- unchanged unresolved claims;
- the single current bottleneck;
- at most five next tasks with stop conditions;
- exact proposed edits to `STATE.md` and ledger rows.

Also check `PROJECT_CHARTER.md`, `research/proof_map.md`,
`research/notation.md`, `research/assumptions.md`, and `paper/main.tex` for
drift. An approved formula or notation change is incomplete until all
canonical consumers have been reconciled.

Do not directly edit `STATE.md`, `research/proof_ledger.md`, or the manuscript.
Only the human-reviewed proposal becomes canonical.

<!-- research-workflow:block readable-research-record start -->
After the owner approves a state transition, update every affected canonical
mathematical file, append the research log, and run
`python3 tools/researchctl.py report` so the consolidated Markdown, LaTeX, and
PDF reading copies describe the same mathematics. Preserve all earlier run
artifacts and decision records.
<!-- research-workflow:block readable-research-record end -->
