# AI4S experimental protocol

1. **Specify.** Freeze a falsifiable hypothesis, domain, outcome variables,
   units, effect of interest, baseline, exclusions, and the cheapest decisive
   failure test. Record data access, compute/time budget, and stopping rule.
   Obtain owner approval of the target and route before execution.
2. **Source.** Record dataset origin, version, checksum, license, access
   restrictions, preprocessing, missingness, and known contamination risks.
   Literature assertions need exact passages and matched assumptions.
3. **Freeze.** Copy `experiments/plan-template.md` into a new run directory.
   Commit code/environment versions, seeds, split identifiers, controls,
   ablations, statistical method, and the sealed final evaluation protocol.
   Append and justify deviations; preserve the original plan.
4. **Construct.** Researcher executes within the approved scope. Keep inputs,
   code, raw outputs, runtime versions, cost, failures, and exact commands.
   Run unfamiliar generated code in an appropriate isolated environment.
5. **Critique.** Critic first writes an independent expectation from the frozen
   question without reading the result, then audits leakage, uncertainty,
   controls, multiple comparisons, robustness, and claim scope. Matching model
   names or different task names do not establish independent evidence.
6. **Decide.** Director states the hypothesis, exact observed result, uncertainty,
   surviving explanation, excluded alternatives, remaining gap, and next
   scientific question. Prepare a state proposal; only owner approval changes
   `STATE.md` or `research/claim_ledger.md`. Never overwrite raw role artifacts.
7. **Reassess.** Review the route after three nondecisive runs, repeated failure,
   leakage, circular reasoning, or an owner request. Refresh primary sources
   before recommending continuation, repair, narrowing, or switching. The owner
   chooses the route. Accepted empirical findings remain scoped to their domain.

`python3 tools/evidencectl.py experiments/R001/evidence.json` checks a portable
evidence bundle's metadata and file hashes. It never replays a command, proves
a hypothesis, checks statistical validity, or approves a state transition.

This profile currently has no automated claim graph, workspace registry
validation, dashboard, reports, migration, or managed upgrade support. Keep
its qualitative, numerical, observational, and intervention evidence distinct.
Do not run the AI4Math `researchctl` or `workflow upgrade` against this profile.
