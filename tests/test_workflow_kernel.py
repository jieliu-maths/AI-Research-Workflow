#!/usr/bin/env python3
"""Regression tests for the reusable workflow kernel."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflowctl", ROOT / "tools" / "workflowctl.py")
assert SPEC and SPEC.loader
workflowctl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflowctl)


class WorkflowKernelTests(unittest.TestCase):
    def test_transaction_rolls_back_modified_and_created_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            original = target / "original.txt"
            original.write_text("before\n", encoding="utf-8")
            created = target / "nested" / "created.txt"
            backup = target / ".research-workflow" / "backups" / "test"
            with self.assertRaises(OSError):
                with workflowctl.FileTransaction(target, {"original.txt", "nested/created.txt"}, backup):
                    original.write_text("after\n", encoding="utf-8")
                    created.parent.mkdir()
                    created.write_text("partial\n", encoding="utf-8")
                    raise OSError("simulated mid-apply failure")
            self.assertEqual(original.read_text(encoding="utf-8"), "before\n")
            self.assertFalse(created.exists())

    def test_rollback_continues_after_one_restore_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            original = target / "original.txt"
            protected = target / "nested" / "protected.txt"
            protected.parent.mkdir()
            original.write_text("before\n", encoding="utf-8")
            protected.write_text("before\n", encoding="utf-8")
            backup = target / ".research-workflow" / "backups" / "test"
            transaction = workflowctl.FileTransaction(
                target, {"original.txt", "nested/protected.txt"}, backup,
            )
            transaction.__enter__()
            original.write_text("after\n", encoding="utf-8")
            protected.write_text("after\n", encoding="utf-8")
            real_copy2 = workflowctl.shutil.copy2

            def guarded_copy(source: Path, destination: Path, *args: object, **kwargs: object) -> object:
                if Path(destination) == protected:
                    raise OSError("simulated protected destination")
                return real_copy2(source, destination, *args, **kwargs)

            with patch.object(workflowctl.shutil, "copy2", side_effect=guarded_copy):
                failures = transaction.rollback()
            transaction.__exit__(None, None, None)
            self.assertEqual(original.read_text(encoding="utf-8"), "before\n")
            self.assertEqual(protected.read_text(encoding="utf-8"), "after\n")
            self.assertEqual(len(failures), 1)
            self.assertIn("nested/protected.txt", failures[0])

    def test_managed_block_drift_is_a_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / "source", root / "target"
            source.mkdir()
            target.mkdir()
            block_id = "example"
            start = workflowctl.marker(block_id, "start")
            end = workflowctl.marker(block_id, "end")
            (source / "doc.md").write_text(f"{start}\nnew\n{end}\n", encoding="utf-8")
            (target / "doc.md").write_text(f"{start}\nlocal edit\n{end}\n", encoding="utf-8")
            actions: list[dict[str, str]] = []
            accepted = workflowctl.apply_document_block(
                source_root=source, target=target, relative="doc.md", block_id=block_id,
                previous_hash="0" * 64, apply=True, backup_root=target / "backup", actions=actions,
            )
            self.assertFalse(accepted)
            self.assertEqual(actions[-1]["action"], "conflict")
            self.assertIn("local edit", (target / "doc.md").read_text(encoding="utf-8"))

    def test_route_scanner_ignores_route_matrix_heading(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            research = target / "research"
            research.mkdir()
            (research / "route_matrix.md").write_text("# Route Matrix\n\nRoute A and Route B are candidates.\n", encoding="utf-8")
            detected = workflowctl.detected_ids(target)
            self.assertEqual(detected["route_labels"], ["A", "B"])

    def test_historical_delivery_manifest_is_excluded_but_research_stays_strict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "init", str(target),
                 "--source", str(ROOT), "--apply"],
                capture_output=True, text=True, check=True,
            )
            delivery = target / "runs/2026-01-01-R001/manifest.json"
            delivery.parent.mkdir()
            record = {"run": "R001", "result": "Draft reviewed within a limited scope.",
                      "pages": 7, "deliveries": {"draft.tex": "historical record"}}
            original = json.dumps(record).encode()
            delivery.write_bytes(original)
            command = ["python3", str(target / "tools/researchctl.py"), "validate"]
            result = subprocess.run(command, text=True, capture_output=True, check=True)
            self.assertIn("LEGACY_DELIVERY_MANIFEST", result.stdout)
            self.assertEqual(delivery.read_bytes(), original)

            malformed = target / "runs/2026-01-02-R002/manifest.json"
            malformed.parent.mkdir()
            malformed.write_text(json.dumps({**record, "run_id": "R002"}), encoding="utf-8")
            result = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("MANIFEST_SCHEMA_RULE: runs/2026-01-02-R002", result.stdout)
            self.assertEqual(result.stdout.count("LEGACY_DELIVERY_MANIFEST"), 1)

            malformed.write_bytes(original)
            state_path = target / "research/machine/project-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["runs"].append({
                "id": "R002", "status": "completed", "route_id": None,
                "manifest": {
                    "path": malformed.relative_to(target).as_posix(),
                    "sha256": hashlib.sha256(original).hexdigest(),
                },
            })
            state_path.write_text(json.dumps(state), encoding="utf-8")
            result = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("MANIFEST_SCHEMA_RULE: runs/2026-01-02-R002", result.stdout)
            self.assertEqual(result.stdout.count("LEGACY_DELIVERY_MANIFEST"), 1)

    def test_new_project_init_is_complete_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "new-project"
            command = [
                "python3", str(ROOT / "tools" / "workflowctl.py"), "init", str(target),
                "--source", str(ROOT), "--project-name", "Test Project", "--apply",
            ]
            first = subprocess.run(command, text=True, capture_output=True, check=False)
            second = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            for relative in workflowctl.FULL_TEMPLATE_FILES:
                self.assertTrue((target / relative).is_file(), relative)
            self.assertTrue((target / "schemas/state-mapping-proposal.schema.json").is_file())
            self.assertTrue((target / "schemas/workspace-roles.schema.json").is_file())
            self.assertTrue((target / "research/machine/_template/workspace-roles.json").is_file())
            prompt_text = (target / "docs/research-workflow-prompts.md").read_text(encoding="utf-8")
            self.assertIn(str(ROOT), prompt_text)
            self.assertNotIn("<WORKFLOW_LIBRARY>", prompt_text)
            self.assertNotIn("create_thread", prompt_text)
            for retired in ("research/task_index.md", "research/proof_map.md", "research/research_log.md"):
                self.assertFalse((target / retired).exists())
            self.assertFalse((target / "research/machine/workspace-roles.json").exists())
            self.assertFalse((target / workflowctl.LIBRARY_MARKER_PATH).exists())
            config = json.loads((target / workflowctl.CONFIG_PATH).read_text(encoding="utf-8"))
            self.assertEqual(config["source_library_id"], workflowctl.LIBRARY_ID)
            self.assertEqual(config["execution_mode"], "single_window")
            validation = subprocess.run(["python3", str(target / "tools/researchctl.py"), "validate"], text=True, capture_output=True, check=False)
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_historical_registry_diagnostics_do_not_require_peer_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "new-project"
            init = subprocess.run(
                [
                    "python3", str(ROOT / "tools" / "workflowctl.py"), "init", str(target),
                    "--source", str(ROOT), "--project-name", "Peer Test", "--apply",
                ],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            registry = json.loads((target / "research/machine/_template/workspace-roles.json").read_text(encoding="utf-8"))
            for index, record in enumerate(registry["roles"]):
                record["thread_id"] = f"task-{index}"
                record["host_id"] = "local"
                record["status"] = "ready"
            registry["project_id"] = "peer-test"
            registry["project_path"] = str(target)
            actual = target / "research/machine/workspace-roles.json"
            actual.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
            valid = subprocess.run(
                ["python3", str(target / "tools/researchctl.py"), "validate"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
            for record in registry["roles"]:
                record["thread_id"] = "same-task"
            actual.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
            validation = subprocess.run(
                ["python3", str(target / "tools/researchctl.py"), "validate"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("LEGACY_WORKSPACE_ROLE_DISTINCT", validation.stdout)

    def test_upgrade_preserves_historical_role_registry_without_activating_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "role-upgrade"
            init = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "init", str(target),
                 "--source", str(ROOT), "--project-name", "Role Upgrade", "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            roles = json.loads((target / "research/machine/_template/workspace-roles.json").read_text(encoding="utf-8"))
            roles["schema_version"] = "1.0"
            for index, record in enumerate(roles["roles"]):
                record.pop("is_current_task")
                record["title"] = f"0{index} {record['role'].title()}"
                record["thread_id"] = f"kept-task-{index}"
                record["status"] = "ready"
            actual = target / "research/machine/workspace-roles.json"
            actual.write_text(json.dumps(roles, indent=2) + "\n", encoding="utf-8")
            upgrade = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "upgrade", str(target),
                 "--source", str(ROOT), "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(upgrade.returncode, 0, upgrade.stdout + upgrade.stderr)
            migrated = json.loads(actual.read_text(encoding="utf-8"))
            self.assertEqual(migrated, roles)

    def test_migrate_preserves_existing_mathematical_state_verbatim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "legacy-project"
            (target / "research").mkdir(parents=True)
            original = "# Project state\n\nA project-specific mathematical conclusion.\n"
            (target / "STATE.md").write_text(original, encoding="utf-8")
            (target / "research/proof_ledger.md").write_text("# Proof ledger\n\nP001 remains open.\n", encoding="utf-8")
            migration = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "migrate", str(target),
                 "--source", str(ROOT), "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(migration.returncode, 0, migration.stdout + migration.stderr)
            self.assertEqual((target / "STATE.md").read_text(encoding="utf-8"), original)
            config = json.loads((target / ".research-workflow.json").read_text(encoding="utf-8"))
            self.assertEqual(config["state_mapping"], "required")
            self.assertFalse((target / "research/machine/project-state.json").exists())

    def test_schema_rejects_an_unexpected_project_state_field(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "schema-project"
            init = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "init", str(target),
                 "--source", str(ROOT), "--project-name", "Schema Test", "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            state_path = target / "research/machine/project-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["unexpected_schema_field"] = True
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            validation = subprocess.run(
                ["python3", str(target / "tools/researchctl.py"), "validate"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(validation.returncode, 1)
            self.assertIn("STATE_SCHEMA_RULE", validation.stdout)
            self.assertIn("unexpected_schema_field", validation.stdout)

    def test_init_refuses_a_symlinked_parent_without_writing_outside(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "project"
            outside = root / "outside"
            target.mkdir()
            outside.mkdir()
            (target / "tools").symlink_to(outside, target_is_directory=True)
            result = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "init", str(target),
                 "--source", str(ROOT), "--project-name", "Link Test", "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("unsafe destination", result.stdout)
            self.assertFalse((outside / "researchctl.py").exists())
            self.assertFalse((target / ".research-workflow.json").exists())

    @unittest.skipUnless(shutil.which("xelatex"), "XeLaTeX is required for PDF generation")
    def test_readable_report_generates_markdown_latex_and_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "report-project"
            init = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "init", str(target),
                 "--source", str(ROOT), "--project-name", "Report Test", "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            report = subprocess.run(
                ["python3", str(target / "tools/researchctl.py"), "report", "--format", "pdf"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(report.returncode, 0, report.stdout + report.stderr)
            for suffix in ("md", "tex", "pdf"):
                path = target / "report" / f"project-summary.{suffix}"
                self.assertTrue(path.is_file(), path)
                self.assertGreater(path.stat().st_size, 0)

    def test_hydrate_run_writes_only_a_proposal_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            run_dir = target / "runs" / "2020-01-01-R001"
            run_dir.mkdir(parents=True)
            (run_dir / "researcher-T001.md").write_text("# T001\n\nA historical calculation.\n", encoding="utf-8")
            command = [
                "python3", str(ROOT / "tools/workflowctl.py"), "hydrate-run", str(target), "R001",
                "--proposal-only", "--apply",
            ]
            result = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            proposal_path = run_dir / "run-hydration.proposal.json"
            proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
            self.assertEqual(proposal["status"], "proposal_only")
            self.assertEqual(proposal["detected_task_ids"], ["T001"])
            self.assertFalse((run_dir / "manifest.json").exists())

    def test_mapping_proposal_template_is_noncanonical(self) -> None:
        proposal = json.loads((ROOT / "research/machine/_template/project-state.proposal.json").read_text(encoding="utf-8"))
        self.assertEqual(proposal["status"], "proposal_only")
        self.assertEqual(proposal["candidate_state"]["schema_version"], "2.1")
        self.assertEqual(proposal["candidate_state"]["snapshot"]["theorem_targets"], [])

    def test_dashboard_has_persistent_bilingual_interface(self) -> None:
        template = (ROOT / "dashboard/template.html").read_text(encoding="utf-8")
        self.assertIn('content="2.1-mathematical-bilingual"', template)
        self.assertIn('data-language="zh"', template)
        self.assertIn('data-language="en"', template)
        self.assertIn("research-dashboard-language", template)
        self.assertIn("已审定的数学进展", template)
        self.assertIn("Reviewed mathematical record", template)
        self.assertIn("命题、公式、路线结论与项目备注均保持原文", template)
        self.assertIn("Claims, formulas, route conclusions, and project notes are shown in their authored language", template)
        self.assertIn("命题及其当前数学地位", template)
        self.assertIn("Present mathematical standing", template)
        self.assertIn("本轮所研究的特定候选类已被排除", template)
        self.assertIn("the scoped candidate class was ruled out", template)
        self.assertNotIn("document.getElementById('route-notice').textContent = state.snapshot.note", template)
        self.assertNotIn("'正式状态'", template)
        self.assertNotIn("'执行结果'", template)
        self.assertNotIn("'结构性问题'", template)
        self.assertEqual(workflowctl.KERNEL_VERSION, "3.1.0")

    @unittest.skipUnless((ROOT / "workflow").is_file(), "standalone source repository only")
    def test_standalone_source_is_project_neutral(self) -> None:
        checked = set(workflowctl.MANAGED_FILES) | set(workflowctl.INIT_SOURCE_FILES)
        checked |= {"AGENTS.md", "WORKFLOW.md", "README.md", "workflow"}
        for relative in sorted(checked):
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"/(?:Users|home)/[A-Za-z0-9._-]+/", relative)
        run_entries = {
            path.name for path in (ROOT / "runs").iterdir()
            if path.name != ".DS_Store"
        }
        self.assertEqual(run_entries, {"README.md", "_template"})
        identity = workflowctl.library_identity(ROOT)
        self.assertEqual(identity["library_id"], workflowctl.LIBRARY_ID)

    @unittest.skipUnless((ROOT / "workflow").is_file(), "standalone source repository only")
    def test_library_identity_rejects_an_installed_project_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fake_source = Path(temporary) / "old-mathematical-project"
            fake_source.mkdir()
            (fake_source / ".research-workflow.json").write_text("{}\n", encoding="utf-8")
            target = Path(temporary) / "target"
            result = subprocess.run(
                [
                    "python3", str(ROOT / "tools/workflowctl.py"), "init", str(target),
                    "--source", str(fake_source), "--project-name", "Rejected Source",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing .research-workflow-library.json", result.stderr)
            self.assertFalse(target.exists())

    @unittest.skipUnless((ROOT / "workflow").is_file(), "standalone source repository only")
    def test_upgrade_replaces_but_never_trusts_a_legacy_source_hint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "legacy-project"
            init = subprocess.run(
                [
                    str(ROOT / "workflow"), "init", str(target),
                    "--project-name", "Legacy Hint Test", "--apply",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            config_path = target / workflowctl.CONFIG_PATH
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["source_hint"] = "/old/mathematical/project"
            config.pop("source_library_id", None)
            config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

            rejected = subprocess.run(
                [
                    "python3", str(ROOT / "tools/workflowctl.py"), "upgrade", str(target),
                    "--source", str(target),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("missing .research-workflow-library.json", rejected.stderr)

            upgraded = subprocess.run(
                [str(ROOT / "workflow"), "upgrade", str(target), "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            refreshed = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(refreshed["source_hint"], str(ROOT))
            self.assertEqual(refreshed["source_library_id"], workflowctl.LIBRARY_ID)

    @unittest.skipUnless((ROOT / "workflow").is_file(), "standalone source repository only")
    def test_standalone_launcher_reports_verified_identity(self) -> None:
        result = subprocess.run(
            [str(ROOT / "workflow"), "identify"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        identity = json.loads(result.stdout)
        self.assertEqual(identity["kind"], workflowctl.LIBRARY_KIND)
        self.assertEqual(identity["library_id"], workflowctl.LIBRARY_ID)
        self.assertEqual(identity["path"], str(ROOT))

    @unittest.skipUnless((ROOT / "workflow").is_file(), "standalone source repository only")
    def test_standalone_launcher_initializes_a_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "launcher-project"
            result = subprocess.run(
                [
                    str(ROOT / "workflow"), "init", str(target),
                    "--project-name", "Launcher Project", "--apply",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            state = json.loads((target / "research/machine/project-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["snapshot"]["project_name"], "Launcher Project")
            self.assertEqual(state["snapshot"]["state_version"], "S0")
            self.assertEqual(state["claims"], [])
            self.assertEqual(state["routes"], [])

    @unittest.skipUnless((ROOT / "workflow").is_file(), "standalone source repository only")
    def test_reusable_prompts_use_the_standalone_launcher(self) -> None:
        prompts = (ROOT / "docs/research-workflow-prompts.md").read_text(encoding="utf-8")
        self.assertIn("<WORKFLOW_LIBRARY>/workflow", prompts)
        self.assertIn("workflow\" identify", prompts)
        self.assertIn("source_hint` 只能作为备用候选", prompts)
        self.assertNotRegex(prompts, r"/(?:Users|home)/[A-Za-z0-9._-]+/")

    def test_route_review_is_due_and_cannot_be_bypassed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "route-review-project"
            init = subprocess.run(
                [
                    "python3", str(ROOT / "tools" / "workflowctl.py"), "init", str(target),
                    "--source", str(ROOT), "--project-name", "Route Review Test", "--apply",
                ],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)

            def file_ref(path: Path) -> dict[str, str]:
                return {
                    "path": str(path.relative_to(target)),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }

            def write_run(number: int, signal: str, review_path: str | None = None) -> Path:
                run_id = f"R{number:03d}"
                run_dir = target / "runs" / run_id
                run_dir.mkdir()
                brief = run_dir / "brief.md"
                summary = run_dir / "director-run-summary.md"
                brief.write_text(f"# {run_id} brief\n", encoding="utf-8")
                summary.write_text(f"# {run_id} summary\n", encoding="utf-8")
                orchestration = {
                    "schema_version": "1.0", "run_id": run_id, "route_id": "route:test",
                    "director_state": "closed", "active_task_id": None, "awaiting_role": None,
                    "last_completed_task_id": None, "next_action": None,
                    "owner_gate": {"required": False, "reason": None, "approval_reference": "owner:test"},
                    "processed_return_keys": [], "updated_at": "2026-09-14T00:00:00Z",
                }
                orchestration_path = run_dir / "orchestration.json"
                orchestration_path.write_text(json.dumps(orchestration, indent=2) + "\n", encoding="utf-8")
                manifest = {
                    "schema_version": "1.1", "run_id": run_id, "route_id": "route:test",
                    "state_in": "S0", "status": "completed", "brief": file_ref(brief),
                    "route_approval_reference": "owner:test", "task_records": [],
                    "director_summary": file_ref(summary), "state_transition": None,
                    "orchestration": {"path": str(orchestration_path.relative_to(target))},
                    "route_signal": signal,
                    "route_review": {"path": review_path} if review_path else None,
                }
                (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                return run_dir

            write_run(1, "partial_support")
            write_run(2, "null_result")
            third = write_run(3, "scoped_obstruction")
            validation = subprocess.run(
                ["python3", str(target / "tools/researchctl.py"), "validate"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("ROUTE_REVIEW_DUE", validation.stdout)

            review = json.loads((target / "runs/_template/route-review.json").read_text(encoding="utf-8"))
            review.update({
                "review_id": "RR-test-001", "route_id": "route:test", "status": "owner_gate",
                "reviewed_runs": ["R001", "R002", "R003"], "recommendation": "continue",
            })
            review["trigger"]["three_runs_without_decisive_support"] = True
            review["literature_refresh"].update({
                "status": "completed",
                "questions_from_obstructions": ["Which primary-source mechanism addresses the observed obstruction?"],
                "primary_sources": ["Primary source with theorem location"],
                "comparison_with_current_route": "No approved route change; comparison prepared for the owner.",
                "new_or_revised_routes": [],
            })
            review_path = third / "route-review.json"
            review_path.write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
            third_manifest_path = third / "manifest.json"
            third_manifest = json.loads(third_manifest_path.read_text(encoding="utf-8"))
            third_manifest["route_review"] = {"path": str(review_path.relative_to(target))}
            third_manifest_path.write_text(json.dumps(third_manifest, indent=2) + "\n", encoding="utf-8")
            write_run(4, "partial_support")
            bypass = subprocess.run(
                ["python3", str(target / "tools/researchctl.py"), "validate"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(bypass.returncode, 1)
            self.assertIn("ROUTE_REVIEW_BYPASSED", bypass.stdout)


class SingleWindowTests(unittest.TestCase):
    def init_project(self, target: Path) -> None:
        result = subprocess.run(
            ["python3", str(ROOT / "tools/workflowctl.py"), "init", str(target),
             "--source", str(ROOT), "--project-name", "Single Window Test", "--apply"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def validate(self, target: Path) -> subprocess.CompletedProcess:
        return subprocess.run(["python3", str(target / "tools/researchctl.py"), "validate"],
                              text=True, capture_output=True, check=False)

    def save(self, path: Path, value: dict) -> dict[str, str]:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return self.ref(path)

    def ref(self, path: Path) -> dict[str, str]:
        # All fixtures belong to a project directly above its runs directory.
        target = next(parent for parent in path.parents if (parent / ".research-workflow.json").is_file())
        return {"path": str(path.relative_to(target)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def session(self, target: Path) -> tuple[Path, dict]:
        directory = target / "runs/R001"
        directory.mkdir()
        (directory / "brief.md").write_text("# Question\nA bounded teaching calculation; no route activation.\n")
        (directory / "work.md").write_text("# Work\nExact finite calculation; the universal claim remains open.\n")
        manifest = json.loads((target / "runs/_template/manifest.json").read_text())
        manifest["schema_version"] = "1.2"
        manifest["critical_review"] = None
        manifest.update(run_id="R001", status="completed", brief=self.ref(directory / "brief.md"),
                        summary=self.ref(directory / "work.md"), route_signal="not_applicable")
        self.save(directory / "manifest.json", manifest)
        return directory, manifest

    def review(self, target: Path, directory: Path, manifest: dict) -> dict:
        for name in ("review-question.md", "review-baseline.md", "review-assessment.md"):
            (directory / name).write_text("# Synthetic independent review fixture: " + name + "\n")
        review = json.loads((target / "runs/_template/review.json").read_text())
        review["schema_version"] = "1.0"
        for field in ("claim_id", "revision", "claim_record"):
            review.pop(field, None)
        review.update(run_id="R001", review_kind="independent", reviewer="synthetic reviewer context",
                      baseline_frozen_before_candidate=True, verdict="survives_current_attacks")
        for field, name in (("question", "review-question.md"), ("baseline", "review-baseline.md"),
                            ("candidate", "work.md"), ("assessment", "review-assessment.md")):
            review[field] = self.ref(directory / name)
        manifest["critical_review"] = self.save(directory / "review.json", review)
        self.save(directory / "manifest.json", manifest)
        return review

    def test_completed_local_research_needs_only_three_files_and_no_role_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            directory, _ = self.session(target)
            before = (target / "STATE.md").read_bytes()
            result = self.validate(target)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("WORKSPACE_ROLES_MISSING", result.stdout)
            self.assertNotIn("READABLE_REPORT_MISSING", result.stdout)
            self.assertEqual({p.name for p in directory.iterdir()}, {"brief.md", "work.md", "manifest.json"})
            self.assertEqual((target / "STATE.md").read_bytes(), before)

    def test_key_review_rejects_missing_self_check_and_nonindependent_read_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            directory, manifest = self.session(target)
            manifest["critical_review_required"] = True
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CRITICAL_REVIEW_REQUIRED", result.stdout)
            review = self.review(target, directory, manifest)
            review["review_kind"] = "self_check"
            manifest["critical_review"] = self.save(directory / "review.json", review)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CRITICAL_REVIEW_SELF_CHECK", result.stdout)
            review["review_kind"] = "independent"
            review["baseline_frozen_before_candidate"] = False
            manifest["critical_review"] = self.save(directory / "review.json", review)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CRITICAL_REVIEW_ORDER", result.stdout)
            review["baseline_frozen_before_candidate"] = True
            manifest["critical_review"] = self.save(directory / "review.json", review)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_decisive_support_requires_surviving_review_of_the_exact_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            directory, manifest = self.session(target)
            manifest.update(route_id="route:synthetic", route_approval_reference="owner:synthetic", route_signal="decisive_support")
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CRITICAL_REVIEW_REQUIRED", result.stdout)
            review = self.review(target, directory, manifest)
            review["verdict"] = "uncertain"
            manifest["critical_review"] = self.save(directory / "review.json", review)
            self.save(directory / "manifest.json", manifest)
            self.assertIn("CRITICAL_REVIEW_UNRESOLVED", self.validate(target).stdout)
            review["verdict"] = "survives_current_attacks"
            manifest["critical_review"] = self.save(directory / "review.json", review)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            # An updated summary cannot silently inherit the old review, even if its own hash is refreshed.
            (directory / "repaired.md").write_text("# Substantively repaired candidate\n")
            manifest["summary"] = self.ref(directory / "repaired.md")
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CRITICAL_REVIEW_CANDIDATE", result.stdout)
            # And tampering with an already frozen proof is still detected.
            (directory / "work.md").write_text("# Changed after review\n")
            self.assertIn("CRITICAL_REVIEW_CANDIDATE_DRIFT", self.validate(target).stdout)

    def test_claim_changes_need_review_even_without_trigger_flag_and_still_need_owner_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            directory, manifest = self.session(target)
            transition = json.loads((target / "runs/_template/state-transition.json").read_text())
            transition.update(run_id="R001", proposal_id="ST-R001-S0-S1", state_to="S1")
            transition["changes"]["claims"] = [{"id": "P001", "status": "verified"}]
            manifest["state_transition"] = self.save(directory / "state-transition.json", transition)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CRITICAL_REVIEW_REQUIRED", result.stdout)
            self.review(target, directory, manifest)
            self.assertIn("TRANSITION_EVIDENCE_REQUIRED", self.validate(target).stdout)
            task = json.loads((target / "runs/_template/Txxx.json").read_text())
            task.update(run_id="R001", task_id="T001", status="returned", verdict="supports",
                        dispatch=self.ref(directory / "brief.md"), artifact=self.ref(directory / "work.md"),
                        derivation_roots=["synthetic exact definitions"])
            manifest["task_records"] = [self.save(directory / "T001.json", task)]
            transition["evidence_records"] = ["T001"]
            transition["status"] = "owner_approved"
            manifest["state_transition"] = self.save(directory / "state-transition.json", transition)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("TRANSITION_APPROVAL", result.stdout)
            transition["owner_approval_reference"] = "owner:synthetic-test-only"
            manifest["state_transition"] = self.save(directory / "state-transition.json", transition)
            self.save(directory / "manifest.json", manifest)
            before = (target / "STATE.md").read_bytes()
            result = self.validate(target)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((target / "STATE.md").read_bytes(), before)
            self.assertEqual(json.loads((target / "research/machine/project-state.json").read_text())["claims"], [])
            # An arbitrary JSON file cannot impersonate a typed evidence record.
            manifest["task_records"] = [self.save(directory / "untyped.json", task)]
            transition["evidence_records"] = ["untyped"]
            manifest["state_transition"] = self.save(directory / "state-transition.json", transition)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("TRANSITION_EVIDENCE_LINK", result.stdout)

    def test_default_report_needs_no_pdf_engine_and_does_not_require_optional_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            for output_format in ("md", "tex"):
                command = ["python3", str(target / "tools/researchctl.py"), "report"]
                if output_format == "tex":
                    command += ["--format", "tex"]
                result = subprocess.run(command, text=True, capture_output=True, check=False)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((target / "report" / ("project-summary." + output_format)).is_file())
            self.assertFalse((target / "report/project-summary.pdf").exists())
            self.assertEqual(self.validate(target).returncode, 0)

    def test_open_planning_claim_does_not_require_an_independent_proof_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            directory, manifest = self.session(target)
            transition = json.loads((target / "runs/_template/state-transition.json").read_text())
            transition.update(run_id="R001", proposal_id="ST-R001-S0-S1", state_to="S1")
            transition["changes"]["claims"] = [{"id": "P001", "status": "open"}]
            # A differently named transition must still be read and checked.
            manifest["state_transition"] = self.save(directory / "planning-proposal.json", transition)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            transition["changes"]["claims"][0]["status"] = "verified"
            manifest["state_transition"] = self.save(directory / "planning-proposal.json", transition)
            self.save(directory / "manifest.json", manifest)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CRITICAL_REVIEW_REQUIRED", result.stdout)

    def test_single_window_route_review_cannot_be_bypassed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            original, base = self.session(target)
            for number in range(1, 5):
                directory = target / "runs" / f"R{number:03d}"
                if number > 1:
                    directory.mkdir()
                    (directory / "brief.md").write_bytes((original / "brief.md").read_bytes())
                    (directory / "work.md").write_bytes((original / "work.md").read_bytes())
                manifest = dict(base, run_id=f"R{number:03d}", route_id="route:synthetic",
                                route_approval_reference="owner:synthetic", route_signal="null_result",
                                brief=self.ref(directory / "brief.md"), summary=self.ref(directory / "work.md"))
                self.save(directory / "manifest.json", manifest)
                if number == 3:
                    result = self.validate(target)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn("ROUTE_REVIEW_DUE", result.stdout)
            result = self.validate(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("ROUTE_REVIEW_BYPASSED", result.stdout)
            self.assertFalse(any(path for path in (target / "runs").rglob("orchestration.json") if "_template" not in path.parts))

    def test_upgrade_conflict_preserves_local_protocol_and_frozen_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            self.session(target)
            protocol = target / "WORKFLOW.md"
            protocol.write_text(protocol.read_text() + "\nProject-specific mathematical guardrail.\n")
            before = {str(path.relative_to(target)): path.read_bytes() for path in target.rglob("*") if path.is_file()}
            result = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "upgrade", str(target), "--source", str(ROOT), "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("CONFLICT", result.stdout)
            self.assertEqual(before, {str(path.relative_to(target)): path.read_bytes() for path in target.rglob("*") if path.is_file()})

    def test_untracked_session_template_is_not_overwritten_on_upgrade(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.init_project(target)
            config_path = target / ".research-workflow.json"
            config = json.loads(config_path.read_text())
            config["managed_files"].pop("runs/_template/work.md")
            self.save(config_path, config)
            template = target / "runs/_template/work.md"
            template.write_text("# Local template predating kernel ownership\n")
            before = template.read_bytes()
            result = subprocess.run(
                ["python3", str(ROOT / "tools/workflowctl.py"), "upgrade", str(target), "--source", str(ROOT), "--apply"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertEqual(template.read_bytes(), before)

if __name__ == "__main__":
    unittest.main()
