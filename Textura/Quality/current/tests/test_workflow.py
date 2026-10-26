"""Integration checks against isolated local records, never the live library."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

TEXTURA_ROOT = Path(__file__).resolve().parents[3]
COMPONENTS = (
    "Configuration", "Contracts", "Topics", "Sources", "Reading", "Writing",
    "Evidence", "State", "Review", "Runner", "Quality",
)
for component in COMPONENTS:
    sys.path.insert(0, str(TEXTURA_ROOT / component / "current"))

import evidence
import maintenance
import sources
import state_records
import storage
import topics
import writing


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        outputs = TEXTURA_ROOT / "Quality" / "current" / "outputs"
        outputs.mkdir(parents=True, exist_ok=True)
        self.fixture_boundary = outputs.resolve()
        self.temp = tempfile.TemporaryDirectory(prefix="workflow-", dir=outputs)
        self.root = Path(self.temp.name)
        for name in COMPONENTS:
            current = self.root / name / "current"
            current.mkdir(parents=True)
            (self.root / name / "history").mkdir()
            (current / "README.md").write_text(f"# {name}\n\nIsolated test fixture.\n", encoding="utf-8")
            self.json(current / "component.json", {"name": name, "version": "0.1.0"})
        self.json(self.root / "Configuration" / "current" / "components.json", {
            "components": [{"name": name, "depends_on": []} for name in COMPONENTS]
        })
        for name in COMPONENTS:
            maintenance.seal(self.root, name)
        self.inputs = self.root / "Quality" / "current" / "outputs"
        self.inputs.mkdir()

    def tearDown(self):
        # Verify the resolved target before the recursive temporary-fixture cleanup.
        if not self.root.resolve().is_relative_to(self.fixture_boundary) or self.root.resolve() == self.fixture_boundary:
            raise ValueError("Refusing cleanup outside this test's isolated fixture")
        self.temp.cleanup()

    @staticmethod
    def json(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

    def input(self, name="资料.txt", text="First line\n实际引文：证据仍需判断。\nLast line\n"):
        path = self.inputs / name
        path.write_text(text, encoding="utf-8")
        return path

    def work(self, policy="cloud_allowed", topic_id=None):
        return topics.create(self.root, "work", "作者的文章", language="zh", genre="essay",
                             processing_policy=policy, topic_id=topic_id)

    def captured(self, policy="cloud_allowed"):
        original = self.input()
        source = sources.register(self.root, title="可追溯资料", file=original, scope="complete",
                                  processing_policy=policy, url="https://example.invalid/source")
        reading = sources.read_source(self.root, source["id"])
        return source, reading

    @staticmethod
    def reference(reading):
        return {"reading_id": reading["id"], "locator": "line[2]", "excerpt": "实际引文：证据仍需判断。"}

    def test_exact_source_hash_original_filename_and_reading_binding(self):
        original = self.input("德文与中文 Ä.txt", "Grüße\n真实材料\n")
        raw = original.read_bytes()
        source = sources.register(self.root, title="Über Quellen", file=original, scope="partial")
        stored = storage.owned(self.root, "Sources", "records", source["id"], source["original_file"])
        self.assertEqual(source["original_name"], original.name)
        self.assertEqual(source["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(stored.read_bytes(), raw)
        self.assertEqual(source["capture_scope"], "partial")
        self.assertEqual(source["verification_status"], "unassessed")
        reading = sources.read_source(self.root, source["id"])
        self.assertEqual(reading["source_sha256"], source["sha256"])
        self.assertEqual(reading["blocks"][1], {"locator": "line[2]", "text": "真实材料"})
        self.assertTrue(maintenance.validate(self.root)["valid"])

    def test_link_only_record_cannot_claim_to_have_read_content(self):
        source = sources.register(self.root, title="Known URL only", url="https://example.invalid/article", scope="complete")
        self.assertEqual(source["capture_scope"], "link_only")
        self.assertIsNone(source["sha256"])
        self.assertIsNone(source["original_file"])
        with self.assertRaisesRegex(ValueError, "no acquired content"):
            sources.read_source(self.root, source["id"])
        self.assertEqual(storage.records(self.root, "Reading", "readings"), [])

    def test_modified_original_is_rejected_and_detected_by_validation(self):
        source, reading = self.captured()
        captured = storage.owned(self.root, "Sources", "records", source["id"], source["original_file"])
        captured.write_text("tampered content", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "digest changed"):
            sources.read_source(self.root, source["id"])
        with self.assertRaisesRegex(ValueError, "original was changed"):
            evidence.check_reference(self.root, self.reference(reading))
        result = maintenance.validate(self.root)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Source changed" in error for error in result["errors"]))

    def test_drafts_are_immutable_and_identical_import_is_noop(self):
        work = self.work()
        path = self.input("初稿 — français.md", "Initial text\n")
        first = writing.import_draft(self.root, work["id"], path)
        folder = storage.owned(self.root, "Writing", "records", work["id"], "drafts", first["id"])
        original_bytes = (folder / first["original_file"]).read_bytes()
        manifest_bytes = (folder / "manifest.json").read_bytes()
        repeated = writing.import_draft(self.root, work["id"], path)
        self.assertEqual(repeated["id"], first["id"])
        self.assertTrue(repeated["reused_existing_snapshot"])
        self.assertEqual((folder / "manifest.json").read_bytes(), manifest_bytes)
        path.write_text("Author-selected revision\n", encoding="utf-8")
        second = writing.import_draft(self.root, work["id"], path)
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(second["previous_draft_id"], first["id"])
        self.assertEqual(writing.latest(self.root, work["id"])["id"], second["id"])
        self.assertEqual((folder / first["original_file"]).read_bytes(), original_bytes)
        self.assertEqual((folder / "manifest.json").read_bytes(), manifest_bytes)
        self.assertEqual(len(list(folder.parent.glob("*/manifest.json"))), 2)

    def test_noop_import_refuses_a_tampered_saved_snapshot(self):
        work = self.work()
        path = self.input("draft.md", "Original version")
        draft = writing.import_draft(self.root, work["id"], path)
        stored = storage.owned(self.root, "Writing", "records", work["id"], "drafts", draft["id"], draft["original_file"])
        stored.write_text("Unexpected edit", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "altered"):
            writing.import_draft(self.root, work["id"], path)
        result = maintenance.validate(self.root)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Draft original changed" in error for error in result["errors"]))

    def test_evidence_uses_actual_excerpt_locator_and_draft_version(self):
        work = self.work()
        draft = writing.import_draft(self.root, work["id"], self.input("draft.md", "A bounded argument"))
        source, reading = self.captured()
        claim = evidence.claim(self.root, "资料表达了这一判断。", work_id=work["id"], kind="quotation", priority="high")
        assessment = evidence.assess(self.root, claim["id"], "supported", "Recorded assessor judgment with a directly located quotation.", [self.reference(reading)])
        self.assertEqual(claim["draft_id"], draft["id"])
        ref = assessment["evidence"][0]
        self.assertEqual(ref["source_id"], source["id"])
        self.assertEqual(ref["source_sha256"], source["sha256"])
        self.assertEqual(ref["locator"], "line[2]")
        self.assertEqual(ref["excerpt"], "实际引文：证据仍需判断。")
        self.assertEqual(assessment["validation_scope"], "reference_integrity_only")
        self.assertEqual(assessment["semantic_review_status"], "assessor_judgment_recorded")
        self.assertTrue(maintenance.validate(self.root)["valid"])

    def test_wrong_locator_fabricated_excerpt_and_empty_excerpt_are_refused(self):
        source, reading = self.captured()
        variants = [
            {**self.reference(reading), "locator": "physical-page[999]"},
            {**self.reference(reading), "excerpt": "A fabricated quotation"},
            {**self.reference(reading), "locator": "line[1]"},
            {**self.reference(reading), "excerpt": "   "},
        ]
        for ref in variants:
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                evidence.check_reference(self.root, ref)
        with self.assertRaises(FileNotFoundError):
            evidence.check_reference(self.root, {**self.reference(reading), "reading_id": "reading-absent"})

    def test_decisive_verdicts_require_references_but_inconclusive_does_not(self):
        work = self.work()
        claim = evidence.claim(self.root, "A claim with an evidence gap", work_id=work["id"])
        for verdict in ("supported", "contradicted", "mixed"):
            with self.subTest(verdict=verdict), self.assertRaisesRegex(ValueError, "require checkable evidence"):
                evidence.assess(self.root, claim["id"], verdict, "No acquired evidence", [])
        self.assertEqual(storage.records(self.root, "Evidence", "assessments"), [])
        assessment = evidence.assess(self.root, claim["id"], "inconclusive", "The necessary source has not been acquired.", [])
        self.assertEqual(assessment["verdict"], "inconclusive")
        handoff = state_records.handoff(self.root, work["id"])
        self.assertIn("Assessment existence does not mean supported", handoff["notice"])

    def test_source_local_only_policy_flows_to_assessment_and_handoff(self):
        work = self.work()
        source, reading = self.captured("local_only")
        claim = evidence.claim(self.root, "Public work, restricted evidence", work_id=work["id"])
        self.assertEqual(work["processing_policy"], "cloud_allowed")
        self.assertEqual(claim["processing_policy"], "cloud_allowed")
        self.assertEqual(reading["processing_policy"], "local_only")
        assessment = evidence.assess(self.root, claim["id"], "supported", "Local-only evidence was consulted.", [self.reference(reading)])
        self.assertEqual(assessment["processing_policy"], "local_only")
        self.assertEqual(assessment["evidence"][0]["processing_policy"], "local_only")
        handoff = state_records.handoff(self.root, work["id"])
        self.assertEqual(handoff["processing_policy"], "local_only")
        self.assertEqual(state_records.handoff(self.root)["processing_policy"], "local_only")

    def test_superseding_assessment_cannot_drop_inherited_privacy(self):
        work = self.work()
        source, reading = self.captured("local_only")
        claim = evidence.claim(self.root, "A restricted assessment history", work_id=work["id"])
        previous = evidence.assess(self.root, claim["id"], "supported", "Restricted source consulted", [self.reference(reading)])
        revised = evidence.assess(self.root, claim["id"], "inconclusive", "The previous reasoning needs review", [], supersedes=previous["id"])
        self.assertEqual(revised["processing_policy"], "local_only")

    def test_reference_does_not_invent_original_inspection(self):
        source, reading = self.captured()
        checked = evidence.check_reference(self.root, self.reference(reading))
        self.assertIsNone(checked["original_inspected"])
        checked_explicit = evidence.check_reference(self.root, {**self.reference(reading), "original_inspected": False,
                    "attribution_chain": ["Quoted by the source actually read"]})
        self.assertIs(checked_explicit["original_inspected"], False)
        self.assertEqual(checked_explicit["attribution_chain"], ["Quoted by the source actually read"])

    def test_reference_rejects_conflicting_source_version_and_reading_hash(self):
        source, reading = self.captured()
        variants = [
            {"source_id": "source-other"},
            {"source_sha256": "0" * 64},
            {"reading_sha256": "0" * 64},
        ]
        for conflict in variants:
            with self.subTest(conflict=conflict), self.assertRaises(ValueError):
                evidence.check_reference(self.root, {**self.reference(reading), **conflict})

    def test_topic_only_claims_survive_global_and_related_work_handoffs(self):
        topic = topics.create(self.root, "topic", "长期议题", processing_policy="local_only")
        topic_claim = evidence.claim(self.root, "Topic research before any work", topic_id=topic["id"])
        global_handoff = state_records.handoff(self.root)
        self.assertIn(topic_claim["id"], global_handoff["claim_ids"])
        self.assertIn(topic_claim["id"], global_handoff["unassessed_claim_ids"])
        self.assertEqual(global_handoff["processing_policy"], "local_only")
        work = self.work(topic_id=topic["id"])
        unrelated_topic = topics.create(self.root, "topic", "Other topic")
        unrelated_claim = evidence.claim(self.root, "Unrelated topic research", topic_id=unrelated_topic["id"])
        related_handoff = state_records.handoff(self.root, work["id"])
        self.assertIn(topic_claim["id"], related_handoff["claim_ids"])
        self.assertNotIn(unrelated_claim["id"], related_handoff["claim_ids"])

    def test_source_original_cannot_escape_its_own_record_directory(self):
        public_path = self.input("public.txt", "Public original")
        private_path = self.input("private.txt", "Restricted original")
        public = sources.register(self.root, title="Public", file=public_path)
        private = sources.register(self.root, title="Private", file=private_path, processing_policy="local_only")
        manifest = storage.owned(self.root, "Sources", "records", public["id"], "manifest.json")
        altered = json.loads(manifest.read_text(encoding="utf-8"))
        altered["original_file"] = f"../{private['id']}/{private['original_file']}"
        altered["sha256"] = private["sha256"]
        self.json(manifest, altered)
        with self.assertRaises(ValueError):
            sources.read_source(self.root, public["id"])

    def test_topic_policy_flows_to_work_draft_claim_decision_and_handoff(self):
        topic = topics.create(self.root, "topic", "私人议题", processing_policy="local_only")
        work = self.work(topic_id=topic["id"])
        draft = writing.import_draft(self.root, work["id"], self.input("private.md", "Private draft"))
        claim = evidence.claim(self.root, "Private proposition", work_id=work["id"])
        decision = state_records.decision(self.root, "author_decision", "Keep this wording", work_id=work["id"], basis="Explicit author instruction in this fixture")
        handoff = state_records.handoff(self.root, work["id"])
        for record in (work, draft, claim, decision, handoff):
            self.assertEqual(record["processing_policy"], "local_only")
        self.assertIn(claim["id"], handoff["unassessed_claim_ids"])
        self.assertEqual(handoff["active_drafts"][0]["draft_id"], draft["id"])

    def test_snapshot_is_component_local_and_excludes_runtime_records(self):
        work = self.work()
        writing.import_draft(self.root, work["id"], self.input("snapshot.md", "Not a definition"))
        record = maintenance.snapshot(self.root, "Writing", "Before a definition change")
        self.assertEqual(record["archive_id"], "v0001")
        archive = self.root / "Writing" / "history" / "v0001"
        self.assertTrue((archive / "version.json").is_file())
        self.assertTrue((archive / "snapshot" / "README.md").is_file())
        self.assertFalse((archive / "snapshot" / "records").exists())
        self.assertFalse(any("records/" in p for p in record["files"]))
        self.assertEqual(list((self.root / "Sources" / "history").iterdir()), [])
        self.assertTrue(maintenance.validate(self.root)["valid"])

    def test_active_and_historical_definition_tampering_are_detected(self):
        self.assertTrue(maintenance.validate(self.root)["valid"])
        maintenance.snapshot(self.root, "Writing", "Preserve the initial definitions")
        active = self.root / "Writing" / "current" / "README.md"
        active.write_text("An unsealed change", encoding="utf-8")
        result = maintenance.validate(self.root)
        self.assertFalse(result["valid"])
        self.assertTrue(any("active definitions differ" in error for error in result["errors"]))
        maintenance.seal(self.root, "Writing")
        self.assertTrue(maintenance.validate(self.root)["valid"])
        historical = self.root / "Writing" / "history" / "v0001" / "snapshot" / "README.md"
        historical.write_text("An impermissible history rewrite", encoding="utf-8")
        result = maintenance.validate(self.root)
        self.assertFalse(result["valid"])
        self.assertTrue(any("historical snapshot mismatch" in error for error in result["errors"]))

    def test_invalid_identifiers_and_escape_paths_are_rejected(self):
        for value in ("../escape", "A/escape", "A\\escape", "A:stream", "CON", "研究", "", "."):
            with self.subTest(value=value), self.assertRaises(ValueError):
                storage.identifier(value)
        with self.assertRaises(ValueError):
            storage.require_record(self.root, "Evidence", "claims", "../escape")
        with self.assertRaises(ValueError):
            storage.owned(self.root, "Evidence", "..", "..", "..", "outside.json")
        with self.assertRaises(ValueError):
            storage.inside(self.root / "Evidence", self.root / "Writing" / "current")
        with self.assertRaises(ValueError):
            storage.mkdir(self.root / "Evidence" / "current" / "非ASCII目录", self.root / "Evidence")
        for alias in ("sources", "SOURCES", "SourceS"):
            with self.subTest(component_alias=alias), self.assertRaises(ValueError):
                storage.owned(self.root, alias, "records")

    def test_author_decisions_require_a_basis_and_never_become_proposals(self):
        work = self.work()
        with self.assertRaisesRegex(ValueError, "explicit basis"):
            state_records.decision(self.root, "author_decision", "Invented consent", work_id=work["id"])
        proposal = state_records.decision(self.root, "ai_proposal", "Possible next step", work_id=work["id"])
        handoff = state_records.handoff(self.root, work["id"])
        self.assertEqual(proposal["kind"], "ai_proposal")
        self.assertEqual(handoff["decisions"][0]["kind"], "ai_proposal")


if __name__ == "__main__":
    unittest.main()
