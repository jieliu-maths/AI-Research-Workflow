# Reuse and upgrades

The workflow is split into two layers.

- The **kernel** contains the validator, JSON Schemas, dashboard template,
  project skill, versioned run templates, and versioned documentation blocks.
  It may be copied or upgraded mechanically.
- The **project state** contains the charter, mathematical guardrails, claims,
  routes, evidence, hashes, run history, and generated dashboard. It must be
  initialized or reviewed separately and is never copied from another project.

There is also a host-level runtime layer. `workflowctl` installs files but does
not create Codex UI tasks. The owner-facing task becomes `0 Director`; a
user-authorized prompt creates or reconnects the two top-level peers
`1 Researcher` and `2 Critic` and records all three identifiers in
`research/machine/workspace-roles.json`. That registry is
operational metadata, not canonical mathematical state. It is safe to replace
stale task identifiers after review, but it cannot carry claim or route
approvals.

## Safe lifecycle

Run `python3 tools/workflowctl.py <mode> <target>` without `--apply` first. The
default is a preview. Use `--apply` only after checking the resolved target,
planned writes, conflicts, and state-mapping requirement.

- `init`: create missing canonical skeletons and an empty S0 machine mirror.
- `migrate`: preserve an older project's canonical files, install the kernel,
  and write a report of detected claim and route IDs. If no reviewed machine
  mirror exists, the report requires a semantic mapping pass before ordinary
  validation can succeed.
- `upgrade`: perform a no-write preflight, then replace only kernel files that
  still match their installed hash. Replace a marked documentation block only
  when its own recorded hash still matches. A local edit outside a block is
  project-owned; a locally changed managed block or kernel file is a conflict.
  Whole run templates are upgraded, while instantiated runs are never rewritten.
- `hydrate-run`: hash one historical run and write only a proposal inventory.
  State input, route identity, task verdicts, derivation roots, and transitions
  remain unresolved until human review; the command never materializes
  canonical sidecars.
- `self-check`: verify the standalone kernel source, schemas, managed blocks,
  project neutrality, and automated tests without requiring project state.

Kernel 2.3 added a host-return loop and a route-review control layer. New runs
carry `orchestration.json` plus a route signal in `manifest.json`. A mandatory
route review uses `route-review.md` and `route-review.json`; these are
operational evidence summaries and decision proposals, not canonical route
decisions. Existing instantiated runs remain untouched and may be hydrated only
through the proposal-only path.

Kernel 2.5 makes the workflow source a standalone repository. Projects are
installed or upgraded through its `workflow` launcher, so no target project
depends on the source path, mathematical state, or generated dashboard of the
project from which the kernel was originally developed.

Kernel 2.6 makes schema constraints executable, rejects writes through linked
destination ancestors, migrates the role registry to the fixed three-task
titles, requires a literature refresh inside route review, and generates
consolidated Markdown, LaTeX, and PDF reading copies.

Kernel 2.6.1 keeps `<WORKFLOW_LIBRARY>` only in the portable source prompt. On
`init`, `migrate`, or `upgrade`, the installed project copy is rendered with
the actual absolute source path. When operating from an older prompt that still
contains the placeholder, use the Codex saved-project list and accept only a
unique standalone repository whose identity and integrity checks pass.

Kernel 2.6.2 adds a source-only `.research-workflow-library.json` marker and
`workflow identify`. Installed mathematical projects never receive this
marker. A candidate library must have the expected kind and stable library ID,
must pass both `workflow identify` and `workflow self-check`, and must not have
its own `.research-workflow.json`. Treat a legacy project's `source_hint` only
as an untrusted fallback candidate subject to those checks. Never guess a path
or treat a mathematical project as the reusable kernel.

Kernel versions follow semantic versioning. Every release must bump
`KERNEL_VERSION`, update its managed blocks and assets, and rerun init,
migration, idempotency, and conflict tests. Schema changes are separate: add an
explicit transformation to `STATE_MIGRATIONS` and bump `SCHEMA_VERSION`.
Upgrades stop with a conflict if no complete schema migration path is
registered; they never discard unknown project-state fields to make a new
validator pass.

Every applied operation writes `.research-workflow.json` and a report under
`research/machine/`. Existing changed files receive timestamped backups under
`.research-workflow/backups/`. Apply is transactional across known targets: a
write failure restores modified files and removes files created by that
operation.

## State-mapping gate

For migration, derive a candidate `project-state.json` from `STATE.md`, the
proof ledger, proof map, route matrix, and accepted run decisions. Treat it as
a proposal until the owner confirms claim statuses, dependency directions,
route-rejection scopes, active run, and evidence lineage. Only then record the
canonical hashes and mark migration ready.
