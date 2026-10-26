"""CLI integration tests using isolated fixtures; never query the real library."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
TEXTURA_ROOT = Path(__file__).resolve().parents[3]
CLI = TEXTURA_ROOT / "Runner" / "current" / "textura.py"
COMPONENTS = (
    "Governance", "Configuration", "Contracts", "Runner", "Topics", "Research",
    "Sources", "Reading", "Translation", "Evidence", "Analysis", "Writing",
    "Style", "Fiction", "Review", "State", "Publishing", "Feedback", "LibraryBridge", "Quality",
)


class CliTests(unittest.TestCase):
    def setUp(self):
        outputs = TEXTURA_ROOT / "Quality" / "current" / "outputs"
        outputs.mkdir(parents=True, exist_ok=True)
        self.boundary = outputs.resolve()
        self.temporary = tempfile.TemporaryDirectory(prefix="cli-", dir=outputs)
        self.fixture = Path(self.temporary.name).resolve()
        self.root = self.fixture / "installation"
        self.caller = self.fixture / "caller"
        self.library = self.fixture / "library"
        self.caller.mkdir()
        for component in COMPONENTS:
            (self.root / component / "current").mkdir(parents=True)
            (self.root / component / "history").mkdir()
        (self.library / "tools").mkdir(parents=True)
        (self.library / "AGENTS.md").write_text("# Isolated test library\n", encoding="utf-8")
        (self.library / "tools" / "bm.mjs").write_text("// Never execute this fixture.\n", encoding="utf-8")
        self.write_json(self.root / "Configuration" / "current" / "settings.json", {
            "release": "0.1.0-test",
            "bibliotheca": {"enabled": True, "root": str(self.library)},
        })
        self.write_json(self.root / "Configuration" / "current" / "components.json", {
            "components": [{"name": name, "depends_on": []} for name in COMPONENTS],
        })
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")

    def tearDown(self):
        # Resolve and verify the exact target before recursive temporary cleanup.
        target = self.fixture.resolve()
        if target == self.boundary or not target.is_relative_to(self.boundary):
            raise ValueError("Refusing cleanup outside the CLI fixture boundary")
        if not target.name.startswith("cli-"):
            raise ValueError("Refusing cleanup of a non-fixture directory")
        self.temporary.cleanup()

    @staticmethod
    def write_json(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

    def input(self, filename, text):
        path = self.caller / filename
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def execute(self, *arguments, success=True):
        result = subprocess.run(
            [sys.executable, "-B", str(CLI), "--root", str(self.root), *map(str, arguments)],
            cwd=self.caller, env=self.env, capture_output=True, text=True,
            encoding="utf-8", timeout=30, shell=False,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertEqual(result.stderr, "", result.stderr)
            payload = json.loads(result.stdout)
            self.assertIsInstance(payload, dict)
            return payload
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertTrue(result.stderr.strip())
        self.assertNotIn("Traceback (most recent call last)", result.stderr)
        return result

    def files(self):
        return {
            path.relative_to(self.fixture).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.fixture.rglob("*") if path.is_file()
        }

    def cli_module(self):
        spec = importlib.util.spec_from_file_location("textura_cli_integration", CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_json_workflow_from_a_directory_outside_the_code(self):
        topic = self.execute("topic", "--title", "多语种研究", "--policy", "local_only")
        work = self.execute("work", "--title", "Über Quellen 与论证", "--topic", topic["id"],
                            "--language", "zh", "--genre", "essay")
        original = self.input("公开资料 Ä.txt", "Background\n可核查的原文。\n")
        source = self.execute("source", "--title", "Original material", "--file", original,
                              "--scope", "partial", "--policy", "local_only")
        reading = self.execute("read", source["id"])
        draft_path = self.input("作者初稿.md", "A bounded interpretation.\n")
        draft = self.execute("draft", work["id"], "--file", draft_path)
        claim = self.execute("claim", "--work", work["id"], "--statement", "可核查的原文。",
                             "--kind", "quotation", "--priority", "high")
        reference_file = self.caller / "evidence.json"
        self.write_json(reference_file, [{"reading_id": reading["id"], "locator": "line[2]",
                                          "excerpt": "可核查的原文。"}])
        assessment = self.execute("assess", claim["id"], "--verdict", "supported",
                                  "--rationale", "The quoted wording is present in the acquired text.",
                                  "--evidence-file", reference_file)
        decision = self.execute("decision", "--kind", "author_decision", "--text", "Keep the ending",
                                "--work", work["id"], "--basis", "Explicit fixture author instruction")
        handoff = self.execute("handoff", "--work", work["id"])

        self.assertEqual(work["topic_id"], topic["id"])
        self.assertEqual(source["original_name"], original.name)
        self.assertEqual(source["capture_scope"], "partial")
        self.assertEqual(reading["source_id"], source["id"])
        self.assertEqual(reading["source_sha256"], source["sha256"])
        self.assertEqual(claim["draft_id"], draft["id"])
        self.assertEqual(assessment["evidence"][0]["source_id"], source["id"])
        self.assertEqual(assessment["validation_scope"], "reference_integrity_only")
        self.assertIn(claim["id"], handoff["claim_ids"])
        self.assertIn(decision["id"], [item["id"] for item in handoff["decisions"]])
        self.assertEqual(handoff["active_drafts"][0]["draft_id"], draft["id"])
        for record in (work, reading, draft, claim, assessment, decision, handoff):
            self.assertEqual(record["processing_policy"], "local_only")
        self.assertEqual(original.read_text(encoding="utf-8"), "Background\n可核查的原文。\n")
        self.assertEqual(draft_path.read_text(encoding="utf-8"), "A bounded interpretation.\n")
        self.assertEqual({path.name for path in self.root.iterdir()}, set(COMPONENTS))

    def test_link_only_source_is_honest_and_cannot_be_read(self):
        lead = self.execute("source", "--title", "URL only", "--url", "https://example.invalid/article",
                            "--scope", "complete")
        self.assertEqual(lead["capture_scope"], "link_only")
        self.assertIsNone(lead["sha256"])
        self.assertIsNone(lead["original_file"])
        result = self.execute("read", lead["id"], success=False)
        self.assertIn("no acquired content", json.loads(result.stderr)["error"])

    def test_free_verse_review_defaults_to_blind_packets(self):
        work = self.execute("work", "--title", "INTENT_SECRET_NOT_FOR_FIRST_READER",
                            "--language", "en", "--genre", "free_verse")
        poem = "First line\nSecond line\n\nNew stanza\n"
        draft = self.execute("draft", work["id"], "--file", self.input("poem.txt", poem))
        review = self.execute("review", "prepare", work["id"])
        self.assertTrue(review["poetry_blind"])
        self.assertEqual(review["draft_id"], draft["id"])
        self.assertEqual(review["phase"], "independent_packets_ready")
        self.assertEqual(review["model_execution"], "not_performed")
        self.assertEqual(review["independence_status"], "not_demonstrated")
        folder = self.root / review["record_path"]
        recognition = (folder / "packets" / "recognition" / "factual-input.json").read_bytes()
        challenge = (folder / "packets" / "challenge" / "factual-input.json").read_bytes()
        self.assertEqual(recognition, challenge)
        self.assertNotIn(b"INTENT_SECRET", recognition)
        factual = json.loads(recognition.decode("utf-8"))
        self.assertEqual(factual["language"], "en")
        self.assertEqual(factual["draft_text"].rstrip("\n"), poem.rstrip("\n"))
        status = self.execute("review", "status", review["id"])
        self.assertFalse(status["stale"])

    def test_invalid_inputs_fail_without_a_python_traceback(self):
        cases = (
            ("work", "--title", "Missing required language"),
            ("source", "--title", "No content or URL"),
            ("source", "--title", "Bad URL", "--url", "file:///private"),
            ("claim", "--statement", "No owning work or topic"),
            ("decision", "--kind", "author_decision", "--text", "Consent was not supplied"),
            ("read", "../escape"),
            ("not-a-command",),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                self.execute(*arguments, success=False)
        self.assertFalse((self.root / "Sources" / "current" / "records").exists())
        self.assertFalse((self.root / "Evidence" / "current" / "records").exists())

    def test_status_and_doctor_are_read_only_and_do_not_claim_remote_checks(self):
        before = self.files()
        status = self.execute("status")
        doctor = self.execute("doctor")
        self.assertEqual(Path(status["root"]), self.root)
        self.assertEqual(status["release"], "0.1.0-test")
        self.assertFalse(status["automatic_model_calls"])
        self.assertEqual(len(status["components"]), len(COMPONENTS))
        for flag in ("network_tested", "accounts_tested", "models_executed"):
            self.assertIs(doctor[flag], False)
        self.assertEqual(self.files(), before)

    def test_bm_cli_forwards_locator_options_to_the_bridge(self):
        module = self.cli_module()
        import library_bridge
        arguments = module.parser().parse_args([
            "--root", str(self.root), "bm", "cite", "BM-R-example", "--version", "v001",
            "--file", "F01", "--extraction", "E01", "--line", "7",
        ])
        with mock.patch.object(library_bridge, "run", return_value={"mocked": True}) as bridge:
            self.assertEqual(module.dispatch(arguments), {"mocked": True})
        bridge.assert_called_once_with(self.root, "cite", "BM-R-example",
                                       version="v001", file="F01", extraction="E01", line="7")

    def test_bm_bridge_uses_positional_search_and_exact_citation_arguments(self):
        self.cli_module()
        import library_bridge
        response = subprocess.CompletedProcess([], 0, stdout='{"fixture": true}', stderr="")
        with mock.patch.object(library_bridge, "node_binary", return_value="fixture-node"), \
                mock.patch.object(library_bridge.subprocess, "run", return_value=response) as runner:
            result = library_bridge.run(self.root, "search", "哲学 -- literal search")
            self.assertFalse(result["write_performed"])
            self.assertEqual(runner.call_args.args[0], ["fixture-node", str(self.library / "tools" / "bm.mjs"),
                                                       "search", "哲学 -- literal search"])
            self.assertIs(runner.call_args.kwargs["shell"], False)
            self.assertEqual(runner.call_args.kwargs["cwd"], self.library)
            library_bridge.run(self.root, "cite", "BM-R-example", version="v001", file="F01",
                               extraction="E01", line=7)
            self.assertEqual(runner.call_args.args[0], ["fixture-node", str(self.library / "tools" / "bm.mjs"),
                "cite", "BM-R-example", "--version", "v001", "--file", "F01", "--extraction", "E01", "--line", "7"])
            count = runner.call_count
            with self.assertRaises(ValueError):
                library_bridge.run(self.root, "search", "query", line="7")
            self.assertEqual(runner.call_count, count)

    def test_powershell_launcher_from_external_cwd_when_available(self):
        powershell = shutil.which("powershell") or shutil.which("pwsh")
        launcher = TEXTURA_ROOT / "Runner" / "current" / "textura.ps1"
        if not powershell or not launcher.is_file():
            self.skipTest("PowerShell launcher is unavailable on this test host")
        before = self.files()
        for command in ("status", "doctor"):
            with self.subTest(command=command):
                result = subprocess.run(
                    [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(launcher),
                     "--root", str(self.root), command], cwd=self.caller,
                    env=dict(self.env, TEXTURA_PYTHON=sys.executable),
                    capture_output=True, text=True, encoding="utf-8", timeout=30, shell=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
                payload = json.loads(result.stdout.lstrip("\ufeff"))
                self.assertIn("system" if command == "status" else "python", payload)
        self.assertEqual(self.files(), before)


if __name__ == "__main__":
    unittest.main()
