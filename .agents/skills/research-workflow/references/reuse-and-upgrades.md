# Reuse and upgrades

Kernel 3.1 defaults to one research window, light records, and on-demand key
review. Installation creates files only; it does not create, rename, reconnect,
or wait for Codex tasks. Historical role registries remain untouched and are
diagnosed as historical metadata if present; any diagnostics are warnings,
never prerequisites for current research. Their absence is normal.

## Safe lifecycle

Use a verified standalone library: `.research-workflow-library.json` has kind
`standalone-proof-ledger-research-workflow-library` and library ID
`ai-research-workflow-kernel`; `workflow identify` and `workflow self-check`
must pass; the source must not contain `.research-workflow.json`.
The installed `source_hint` is an untrusted fallback candidate. If a portable
prompt still has `<WORKFLOW_LIBRARY>`, resolve a unique saved source project or
ask for its path; never guess or use a mathematical project as the library.

Preview `workflow init TARGET`, `migrate TARGET`, or `upgrade TARGET`, then use
`--apply` after reviewing target, conflicts, and authorization. Apply repeats
preflight and rolls back known targets on write failure. Refuse destination
symlinks and linked ancestors. Never overwrite canonical mathematics, raw
submitted evidence, or instantiated runs.

New projects receive only the small canonical skeleton and empty S0 mirror.
Detailed proof maps, logs, and specialized notes are optional, with links
instead of duplicated mathematical assertions. Managed run templates include
conditional evidence/review/transition templates; copy only the three ordinary
session files. Retired dispatch templates live under `_template/legacy/`.

## Upgrading from 2.x

Manifest schema 1.2 adds a summary reference and key-review gate without
orchestration. Old v1.0/v1.1 runs and task records remain accepted with their
original constraints; do not silently rewrite them. The project-state schema
remains 2.1. No claim statuses, route decisions, or evidence meanings migrate.

WORKFLOW.md and optional activity guides are now whole managed documents, so
an upgrade cannot leave mandatory three-role prose between managed blocks.
An exact shipped v2.7.0 document can be recognized by its recorded checksum and
adopted, with backup. Other preexisting or locally modified documents conflict;
merge project-specific guardrails deliberately. AGENTS.md keeps managed
operational blocks and preserves project-owned guardrails. New governing
blocks explicitly supersede retired operational requirements in preserved text.

Unmodified managed files are replaced, modified ones conflict, and old
instantiated runs and role registries remain byte-for-byte preserved. Preview
and apply must agree; no partial change is accepted on conflict. Historical
root-level retired templates may remain in old projects but are not required.

## State mapping

Migration of a project without a reviewed mirror requires a separate proposal
for claim status, necessary dependencies, scope, theorem targets, route/run
identity, and evidence lineage. Keep canonical hashes unchanged until explicit
human approval. A structural validation pass is never mathematical acceptance.
Use `hydrate-run ... --proposal-only` only for a historical inventory; it never
creates canonical evidence records or silently promotes inferred statuses.

Version managed assets with KERNEL_VERSION. Register explicit project-state
schema transformations in STATE_MIGRATIONS when that schema changes. Unknown
fields and statuses must not be discarded to make validation pass.

## Upgrading 3.0 to 3.1

Install new tools, schemas, conditional templates and operational instructions
through the same preview/transaction/conflict rules. New sessions use manifest
1.3 and claim-bound review 1.1. Existing 1.2 manifests and 1.0 reviews retain
their summary-bound semantics and frozen bytes; do not rewrite them or infer
reviewed claim snapshots automatically. Project-state schema stays 2.1, so no
mathematical state migration or owner approval is inferred from tool upgrades.
Conditional checks/evaluations must not become new startup requirements.

For an older project's first restart, compare STATE and its approved ledger
with the actual manuscript series and dated review records. When useful,
record the exact paths, review scope and unresolved discrepancies in the
project-owned `research/current-work.md`. Keep this note out of canonical
hashes. It can be corrected as files move without changing any claim status.
Use the existing proposal path for a mathematical reconciliation.

The validator reports a legacy `manifest.json` as a delivery when it has a
textual `result`, integer `pages` and a `deliveries` object, with no research
identity or evidence fields, task or transition sidecars, or canonical run
reference. A research record that fails its schema or hash checks needs
deliberate repair or evidence reconciliation. Do not invent missing hashes,
outcomes or approvals.
