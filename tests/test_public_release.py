"""Regression coverage for evidence boundaries and the experimental AI4S scaffold."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import evidencectl
import publication_check


class PublicReleaseTests(unittest.TestCase):
    def demo(self, name: str, script: str, parent: Path) -> tuple[Path, dict]:
        output = parent / name
        result = subprocess.run([sys.executable, str(ROOT / script), "--output-dir", str(output)],
                                text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = json.loads((output / "evidence.json").read_text())
        self.assertEqual(evidencectl.inspect(record, output), [])
        return output, record

    def test_bounded_math_demo_does_not_claim_a_universal_proof(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output, record = self.demo("math", "examples/ai4math/verify.py", Path(temporary))
            rows = json.loads((output / "results.json").read_text())
            self.assertEqual([row["n"] for row in rows], list(range(100)))
            self.assertTrue(all(row["sum"] == row["square"] for row in rows))
            self.assertEqual(record["kind"], "finite_check")
            self.assertEqual(record["status"], "evidence_only")
            self.assertIn("no quantification beyond", record["scope"])
            self.assertFalse((output / "STATE.md").exists())
            (output / "results.json").write_text("tampered")
            self.assertTrue(any("content mismatch" in item for item in evidencectl.inspect(record, output)))

    def test_synthetic_demo_reproduces_selection_without_test_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            first, record = self.demo("first", "examples/ai4s/experiment.py", parent)
            second, _ = self.demo("second", "examples/ai4s/experiment.py", parent)
            self.assertEqual((first / "results.json").read_bytes(), (second / "results.json").read_bytes())
            result = json.loads((first / "results.json").read_text())
            self.assertEqual(result["test_accesses"], 1)
            self.assertEqual(result["selected_model"], min(result["validation_mse"], key=result["validation_mse"].get))
            data = json.loads((first / "data.json").read_text())
            partitions = [set(map(tuple, data[key])) for key in ("train", "validation", "test")]
            self.assertFalse(partitions[0] & partitions[1] or partitions[0] & partitions[2] or partitions[1] & partitions[2])
            self.assertEqual(record["kind"], "numerical_experiment")

    def test_evidence_refuses_path_escape_symlink_and_false_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output, record = self.demo("math", "examples/ai4math/verify.py", Path(temporary))
            bad = copy.deepcopy(record)
            bad["files"][0]["path"] = "../outside.txt"
            self.assertTrue(evidencectl.inspect(bad, output))
            linked = output / "linked.py"
            linked.symlink_to(output / "verify.py")
            bad["files"][0]["path"] = "linked.py"
            self.assertTrue(any("symbolic link" in item for item in evidencectl.inspect(bad, output)))
            bad = copy.deepcopy(record)
            bad["execution"]["exit_code"] = 1
            self.assertTrue(evidencectl.inspect(bad, output))
            bad = copy.deepcopy(record)
            bad["kind"] = "formal_certificate"
            bad["formal"] = {"theorem": "Demo.identity", "axioms": [], "has_placeholders": True}
            self.assertTrue(any("placeholders" in item for item in evidencectl.inspect(bad, output)))
            bad["formal"]["has_placeholders"] = False
            # This only admits a metadata record, never verifies a formal proof.
            self.assertEqual(evidencectl.inspect(bad, output), [])

    def test_malformed_metadata_fails_cleanly_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            output, record = self.demo("math", "examples/ai4math/verify.py", parent)
            record["execution"]["command"] = [sys.executable, "-c", "raise RuntimeError('must not execute')"]
            self.assertEqual(evidencectl.inspect(record, output), [])
            for key in ("kind", "outcome"):
                bad = copy.deepcopy(record)
                bad[key] = []
                self.assertTrue(evidencectl.inspect(bad, output))
            path = parent / "invalid.json"
            path.write_text("{")
            result = subprocess.run([sys.executable, str(ROOT / "tools/evidencectl.py"), str(path)],
                                    text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)

    def test_ai4s_preview_is_read_only_and_existing_targets_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "science"
            command = [str(ROOT / "workflow"), "init-ai4s", str(target), "--project-name", "Synthetic science"]
            preview = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertFalse(target.exists())
            apply = subprocess.run(command + ["--apply"], text=True, capture_output=True, check=False)
            self.assertEqual(apply.returncode, 0, apply.stdout + apply.stderr)
            before = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            again = subprocess.run(command + ["--apply"], text=True, capture_output=True, check=False)
            self.assertEqual(again.returncode, 1)
            after = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            self.assertFalse((target / "research/proof_ledger.md").exists())
            self.assertFalse((target / ".research-workflow.json").exists())
            self.assertTrue((target / "tools/evidencectl.py").is_file())
            profile = json.loads((target / "profile.json").read_text())
            self.assertFalse(profile["claims_approved"])
            self.assertFalse(profile["upgrade_support"])
            for mode in ("init", "migrate", "upgrade"):
                mixed = subprocess.run([str(ROOT / "workflow"), mode, str(target), "--apply"],
                                       text=True, capture_output=True, check=False)
                self.assertEqual(mixed.returncode, 1, mixed.stdout + mixed.stderr)
                self.assertIn("separate profile", mixed.stderr)
            self.assertEqual(before, {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()})

    def test_ai4s_refuses_symlinked_target_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real = root / "real"
            real.mkdir()
            link = root / "linked"
            link.symlink_to(real, target_is_directory=True)
            result = subprocess.run([str(ROOT / "workflow"), "init-ai4s", str(link / "science"), "--apply"],
                                    text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(list(real.iterdir()), [])

    def test_publication_scan_detects_paths_and_environment_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "guide.md").write_text("/" + "Users" + "/private-owner/project")
            (root / ".env").write_text("NOT_A_REAL_KEY=placeholder")
            problems = publication_check.check(root)
            self.assertTrue(any("home-directory" in item for item in problems))
            self.assertTrue(any("environment file" in item for item in problems))


if __name__ == "__main__":
    unittest.main()
