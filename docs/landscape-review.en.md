# Research workflow landscape and positioning

Reviewed **2026-10-30**. [中文](landscape-review.zh-CN.md).

## Scope and method

This is a targeted design review, not an exhaustive survey or a comparative
performance benchmark. We inspected primary project repositories, license
files, papers linked by the authors, and official product/research reports.
We did not run the external systems or purchase private services. Product
access and licenses can change. “Hosted / no complete implementation located”
means no full open implementation was identified in the reviewed sources; it
is not proof that none exists. Published success and productivity claims are
vendor/author reports, not measurements performed here.

The relevant comparison separates four layers: (1) models that generate
mathematics, (2) proof/experiment execution, (3) literature and data tools,
and (4) long-lived evidence and research decisions. This project chiefly
addresses layer 4. A shared word such as “agent” does not make the systems
interchangeable.

## Representative systems

| System and primary source | Availability observed | Strength relevant here | Design consequence for this workflow |
| --- | --- | --- | --- |
| [QED](https://github.com/proofQED/QED), [license](https://github.com/proofQED/QED/blob/main/LICENSE) | MIT source; external model CLIs | Natural-language proof planning, subgoal DAGs, structural/citation checks, detailed verification, and controlled retries | A direct AI4Math comparator. Learn fine-grained citation and statement checks; distinguish an automated proof loop from this repository's owner-approved route and state decisions. Neither LLM review is a proof kernel. |
| [MathResearch Ledger](https://github.com/Caie777/math-research-ledger) | Apache-2.0 source with MCP interfaces | Persistent mathematical objects, versioned dependencies, bounded context, provisional checkpoints, and separate human acceptance | A direct evidence/memory comparator with overlapping goals. Our next gaps include bounded context restoration and dependency-version freshness; differentiate the explicit role/preflight/run-review contracts, not ledger terminology. |
| [Lean Copilot](https://github.com/lean-dojo/LeanCopilot) | MIT source; separate models/toolchain | Native Lean tactic suggestions, premise selection, and proof search | Accept formal outputs with pinned toolchains, axiom reports, and statement-mapping review. It is not a replacement for a multi-session natural-language proof ledger. |
| [LeanDojo-v2](https://github.com/lean-dojo/LeanDojo-v2) | Apache-2.0 framework; external dependencies/models | Lean repository tracing, datasets, training, retrieval, and prover deployment | Plan an external adapter rather than recreate a training/proving stack. Training needs and data provenance differ from project governance. |
| [DeepSeek-Prover-V2](https://github.com/deepseek-ai/DeepSeek-Prover-V2) | Released weights/examples under a distinct [model license](https://github.com/deepseek-ai/DeepSeek-Prover-V2/blob/main/LICENSE-MODEL) | A specialized Lean proof-generation model | Track model and artifact identity; do not confuse open weights or generated code with a complete open research workflow. |
| [Aletheia / Gemini Deep Think](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/) | Official research description; full agent implementation not located | Candidate generation, natural-language verification/revision, and explicit failure | Make abstention and scoped failure first-class. Natural-language verification still needs independent scrutiny. No model-level parity is claimed here. |
| [Aristotle](https://www.harmonic.fun/aristotle/) and [mathematics research access](https://aristotle.harmonic.fun/sponsorships) | Hosted commercial verification; no complete backend located | Machine-checked formal artifacts and explicit proved/refuted/open outcomes; current public landing page emphasizes C/Verilog, while research program mentions Lean | Treat product capabilities and research access separately. Preserve exact checker assumptions and the gap from informal intent to formal specification. An SDK is not an open backend. |
| [The AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2), [v3 / Agentic Scientist](https://github.com/SakanaAI/AI-Scientist-v3) | v2 currently has a [use-restricted source license](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/LICENSE); v3 advertises Apache-2.0 | Experiment search and paper pipelines; v3 includes baselines, ablations, sealed final evaluation, run records, and container execution | Borrow explicit evaluation separation, reproducibility, and runnable examples. Do not describe all Sakana versions as identically licensed or use paper generation as the correctness gate. |
| [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory), [license](https://github.com/SamuelSchmidgall/AgentLaboratory/blob/main/LICENSE) | MIT source, externally supplied models | Literature, experimentation, reporting, and configurable human involvement | Show an accessible end-to-end path; our current gap is automatic execution and connectors. A human-in-the-loop design is not unique to this repository. |
| [PaperQA2](https://github.com/Future-House/paper-qa) | Apache-2.0 source; external model/search services | Scientific-document retrieval, evidence gathering, and cited synthesis | A future literature adapter should retain exact passages, search scope, and applicability audits. Retrieval scores do not prove a mathematical lemma. |
| [Google AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/), [2026 update](https://research.google/blog/a-new-era-of-innovation-google-research-at-io-2026/) | Hosted/research access; full implementation not located | Multi-agent hypothesis generation, reflection, ranking/evolution, and expert collaboration | Use diverse routes and cheap falsification tests, but never promote tournament rankings to proof status. Current public work extends into Gemini for Science. |
| [Kosmos / Edison](https://advances.edisonscientific.com/research/announcing-kosmos/), [data-access update](https://edisonscientific.com/news/expanding-kosmos-data-access-capabilities) | Hosted commercial platform; full implementation not located | Structured world models, linked literature/code evidence, and scientific-data retrieval | Traceability is already a competitive capability, not our exclusive invention. Differentiate with locally inspectable records, explicit proof dependencies, and owner-controlled acceptance. |
| [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), [2026 update](https://deepmind.google/blog/alphaevolve-impact/) | Hosted/research system; full production implementation not located | Evolutionary code search guided by automated evaluators | Define cheap executable falsifiers and distinguish optimizing a score from proving a universal statement. Use it as a potential candidate source, not a proof authority. |

## What is distinctive in the current repository

The strongest positioning is an **AI4Math-first, owner-controlled research
record and evidence workflow**, especially for long natural-language proofs
whose analytic details are not yet completely formalized. The distinction is
the combination, not a claim that each ingredient is novel. QED and MathResearch
Ledger are especially close comparators, and the latter already separates
verification, provisional records, and human acceptance:

1. Claims, technical routes, and execution runs are separate objects. A failed
   candidate can exclude a precise class without rejecting the theorem target.
2. Strict proof prerequisites, evidence lineage, and circularity are explicit.
   Two agents sharing a decisive derivation root do not create two independent
   arguments.
3. A Critic's blind-first pass, mathematical preflight, route-review triggers,
   and owner approval are written contracts supported by consistency checks.
4. Records are ordinary local text/JSON, with a readable bilingual proof map
   and conflict-preserving upgrades. A host or model outage need not erase them.
5. A distinction between record consistency and mathematical truth is central.
   No software status silently discharges a proof obligation.

These are design properties found by inspecting this repository. They do not
establish superiority in correctness, research speed, or theorem difficulty.
Separate tasks also do not mechanically guarantee independent reasoning or
that an agent obeyed its reading order.

## Gaps and priorities

| Priority | Gap | Change in 2.7.0 | Remaining work and acceptance criterion |
| --- | --- | --- | --- |
| P0 | Private-machine assumptions and inaccessible entry path | Portable bilingual documentation, MIT license, source-publication check, clean public snapshot | Keep every documented command runnable in a fresh clone; do not publish historical private context. |
| P0 | External tools lack a concrete evidence-return contract | Shared inspector for finite/formal/numerical/source evidence bundles plus a primary-source applicability template | Add independently replayed Lean/CAS adapters; demonstrate rejection of placeholders, untrusted axioms, and statement mismatch. The current inspector checks metadata/hashes only. |
| P0 | New users cannot see the proof/computation boundary | Offline 100-case exact arithmetic teaching fixture | Add reviewed examples from several mathematical areas; never use finite enumeration to claim unbounded proof. |
| P1 | AI4S requirements are not mathematical proof requirements | Separate experimental scaffold, frozen experiment plan, synthetic regression demo with a baseline and held-out evaluation | Add scientific claim schemas, independent repeats, uncertainty, data connectors, and migration only after fixtures validate their semantics. |
| P1 | Protocol complexity and manual operations impose overhead | Short entry points, explicit supported-host boundary, bilingual role prompts | Measure onboarding effort and accepted progress per human review hour; avoid removing owner gates merely to increase autonomy. |
| P1 | No evidence of workflow effectiveness | Honest capability/maturity matrix and evaluation plan | Run a predeclared comparison against single-chat and minimally structured workflows with blinded external review. |
| P2 | No automatic budget accounting or provider adapters | Plans record resource limits; roadmap separates proposals from implementation | Implement bounded adapters with cancellation, cost receipts, and reproducible model/tool configurations. |

## Closest-comparator implications

QED has a more developed automatic natural-language proof-search and staged
verification pipeline. This release does not implement an equivalent runtime.
MathResearch Ledger offers MCP-based continuation and explicit dependency-version
freshness; this release does not implement those interfaces. Human acceptance,
persistent mathematical objects, and traceable evidence therefore cannot be
advertised as exclusive features. Our combination of domain-specific preflight,
blind-first peer review, route-evidence review, explicit owner route approval,
and project-preserving kernel lifecycle is the narrower positioning to test.
An optional future adapter could share reviewed evidence with these systems
without importing their decisions as accepted project state.

## Evaluation proposal (not a completed benchmark)

Use a mix of known-proof reconstruction, seeded false statements, scoped failed
routes, formalization mismatches, and small synthetic experiments. Separate
training/development examples from sealed evaluation tasks. Compare single-chat,
lightweight multi-role, and full-ledger workflows under matched model, token,
compute, and human-review budgets. Have external reviewers blind to the arm
assess correctness, hallucinated citations, scope overclaiming, independence,
ability to stop on failure, reproducibility, and time to accepted progress.
Report failures and costs as well as successes. Human reviewers, not agent
ratings or validator passes, determine mathematical correctness. Run multiple
seeds and disclose contamination risks. No comparative result is claimed here.

## Product decision

Ship one repository with **AI4Math as the supported core** and **AI4S as an
experimental profile**, sharing only evidence and decision principles whose
meaning survives the domain change. Keep theorem-proof semantics out of
empirical acceptance criteria. Integrate specialized proving, retrieval, and
experiment systems through audited artifacts before attempting a universal
“autonomous scientist.” All code in this release is original local tooling;
related projects are references, not vendored dependencies.
