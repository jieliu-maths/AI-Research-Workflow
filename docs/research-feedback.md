# Mathematical feedback in the single-window workflow (3.1)

Ordinary sessions still have brief.md, work.md and a v1.3 manifest.json. The
following records are conditional, not a new startup checklist. Canonical state,
claim status, hypotheses, main routes, global notation and manuscripts retain
explicit owner approval. No command below promotes mathematics automatically.

## 1. Verify the intended question

Fill the brief's “What counts as answering the question” before long derivations:
quantifiers; parameter/dimension range; topology; uniformity; allowed hypotheses;
excluded weakenings; exact source theorem/location, applicability and remaining
difference. Set meaning_audit to matched only after checking this correspondence.
A known theorem applied correctly may be valuable without being novel. Novelty
labels are judgments to audit, not machine certificates.

## 2. Execute a decisive check

A check-plan.json uses schema 1.0: kind (symbolic, scale, finite_check, numerical,
formal_certificate), exact scope, hashed candidate/evaluator/inputs, command as
an argument array, timeout_seconds (positive, at most 300), evaluator_review and
limitations. The command must include {evaluator}; optional placeholders are
{python}, {candidate}, and {input:0}, etc. The evaluator prints one JSON object
with outcome passed/failed/inconclusive and relevant witnesses. A nonzero exit,
timeout or changed input is inconclusive. No shell is invoked.

```bash
python3 tools/checkctl.py calculations/check-plan.json
python3 tools/checkctl.py calculations/check-plan.json --run --output calculations/check-result-v1.json
```

The first command only inspects; the second executes an already-authorized
trusted evaluator within the host's permissions. It supplies no new sandbox,
network policy, model budget enforcement or guarantee of checker correctness.
It verifies hashes before/after execution, detects collateral edits to registered
canonical files, records raw output and measured time,
and refuses to overwrite an existing result. Detected collateral edits make the
result inconclusive and must be investigated; they are not silently restored. Link the result in manifest.checks
using its hash. Candidate generation must not quietly rewrite the evaluator.
Use independently reviewed checkers and adversarial/withheld cases where useful.
Exact arithmetic is preferred for a finite certificate; numerical evidence
cannot certify an unbounded theorem. External Lean/CAS tools are optional;
their installation and statement correspondence are not supplied by this runner.

A runnable standard-library demonstration is in examples/ai4math/checks/:
make_plan.py freezes plans for rational-polynomial identity and a failing
monomial scale test. These teaching checks certify only their explicitly
specified algebra/monomials, not an analytic theorem.

## 3. Escalate computation when it can answer a question

Optional manifest.compute_steps entries record action, reason,
expected_information, max_seconds, max_cost_usd (null if no known cost limit),
stop_condition, status (planned/completed/stopped), elapsed_seconds, cost_usd
(null when unknown) and outcome. Actions are increase_reasoning, change_model,
independent_candidates and external_verifier. Preserve owner-selected defaults;
use a stronger model or more attempts only for a defined missing information
source. No automatic model changes, delegation, billing or chat creation are
implemented. Overruns are recorded as stopped and count in comparisons.

## 4. Review the exact claim/proof version

At a key gate, use the conditional claim-evidence.json template, for example
runs/R001/P001-v1.json. It freezes an exact statement, quantifiers, hypotheses,
regime, function space, intended target hash, excluded weakenings, meaning audit,
prior-work comparison, novelty standing, proof hash and derivation roots.
Versioned depends_on entries bind existing prerequisite claim snapshots; the
canonical proof ledger still owns the mathematical dependency graph.

Index claim snapshots in manifest.claim_records and v1.1 reviews in
manifest.critical_reviews. Each review binds claim_id, revision, claim_record,
question, independent baseline, proof candidate, assessment, read order, roots
and verdict. The proof candidate equals the snapshot's proof, not the session
summary. Changing statement/hypotheses/target/dependencies creates a new snapshot
and requires its own assessment, even if proof bytes happen to be identical.
A surviving independent assessment plus matched meaning is required at a key
formal gate; it is never a proof or owner approval by itself.

Reuse an exact snapshot and review across sessions by hash. For a substantive
correction create v2 with change_kind substantive and supersedes pointing to v1.
All transitive version dependents are marked for recheck and withheld from new
formal use; canonical status is not silently changed. Editorial changes are
explicitly declared and must not hide a mathematical change. Inspect downstream
canonical claims with:

```bash
python3 tools/researchctl.py affected P001
```

For a transition proposal, cite manifest-indexed local Txxx IDs. Those records
must identify changed proof_items and reference the exact independently reviewed
proof version. A prose summary or unrelated reviewed lemma cannot cover another
claim. Open planning entries retain the lighter approval-only path. Historical
v1.2 sessions keep their old summary-bound review contract and are not rewritten.

## 5. Stop when information stops increasing

Set manifest.progress.kind to gap_closed, new_exclusion, new_external_result,
new_distinction or none, and explain the exact change. Candidate class,
obstruction_key, derivation_roots and repeat_reason help identify repeated work.
Do not call a renamed formula a new excluded class. Two consecutive none sessions
on a route trigger review before more construction, alongside the three-session
and structural-failure rules. New negative information can be valuable even
without decisive support. The route review refreshes primary literature and
compares mechanisms; only the owner approves post-review continuation/change.

## 6. Compare actual tasks under frozen inputs

Use evaluation/suite-template.json with owner-supplied historical tasks (aim for
10–20 representative tasks, not selected successes). Supply question/context
hashes, a hidden human reference, category and expected disposition for every
case; configure two or more alternatives. Declare factor workflow/model/
reasoning_effort/exploratory, comparison matched_budget/exploratory and a shared
budget. For workflow comparisons model and reasoning must be identical. Do not
vary many factors and attribute the difference to the workflow alone.

```bash
python3 tools/benchctl.py prepare evaluation/my-suite.json --output-dir evaluation/packets-v1
python3 tools/benchctl.py blind evaluation/submissions-v1.json --output-dir evaluation/blind-v1
python3 tools/benchctl.py score evaluation/blind-v1/owner/key.json --grades evaluation/blind-v1/review/grades.json
```

prepare copies only question/context into each runner's inputs packet; reference
answers, expected outcomes and source data stay in owner/. Give the runner only
its input packet and arrange actual filesystem/context isolation in the host.
This tool cannot prevent an agent with broad project access reading owner data.
It never invokes models or services. A submission record contains a frozen
suite reference and submissions covering every case/configuration pair:
case_id, configuration_id, hashed answer, disposition (accepted/rejected/
conditional/open/abstain), and usage.wall_seconds/cost_usd. Include abstentions
and failures instead of dropping them. Usage receipts are runner-reported,
not independently certified API bills.

blind shuffles answers, includes the question and allowed context, strips
configuration labels, and creates a blank grades-template.json. Keep owner/key
away from graders. Content can still self-identify, so label blinding is not
proof of reviewer blindness. In grades.json human reviewers fill correctness,
exposition and attribution separately (0/1/2), meaning_matched, gap_closed,
reproducible and measured review_minutes. A claimed gap closure needs full
correctness and intended-target match. Score reports correct results, reviewed
gap closures, false accepts, meaning errors, exposition/attribution, reproducible
results, wall/review time, known costs, missing cost data and budget overruns.
Do not treat unknown costs as zero or these grades as canonical acceptance.

The demonstration in examples/benchmark/ tests packet/grade mechanics only.
No controlled research-effectiveness experiment or private historical benchmark
has been performed by this source repository.

### Paired checks for proof and revision tasks

Use short synthetic cases before expanding the protocol or adding a checker.
Freeze the following invariants and the owner reference in separate packets.

| Change one input | Expected response |
| --- | --- |
| Reorder two calculus derivations with the same decisive pairing, leaving the functional and time variable fixed | Reproduce the requested derivative in both cases, retain each endpoint and coefficient derivative, and identify their shared source of control. |
| Change from fixed normal label to fixed physical height, keeping the tangential estimate fixed | Write the composition map. Transfer the radius only when the induced complex normal displacement lies inside the supplied normal domain. Keep any failure scoped to the tested estimate. |
| Keep the revised proof fixed and change only the response letter's confidence | Judge the proof issue the same way using the frozen criterion. |
| Keep the reply fixed and replace the decisive estimate by one with a parameter-dependent constant | Change the judgment when the fixed criterion requires a uniform constant. Cite the estimate that changes it. |

Three small cases can seed the packets:

- **Product-rule target.** With real functions \(a,b,\lambda\) of \(s\),
  differentiate \(\lambda(a+b)^2/2\) and retain both endpoint squares and the
  mixed term. Compare the expanded calculation to one using
  \(w=a+b\). The term \(\lambda'(a+b)^2/2\) must appear in both. The
  two calculations use the same identity.
- **Coordinate transfer.** Give the chart \(y=\eta+x\) and
  \(F(x,\eta)=g(\eta)\). At fixed \(y\) the composition is \(g(y-x)\).
  In one arm assume only smooth real \(g\), with no analytic normal control.
  In the other give a holomorphic normal disk \(|\eta-y|<r\), so the
  composition is holomorphic for \(|x|<r\).
- **Revision review.** Require \(x^2\le C E\) with \(C\) independent of
  \(0<\varepsilon\le1\), for nonnegative \(E\). Contrast an available
  estimate \(x^2\le E\) with \(x^2\le E/\varepsilon\). Use the same
  reply claiming a fix in both arms. In a separate pair, keep the weaker
  estimate fixed and vary only the confidence of the reply.

Place the expected reasoning only in the hidden references. Track wrong-target
answers, false gap closures and human checking time. Source/package checks and
evaluator replay measure separate things.

## Evidence behind these design choices

These are design inferences, not a claim that the cited systems validate this
implementation or guarantee improvements on analysis/PDE problems.

- Aletheia describes iterative generation/verification/revision and failures of
  intended-question interpretation: https://arxiv.org/abs/2602.10177.
- AlphaEvolve studies construction search with executable evaluation across
  multiple mathematical domains: https://arxiv.org/abs/2511.02864.
- Aristotle combines informal reasoning with formal proof search:
  https://arxiv.org/abs/2510.01346.
- The formative AlphaEvolve user study reports evaluator gaming, versioning
  friction and diagnosis needs; it is not a controlled productivity trial:
  https://arxiv.org/abs/2605.05921.
- First Proof's October 2026 comparison separates correctness, exposition and
  attribution and reports differing compute costs:
  https://1stproof.org/third-batch-press-release.html.
