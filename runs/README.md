# Research sessions

For a new session create only `brief.md`, `work.md`, and `manifest.json` from
`_template/`. Do not copy every template. Keep one active question and work
continuously within the owner-approved scope. The closing mathematical summary
belongs in `work.md`, referenced by the manifest, without a duplicate summary.

Use `Txxx.json` only for durable evidence; `review.json` only for triggered
independent review; state proposal files only when a canonical change is
requested; route-review files only when the route-review trigger fires.
Historical v1.0/v1.1 runs remain unchanged and readable. Files under
`_template/legacy/` are compatibility examples, never a new-session checklist.

In 3.1 use manifest 1.3. Freeze only submitted claim/proof versions, with
claim-evidence.json and review 1.1 when needed. Work notes remain appendable.
Executable checks, compute escalation and benchmark comparisons are conditional;
see docs/research-feedback.md. Historical v1.2 review contracts remain unchanged.

Some older manuscript deliveries used `manifest.json` for a record with a
textual `result`, an integer `pages` count and a `deliveries` object. If none
of the research-manifest identity or evidence fields are present, validation
reports an unregistered record of this shape as a historical delivery and
excludes it from run evidence. A directory with task or state-transition
sidecars still receives research-manifest checks.
Keep its original bytes. Store new manuscript review and delivery records
under the manuscript's artifact convention.
