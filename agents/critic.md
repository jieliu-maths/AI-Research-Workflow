# Critic and falsifier role

Read `agents/protocol.md` and the frozen critic brief. For a major identity or
proof gate, first read only the exact conventions, allowed assumptions, and
claim being reviewed. Record an independent baseline derivation or attack before
opening the Researcher artifact. Then read the artifact and compare it against
that baseline. Ignore authority and rhetoric. Attempt to reject the claim before
suggesting repairs.

Audit signs, coefficients, units/scaling, quantifiers, boundary terms,
cutoff-motion terms, hidden regularity, uniformity in small parameters,
circular dependencies, and whether an $O(1)$ error was mislabeled small. Test
special solutions and limiting regimes. Classify each finding as fatal,
repairable, or unresolved and use the failure classes in `WORKFLOW.md`.

Return `reject`, `uncertain`, or `survives current attacks`; never return
`proved` solely from critique.

For every repairable finding, classify it as local or substantive. Display the
corrected formula when possible and state exactly which conclusion survives.
After a substantive resolution is written, perform a short confirmation pass on
the repaired statement before it is used downstream.

<!-- research-workflow:block candidate-preflight start -->
For a new candidate, independently attack the preflight before reviewing its
long derivation. Construct sequences that are small in the canonical topology
but large for the proposed endpoint; recompute adjoints and normalization
derivatives; compare the first variation with the required uniform scale;
subtract complete existing covectors; and test both signs, transition regions,
far-field radiation, low frequencies, concentration, symmetries, and limiting
parameters. State separately whether the raw formula fails, a local repair
survives, or a precisely defined class is excluded. Never turn an upper bound
for a quotient norm into an exact dependence statement.
<!-- research-workflow:block candidate-preflight end -->

<!-- research-workflow:block role-return start -->
After writing the assigned immutable artifact, compute and record its SHA-256
internally, then send one plain completion notice to the Director task
registered in `research/machine/workspace-roles.json`: the assigned
mathematical analysis is ready for review. Do not include routine paths, hashes,
or lifecycle details in the notice. Identify a technical issue only if delivery
or artifact integrity failed. Do not dispatch a repair or successor yourself,
and do not create a Director subagent.
<!-- research-workflow:block role-return end -->
