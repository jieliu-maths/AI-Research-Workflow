"""Behavioral checks for meaning, versioned evidence, executable tests and comparisons."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import benchctl
import checkctl
import evidencectl


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


class VersionedEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "project"
        result = subprocess.run(["python3", str(ROOT / "tools/workflowctl.py"), "init", str(self.root),
                                 "--source", str(ROOT), "--apply"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def ref(self, path: Path) -> dict:
        return evidencectl.file_ref(self.root, str(path.relative_to(self.root)))

    def validate(self) -> subprocess.CompletedProcess:
        return subprocess.run(["python3", str(self.root / "tools/researchctl.py"), "validate"], text=True, capture_output=True)

    def session(self, number: int = 1, gain: str = "new_distinction") -> tuple[Path, dict]:
        directory = self.root / "runs" / f"R{number:03d}"
        directory.mkdir()
        (directory / "brief.md").write_text("# Synthetic exact question\nPreserve all stated quantifiers and hypotheses.\n")
        (directory / "work.md").write_text("# Continuous notes\nSynthetic result; no canonical claim is accepted.\n")
        value = json.loads((self.root / "runs/_template/manifest.json").read_text())
        value.update(run_id=f"R{number:03d}", status="completed", brief=self.ref(directory / "brief.md"),
                     summary=self.ref(directory / "work.md"), route_signal="not_applicable",
                     meaning_audit={"status": "matched", "note": "Synthetic intended target checked, not a real proof certificate."})
        value["progress"].update(kind=gain, explanation="An explicitly scoped synthetic distinction, or a declared lack of new information.")
        save(directory / "manifest.json", value)
        return directory, value

    def claim(self, directory: Path, claim_id: str = "P001", revision: str = "v1", *, dependencies: list | None = None, previous: dict | None = None) -> tuple[Path, dict]:
        value = json.loads((self.root / "runs/_template/claim-evidence.json").read_text())
        proof = directory / f"{claim_id}-{revision}-proof.md"
        proof.write_text(f"# {claim_id} {revision}\nSynthetic proof metadata fixture only.\n")
        value.update(claim_id=claim_id, revision=revision, target=self.ref(directory / "brief.md"),
                     proof=self.ref(proof), depends_on=dependencies or [], supersedes=previous,
                     change_kind="substantive" if previous else "initial",
                     meaning_audit={"status": "matched", "note": "Every declared quantifier and scope matches the synthetic target."},
                     novelty={"status": "known_result", "note": "Teaching fixture, no research novelty claimed."})
        path = directory / f"{claim_id}-{revision}.json"
        save(path, value)
        return path, value

    def review(self, directory: Path, path: Path, claim: dict) -> tuple[Path, dict]:
        for name in ("question", "baseline", "assessment"):
            (directory / f"{claim['claim_id']}-{claim['revision']}-{name}.md").write_text(f"# Synthetic {name}\n")
        value = json.loads((self.root / "runs/_template/review.json").read_text())
        value.update(run_id=directory.name, claim_id=claim["claim_id"], revision=claim["revision"],
                     claim_record=self.ref(path), review_kind="independent", reviewer="synthetic isolated reviewer",
                     baseline_frozen_before_candidate=True, candidate=claim["proof"], verdict="survives_current_attacks")
        for field in ("question", "baseline", "assessment"):
            value[field] = self.ref(directory / f"{claim['claim_id']}-{claim['revision']}-{field}.md")
        review_path = directory / f"{claim['claim_id']}-{claim['revision']}-review.json"
        save(review_path, value)
        return review_path, value

    def index(self, directory: Path, manifest: dict, path: Path, claim: dict, *, critical: bool = True) -> Path:
        review_path, _ = self.review(directory, path, claim)
        manifest.setdefault("claim_records", []).append(self.ref(path))
        manifest.setdefault("critical_reviews", []).append(self.ref(review_path))
        manifest["critical_review_required"] = critical
        save(directory / "manifest.json", manifest)
        return review_path

    def proposal(self, directory: Path, manifest: dict, claim: dict, status: str = "proposal_only") -> dict:
        task = json.loads((self.root / "runs/_template/Txxx.json").read_text())
        task.update(run_id=directory.name, task_id="T001", status="returned", verdict="supports", proof_items=[claim["claim_id"]],
                    dispatch=self.ref(directory / "brief.md"), artifact=claim["proof"], derivation_roots=["synthetic definitions"])
        save(directory / "T001.json", task)
        manifest["task_records"] = [self.ref(directory / "T001.json")]
        transition = json.loads((self.root / "runs/_template/state-transition.json").read_text())
        transition.update(run_id=directory.name, proposal_id=f"ST-{directory.name}-S0-S1", state_to="S1", status=status, evidence_records=["T001"])
        transition["changes"]["claims"] = [{"id": claim["claim_id"], "status": "verified"}]
        save(directory / "state-transition.json", transition)
        manifest["state_transition"] = self.ref(directory / "state-transition.json")
        save(directory / "manifest.json", manifest)
        return transition

    def test_three_daily_files_suffice_without_claim_review_or_escalation(self) -> None:
        directory, _ = self.session()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual({p.name for p in directory.iterdir()}, {"brief.md", "work.md", "manifest.json"})

    def test_summary_can_evolve_without_invalidating_frozen_proof_review(self) -> None:
        directory, manifest = self.session()
        path, claim = self.claim(directory)
        review_path = self.index(directory, manifest, path, claim)
        frozen = {p: p.read_bytes() for p in (path, review_path, self.root / claim["proof"]["path"])}
        self.assertEqual(self.validate().returncode, 0)
        with (directory / "work.md").open("a") as handle:
            handle.write("\nFurther discussion which changes no submitted proof.\n")
        manifest["summary"] = self.ref(directory / "work.md")
        save(directory / "manifest.json", manifest)
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(frozen, {p: p.read_bytes() for p in frozen})

    def test_changed_statement_cannot_inherit_review_of_identical_proof_bytes(self) -> None:
        directory, manifest = self.session()
        path, claim = self.claim(directory)
        self.index(directory, manifest, path, claim)
        newer_path, newer = self.claim(directory, revision="v2", previous=self.ref(path))
        newer["proof"] = claim["proof"]
        newer["hypotheses"] = ["Additional regularity absent from the intended target"]
        newer["meaning_audit"] = {"status": "mismatch", "note": "Narrower than the approved statement."}
        save(newer_path, newer)
        manifest["claim_records"] = [self.ref(newer_path)]
        save(directory / "manifest.json", manifest)
        result = self.validate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLAIM_REVIEW_UNINDEXED", result.stdout)
        self.assertIn("CLAIM_MEANING_GATE", result.stdout)

    def test_self_review_and_reversed_read_order_cannot_clear_key_gate(self) -> None:
        directory, manifest = self.session()
        path, claim = self.claim(directory)
        review_path = self.index(directory, manifest, path, claim)
        review = json.loads(review_path.read_text())
        review["review_kind"] = "self_check"
        save(review_path, review)
        manifest["critical_reviews"] = [self.ref(review_path)]
        save(directory / "manifest.json", manifest)
        self.assertIn("CLAIM_REVIEW_REQUIRED", self.validate().stdout)
        review.update(review_kind="independent", baseline_frozen_before_candidate=False)
        save(review_path, review)
        manifest["critical_reviews"] = [self.ref(review_path)]
        save(directory / "manifest.json", manifest)
        result = self.validate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("CRITICAL_REVIEW_ORDER", result.stdout)

    def test_reuse_across_sessions_and_transitive_recheck_without_state_mutation(self) -> None:
        first, m1 = self.session()
        a_path, a = self.claim(first)
        alias = dict(self.ref(a_path))
        alias["path"] = alias["path"].replace("P001-v1.json", "./P001-v1.json")
        b_path, b = self.claim(first, "P002", dependencies=[{"claim_id": "P001", "revision": "v1", "record": alias}])
        self.index(first, m1, b_path, b, critical=False)
        original = {name: (self.root / name).read_bytes() for name in ("STATE.md", "research/proof_ledger.md", "research/machine/project-state.json")}
        second, m2 = self.session(2)
        # An unchanged proof/review can be reused without a new role task or copied proof.
        m2.update(claim_records=[self.ref(b_path)], critical_reviews=m1["critical_reviews"], critical_review_required=True)
        save(second / "manifest.json", m2)
        self.assertEqual(self.validate().returncode, 0)
        a2_path, _ = self.claim(second, revision="v2", previous=self.ref(a_path))
        m2["claim_records"].append(self.ref(a2_path))
        m2["critical_review_required"] = False
        save(second / "manifest.json", m2)
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CLAIM_RECHECK_REQUIRED", result.stdout)
        self.proposal(second, m2, b)
        result = self.validate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("STALE_CLAIM_USE", result.stdout)
        self.assertEqual(original, {name: (self.root / name).read_bytes() for name in original})

    def test_formal_changes_still_need_owner_approval_and_exact_claim_coverage(self) -> None:
        directory, manifest = self.session()
        path, claim = self.claim(directory)
        self.index(directory, manifest, path, claim)
        transition = self.proposal(directory, manifest, claim, status="owner_approved")
        self.assertIn("TRANSITION_APPROVAL", self.validate().stdout)
        transition["owner_approval_reference"] = "owner:synthetic-only"
        save(directory / "state-transition.json", transition)
        manifest["state_transition"] = self.ref(directory / "state-transition.json")
        save(directory / "manifest.json", manifest)
        self.assertEqual(self.validate().returncode, 0)
        transition["changes"]["claims"] = [{"id": "P002", "status": "verified"}]
        save(directory / "state-transition.json", transition)
        manifest["state_transition"] = self.ref(directory / "state-transition.json")
        save(directory / "manifest.json", manifest)
        self.assertIn("TRANSITION_CLAIM_COVERAGE", self.validate().stdout)

    def test_two_no_information_sessions_trigger_review_before_third_construction(self) -> None:
        for number in range(1, 4):
            directory, manifest = self.session(number, "none")
            manifest.update(route_id="route:synthetic", route_approval_reference="owner:synthetic", route_signal="null_result")
            save(directory / "manifest.json", manifest)
            if number == 2:
                result = self.validate()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("ROUTE_REVIEW_DUE", result.stdout)
        self.assertIn("ROUTE_REVIEW_BYPASSED", self.validate().stdout)

    def test_compute_budget_and_information_goal_are_real_constraints(self) -> None:
        directory, manifest = self.session()
        step = {"action": "change_model", "reason": "Resolve one exact missing lemma", "expected_information": "Independent coefficient recomputation",
                "stop_condition": "Coefficient determined or budget exhausted", "max_seconds": 2, "max_cost_usd": None,
                "status": "completed", "elapsed_seconds": 3, "cost_usd": None, "outcome": "No new result"}
        manifest["compute_steps"] = [step]
        save(directory / "manifest.json", manifest)
        self.assertIn("COMPUTE_BUDGET", self.validate().stdout)
        step["status"] = "stopped"
        save(directory / "manifest.json", manifest)
        self.assertEqual(self.validate().returncode, 0)
        step["max_seconds"] = -1
        save(directory / "manifest.json", manifest)
        self.assertIn("exclusiveMinimum", self.validate().stdout)

    def test_mixed_open_and_proved_claims_need_only_relevant_review_but_not_numerical_promotion(self) -> None:
        directory, manifest = self.session()
        path, claim = self.claim(directory)
        self.index(directory, manifest, path, claim)
        transition = self.proposal(directory, manifest, claim)
        transition["changes"]["claims"].append({"id": "P002", "status": "open"})
        save(directory / "state-transition.json", transition)
        manifest["state_transition"] = self.ref(directory / "state-transition.json")
        save(directory / "manifest.json", manifest)
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        task_path = directory / "T001.json"
        task = json.loads(task_path.read_text()); task["evidence_class"] = "numerical"; save(task_path, task)
        manifest["task_records"] = [self.ref(task_path)]
        save(directory / "manifest.json", manifest)
        result = self.validate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("NUMERICAL_PROMOTION", result.stdout)

    def test_malformed_compute_record_fails_cleanly_and_affected_query_is_read_only(self) -> None:
        directory, manifest = self.session()
        manifest["compute_steps"] = [{"action": "change_model", "status": "completed", "max_seconds": [], "elapsed_seconds": 2}]
        save(directory / "manifest.json", manifest)
        result = self.validate()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        import research_checks
        state = {"claims": [{"id": "P001", "depends_on": []}, {"id": "P002", "depends_on": ["P001"]},
                            {"id": "P003", "depends_on": ["P002"]}, {"id": "P004", "depends_on": []}]}
        before = copy.deepcopy(state)
        self.assertEqual(research_checks.affected(state, "P001"), ["P002", "P003"])
        self.assertEqual(state, before)


class ExecutableCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copy2(ROOT / "examples/ai4math/checks/evaluator.py", self.root / "evaluator.py")
        shutil.copy2(ROOT / "examples/ai4math/checks/polynomial.json", self.root / "candidate.json")

    def plan(self, command: list | None = None, timeout: float = 10) -> Path:
        value = {"schema_version": "1.0", "kind": "symbolic", "scope": "Exact supplied rational coefficients only",
                 "candidate": evidencectl.file_ref(self.root, "candidate.json"), "evaluator": evidencectl.file_ref(self.root, "evaluator.py"),
                 "inputs": [], "command": command or ["{python}", "{evaluator}", "{candidate}"], "timeout_seconds": timeout,
                 "evaluator_review": "Synthetic fixture, not a mathematical acceptance", "limitations": ["Not a PDE proof"]}
        save(self.root / "plan.json", value)
        return self.root / "plan.json"

    def test_inspect_does_not_execute_and_run_records_exact_feedback(self) -> None:
        (self.root / "evaluator.py").write_text("from pathlib import Path\nprint('{\"outcome\":\"passed\"}')\nPath('executed').write_text('yes')\n")
        path = self.plan()
        result = subprocess.run(["python3", str(ROOT / "tools/checkctl.py"), str(path), "--root", str(self.root)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / "executed").exists())
        receipt = checkctl.execute(path, self.root, "result.json")
        self.assertEqual(receipt["outcome"], "passed")
        self.assertTrue((self.root / "executed").exists())
        self.assertEqual(checkctl.inspect_result(receipt, self.root), [])
        with self.assertRaises(ValueError):
            checkctl.execute(path, self.root, "result.json")

    def test_rational_check_passes_and_scale_obstruction_is_exactly_scoped(self) -> None:
        receipt = checkctl.execute(self.plan(), self.root, "identity.json")
        self.assertEqual(receipt["outcome"], "passed")
        shutil.copy2(ROOT / "examples/ai4math/checks/scale-failure.json", self.root / "candidate.json")
        path = self.plan()
        value = json.loads(path.read_text()); value["kind"] = "scale"; save(path, value)
        result = checkctl.execute(path, self.root, "scale.json")
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["evaluation"]["ratio_exponent"], "-1")
        self.assertEqual(result["execution"]["exit_code"], 0)

    def test_timeout_and_runtime_error_are_inconclusive_not_counterexamples(self) -> None:
        (self.root / "evaluator.py").write_text("import time\ntime.sleep(1)\nprint('{\"outcome\":\"passed\"}')\n")
        result = checkctl.execute(self.plan(timeout=.03), self.root, "timeout.json")
        self.assertEqual(result["outcome"], "inconclusive")
        self.assertTrue(result["execution"]["timed_out"])
        (self.root / "evaluator.py").write_text("print('{\"outcome\":\"passed\"}')\nraise RuntimeError('synthetic failure')\n")
        result = checkctl.execute(self.plan(), self.root, "runtime.json")
        self.assertEqual(result["outcome"], "inconclusive")
        self.assertIn("synthetic failure", result["stderr"])

    def test_input_tampering_and_unsafe_paths_fail_without_false_pass(self) -> None:
        (self.root / "evaluator.py").write_text("from pathlib import Path\nPath('candidate.json').write_text('{}')\nprint('{\"outcome\":\"passed\"}')\n")
        result = checkctl.execute(self.plan(), self.root, "tampered.json")
        self.assertEqual(result["outcome"], "inconclusive")
        self.assertFalse(result["inputs_unchanged"])
        self.assertTrue(checkctl.inspect_result(result, self.root))
        path = self.plan()
        with self.assertRaises(ValueError):
            checkctl.execute(path, self.root, "../escape.json")
        (self.root / "evaluator.py").write_text("from pathlib import Path\nPath('STATE.md').write_text('collateral edit')\nprint('{\"outcome\":\"passed\"}')\n")
        collateral = checkctl.execute(self.plan(), self.root, "collateral.json")
        self.assertEqual(collateral["outcome"], "inconclusive")
        self.assertFalse(collateral["protected_files_unchanged"])
        linked = self.root / "linked"
        linked.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            checkctl.execute(path, self.root, "linked/escape.json")


class BenchmarkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "examples/benchmark", self.root / "examples/benchmark")
        self.suite_ref = evidencectl.file_ref(self.root, "examples/benchmark/suite.json")

    def records(self) -> tuple[dict, dict]:
        suite = benchctl.load_suite(self.suite_ref, self.root)
        entries = []
        for config in suite["configurations"]:
            for case in suite["cases"]:
                name = f"answers/{config['id']}-{case['id']}.md"
                path = self.root / name; path.parent.mkdir(exist_ok=True)
                wrong = config["id"] == "direct" and case["id"] == "quantifiers"
                path.write_text("Incorrect universal extrapolation from finite tests." if wrong else "Synthetic answer with exact intended scope.")
                entries.append({"case_id": case["id"], "configuration_id": config["id"],
                                "answer": evidencectl.file_ref(self.root, name), "disposition": "accepted" if wrong else case["expected_disposition"],
                                "usage": {"wall_seconds": 121 if wrong else 3, "cost_usd": None if config["id"] == "direct" else .05}})
        value = {"suite": self.suite_ref, "submissions": entries}
        save(self.root / "submissions.json", value)
        return value, evidencectl.file_ref(self.root, "submissions.json")

    def test_packets_exclude_reference_answers_and_blind_output_excludes_configuration(self) -> None:
        packets = benchctl.prepare(self.suite_ref, self.root, "packets")
        for path in (packets / "inputs").rglob("task.json"):
            self.assertNotIn("expected_disposition", path.read_text())
            self.assertNotIn("references/", path.read_text())
            self.assertNotIn("reference", json.loads(path.read_text()))
        _, reference = self.records()
        blinded = benchctl.blind(reference, self.root, "blinded")
        answers = json.loads((blinded / "review/answers.json").read_text())
        self.assertEqual(len(answers), 8)
        self.assertTrue(all(set(answer) == {"id", "question", "context", "answer"} for answer in answers))
        self.assertTrue(all(answer["question"] for answer in answers))
        self.assertTrue((blinded / "owner/key.json").exists())

    def test_scoring_separates_false_accepts_scope_review_time_and_unknown_costs(self) -> None:
        _, reference = self.records()
        blinded = benchctl.blind(reference, self.root, "blinded")
        key = json.loads((blinded / "owner/key.json").read_text())
        grades = []
        for mapping in key["mapping"]:
            wrong = mapping["configuration_id"] == "direct" and mapping["case_id"] == "quantifiers"
            grades.append({"id": mapping["id"], "correctness": 0 if wrong else 2, "exposition": 1, "attribution": 2,
                           "meaning_matched": not wrong, "gap_closed": False, "reproducible": not wrong, "review_minutes": 2})
        result = benchctl.score(key, grades, self.root)
        direct = result["configurations"]["direct"]
        self.assertEqual(direct["false_accepts"], 1)
        self.assertEqual(direct["meaning_mismatches"], 1)
        self.assertEqual(direct["unknown_cost_cases"], 4)
        self.assertEqual(direct["budget_overruns"], 1)
        self.assertEqual(direct["review_minutes"], 8)
        self.assertEqual(result["purpose"], "mechanics_only")
        self.assertEqual(result["configurations"]["feedback"]["fully_correct"], 4)
        grades[0]["correctness"] = None
        with self.assertRaises(ValueError):
            benchctl.score(key, grades, self.root)

    def test_incomplete_or_confounded_comparisons_are_not_accepted(self) -> None:
        value, reference = self.records()
        value["submissions"].pop()
        save(self.root / "submissions.json", value)
        with self.assertRaises(ValueError):
            benchctl.blind(evidencectl.file_ref(self.root, "submissions.json"), self.root, "incomplete")
        self.assertFalse((self.root / "incomplete").exists())
        suite = json.loads((self.root / "examples/benchmark/suite.json").read_text())
        suite["configurations"][1]["model"] = "different-model"
        save(self.root / "examples/benchmark/suite.json", suite)
        with self.assertRaises(ValueError):
            benchctl.prepare(evidencectl.file_ref(self.root, "examples/benchmark/suite.json"), self.root, "confounded")
        self.assertFalse((self.root / "confounded").exists())
        suite["configurations"][1]["model"] = suite["configurations"][0]["model"]
        suite["cases"][0]["context"] = [suite["cases"][0]["reference"]]
        save(self.root / "examples/benchmark/suite.json", suite)
        with self.assertRaises(ValueError):
            benchctl.prepare(evidencectl.file_ref(self.root, "examples/benchmark/suite.json"), self.root, "leaking")
        self.assertFalse((self.root / "leaking").exists())


if __name__ == "__main__":
    unittest.main()
