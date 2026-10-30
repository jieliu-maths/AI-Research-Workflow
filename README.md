# AI Research Workflow

**AI4Math-first research workflows with explicit evidence, independent review,
and human-approved mathematical state.**

[简体中文](README.zh-CN.md) · [Quickstart](#quickstart) ·
[Landscape review](docs/landscape-review.en.md) · [AI4S experimental profile](profiles/ai4s/README.md) ·
[MIT License](LICENSE)

Version **2.7.0**. A reusable workflow kernel for researchers who use AI to
explore difficult mathematical questions over many sessions. It keeps theorem
targets, proof dependencies, derivation roots, failed candidates, and unresolved
gaps visible. A generated argument or a successful computation does not silently
become an accepted theorem.

## Why this project

- **Proof-ledger first:** separate the theorem target, proof obligations, routes,
  executions, and evidence. Expose strict dependencies and circularity risks.
- **Independent review:** Director, Researcher, and Critic are separate visible
  top-level tasks sharing the project. Critic develops a baseline before reading
  the construction; different role names alone do not guarantee independence.
- **Scoped learning:** preserve failed candidates and exactly what they exclude.
  Review an unproductive route before investing in another construction run.
- **Owner decisions:** target/route changes, claim promotion, global notation,
  and manuscript transfer require explicit human approval.
- **Reusable records:** versioned templates, transactional installation,
  conflict-preserving upgrades, bilingual proof-map dashboard, and consolidated
  Markdown/LaTeX/PDF reading copies in installed mathematical projects.
- **Portable evidence:** inspect external proof/computation/experiment bundles
  without granting their outputs authority over canonical state.

This is a protocol and local tooling layer. It includes no foundation model,
proof-search engine, literature-search service, automatic agent scheduler, or
host sandbox. No evidence yet shows that this workflow improves theorem-solving
rates or research productivity relative to alternatives.

## Requirements

- Python **3.10+**, with only the standard library for the kernel and demos.
- Bash and Git for the commands below. macOS and Linux are CI targets;
  Windows users can use WSL, which is not yet a separate CI target.
- For the supported role workflow: a Codex desktop saved project and the ability
  to create three separate visible local tasks. The installer creates files,
  not app tasks. Other hosts can read the protocols, but no equivalent host
  adapter is shipped or validated.
- Optional: XeLaTeX for PDF reading copies; without it, the report command
  preserves Markdown/LaTeX and reports that PDF generation was not completed.
- External provers/models/services require their own setup, access, and licenses.
  No API key is needed for the offline demos or self-check.

## Quickstart

```bash
git clone https://github.com/jieliu-maths/AI-Research-Workflow.git
cd AI-Research-Workflow
./workflow identify
./workflow self-check
```

Try the offline bounded-arithmetic example (choose a fresh output directory):

```bash
python3 examples/ai4math/verify.py --output-dir /tmp/ai4math-demo
python3 tools/evidencectl.py /tmp/ai4math-demo/evidence.json
```

It checks 100 exact integer cases and explicitly leaves the universal theorem
unproved by the computation. See [the example](examples/ai4math/README.md).

Preview a new AI4Math project, then apply after reviewing its name and target:

```bash
./workflow init ../my-math-project --project-name "My math project"
./workflow init ../my-math-project --project-name "My math project" --apply
```

Open the target directory as a saved project in Codex. Use the
[English prompts](docs/research-workflow-prompts.en.md) or
[Chinese prompts](docs/research-workflow-prompts.md). Start with your tentative
question, known literature, constraints, and intended result. The current chat
is `0 Director`; only after you approve the exact target and route, create
`1 Researcher` and `2 Critic` as independent peers. A scaffold starts at S0
with no approved theorem, claim, or route.

## Everyday use

From an **installed AI4Math project**:

```bash
python3 tools/researchctl.py validate
python3 tools/researchctl.py summary
python3 tools/researchctl.py blockers P001
python3 tools/researchctl.py dashboard
python3 tools/researchctl.py report
```

`P001` is an illustrative claim identifier; replace it with a registered claim.
Open `dashboard/index.html` for the bilingual proof map. Generate reading copies
only after the owner-approved mathematical record is synchronized. This source
repository intentionally has no project state: use `./workflow self-check` here.

A validator pass means record consistency, not mathematical correctness. A
Critic verdict of “survives current attacks” is not a proof. A numerical result,
finite check, or submitted formal artifact must retain its exact scope. See
[the evidence contract](docs/evidence-bundles.md) and [governing workflow](WORKFLOW.md).

## Existing projects and upgrades

Run these from the verified source repository:

```bash
./workflow migrate /path/to/legacy-project
./workflow upgrade /path/to/installed-math-project
```

Preview first; add `--apply` only after review. Migration preserves existing
mathematical files and may require an owner-reviewed semantic mapping. Upgrade
replaces unchanged managed kernel assets and marked blocks, preserves local
modifications as conflicts, and leaves instantiated runs intact. Installation
copies assets; projects do not need this repository to run their local tools.
Keep a verified source checkout for future upgrades. Installed assets carry
`WORKFLOW-LICENSE`; this does not choose a license for your research.

## AI4S extension

An **experimental, separately initialized** scientific profile adds dataset
provenance, controls, frozen splits, uncertainty, reproducibility, and resource
budgets. It shares evidence principles with AI4Math while using a separate
scientific protocol and claim vocabulary.

```bash
./workflow init-ai4s ../my-science-project --project-name "My science project"
./workflow init-ai4s ../my-science-project --project-name "My science project" --apply
python3 examples/ai4s/experiment.py --output-dir /tmp/ai4s-demo
python3 tools/evidencectl.py /tmp/ai4s-demo/evidence.json
```

The parent directory must exist and the target must be new. AI4S currently has
no managed upgrades, automated experiments, claim-graph validator, dashboard,
or report generator. [Profile scope](profiles/ai4s/README.md).

## Repository map

| Path | Purpose |
| --- | --- |
| `WORKFLOW.md`, `agents/` | Mathematical lifecycle and role contracts |
| `runs/_template/`, `schemas/` | Frozen-run templates and machine record schemas |
| `tools/`, `workflow` | Installation, validation, evidence inspection, reports |
| `dashboard/` | Bilingual proof-map template |
| `docs/` | Prompts, evidence contract, comparison, and roadmap |
| `examples/` | Offline AI4Math and synthetic AI4S teaching fixtures |
| `profiles/ai4s/` | Experimental scientific workflow scaffold |
| `tests/` | Regression tests; no model or research-quality benchmark |

## Development and reuse

```bash
./workflow self-check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributions, [the dated primary-source
comparison](docs/landscape-review.en.md) for positioning and limitations, and
[ROADMAP.md](ROADMAP.md) for implemented versus planned work.

MIT licensed, copyright 2026 Jie Liu. References to other projects describe
related work; no third-party code, model weights, datasets, or services are
bundled or relicensed under this project's license. The teaching examples are
synthetic and contain no private research results.
