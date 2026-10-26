"""Contract tests for immutable review preparation and honest stage advancement."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "review.py"
spec = importlib.util.spec_from_file_location("textura_review", MODULE)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


class ReviewTests(unittest.TestCase):
    def setUp(self):
        base = Path(__file__).resolve().parent / "runtime"
        base.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="fixture_", dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.work = {"id": "work-one", "title": "Secret title", "language": "zh", "genre": "free_verse", "author_intention": "Never expose this in blind input", "processing_policy": "cloud_allowed"}
        write_json(self.root / "Topics/current/records/work/work-one.json", self.work)
        self.make_draft("draft-one", "夜色\n停在窗沿")
        write_json(self.root / "Evidence/current/records/claims/claim-one.json", {"id": "claim-one", "work_id": "work-one", "statement": "Interpretive secret", "processing_policy": "local_only"})
        write_json(self.root / "Evidence/current/records/assessments/assessment-one.json", {"id": "assessment-one", "claim_id": "claim-one", "verdict": "inconclusive", "rationale": "Unresolved", "evidence": []})

    def make_draft(self, draft_id, text, suffix=".txt", reading=None):
        folder = self.root / "Writing/current/records/work-one/drafts" / draft_id
        folder.mkdir(parents=True)
        data = text.encode("utf-8")
        original_file = "original" + suffix
        (folder / original_file).write_bytes(data)
        reading = reading or {"format": "text", "extraction_status": "complete", "blocks": [{"locator": "text line 1", "text": text}], "warnings": []}
        write_json(folder / "manifest.json", {"id": draft_id, "work_id": "work-one", "sha256": hashlib.sha256(data).hexdigest(), "original_file": original_file, "reading": reading})
        write_json(self.root / "Writing/current/records/work-one/latest.json", {"draft_id": draft_id})

    def prepare(self, blind=False):
        result = review.prepare(self.root, "work-one", poetry_blind=blind)
        return result, self.root / result["record_path"]

    def test_blind_packets_and_privacy(self):
        result, folder = self.prepare(True)
        recognition = (folder / "packets/recognition/factual-input.json").read_bytes()
        challenge = (folder / "packets/challenge/factual-input.json").read_bytes()
        self.assertEqual(recognition, challenge)
        self.assertEqual(set(json.loads(recognition)), {"language", "draft_text"})
        self.assertNotIn(b"Interpretive secret", recognition)
        self.assertNotIn(b"Never expose", recognition)
        self.assertEqual(result["processing_policy"], "local_only")
        self.assertEqual(result["independence_status"], "not_demonstrated")
        self.assertEqual(result["model_execution"], "not_performed")
        self.assertFalse(result["stale"])

    def test_free_verse_plain_text_preserves_stanzas_and_line_endings(self):
        text = "\ufeff  夜色\r\n停在窗沿\r\n\r\n\r\n\t风仍在\n  门外\n"
        # The stored extraction intentionally omits blank lines, as older
        # readers did. Review must recover form from the verified original.
        reading = {"format": "text", "extraction_status": "complete", "blocks": [{"locator": f"line[{index}]", "text": line} for index, line in enumerate(text.splitlines(), 1) if line], "warnings": []}
        for index, suffix in enumerate((".txt", ".md")):
            with self.subTest(suffix=suffix):
                self.make_draft(f"draft-form-{index}", text, suffix=suffix, reading=reading)
                result, folder = self.prepare(True)
                factual = json.loads((folder / "packets/recognition/factual-input.json").read_bytes())
                self.assertEqual(factual["draft_text"], text)
                self.assertEqual((folder / "inputs/draft.txt").read_bytes(), text.encode("utf-8"))
                self.assertTrue(result["text_fidelity"]["exact_text"])
                self.assertEqual(set(factual), {"language", "draft_text"})

    def test_partial_extraction_warning_reaches_blind_and_cross_review(self):
        reading = {"format": "text", "extraction_status": "partial", "blocks": [{"locator": "line[1]", "text": "First line"}], "warnings": ["Output limit reached; later content was not extracted."]}
        text = "First line\n\nLast stanza\n"
        self.make_draft("draft-partial", text, reading=reading)
        result, folder = self.prepare(True)
        for role in ("recognition", "challenge"):
            instructions = (folder / "packets" / role / "instructions.md").read_text(encoding="utf-8")
            self.assertIn("Stored draft extraction is partial", instructions)
            self.assertIn("Output limit reached", instructions)
            self.assertIn("complete UTF-8 original", instructions)
            self.assertNotIn("Never expose this", instructions)
            factual = json.loads((folder / "packets" / role / "factual-input.json").read_bytes())
            self.assertEqual(factual["draft_text"], text)
            self.assertEqual(set(factual), {"language", "draft_text"})
        a, b = self.root / "recognition.txt", self.root / "challenge.txt"
        a.write_text("Possible reading", encoding="utf-8")
        b.write_text("Alternative reading", encoding="utf-8")
        review.advance(self.root, result["id"], a, b)
        self.assertIn("Stored draft extraction is partial", (folder / "stage2/countercritique.md").read_text(encoding="utf-8"))

    def test_docx_projection_preserves_available_empty_paragraphs_and_warns(self):
        folder = self.root / "Writing/current/records/work-one/drafts/draft-docx"
        folder.mkdir(parents=True)
        original = folder / "original.docx"
        with zipfile.ZipFile(original, "w") as archive:
            archive.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>First line</w:t><w:br/><w:t>Second line</w:t></w:r></w:p><w:p/><w:p><w:r><w:t>Last stanza</w:t></w:r></w:p></w:body></w:document>')
            archive.writestr("word/header1.xml", '<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:r><w:t>Author context</w:t></w:r></w:p></w:hdr>')
        reading = {"format": "docx", "extraction_status": "complete", "blocks": [{"locator": "word/document.xml/body/p[1]", "text": "First line\nSecond line"}, {"locator": "word/document.xml/body/p[2]", "text": ""}, {"locator": "word/document.xml/body/p[3]", "text": "Last stanza"}, {"locator": "word/header1.xml/p[1]", "text": "Author context"}], "warnings": []}
        write_json(folder / "manifest.json", {"id": "draft-docx", "work_id": "work-one", "sha256": hashlib.sha256(original.read_bytes()).hexdigest(), "original_file": "original.docx", "reading": reading})
        write_json(self.root / "Writing/current/records/work-one/latest.json", {"draft_id": "draft-docx"})
        result, review_folder = self.prepare(True)
        factual = json.loads((review_folder / "packets/recognition/factual-input.json").read_bytes())
        self.assertEqual(factual["draft_text"], "First line\nSecond line\n\nLast stanza")
        self.assertNotIn("Author context", factual["draft_text"])
        self.assertFalse(result["text_fidelity"]["exact_text"])
        instructions = (review_folder / "packets/recognition/instructions.md").read_text(encoding="utf-8")
        self.assertIn("not exact visual form", instructions)
        self.assertIn("headers, footers and separate notes are excluded", instructions)

    def test_advance_is_append_only_and_honest(self):
        result, folder = self.prepare()
        initial = (folder / "manifest.json").read_bytes()
        a, b = self.root / "recognition.txt", self.root / "challenge.txt"
        a.write_text("Defensible reading", encoding="utf-8")
        b.write_text("Substantive objection", encoding="utf-8")
        advanced = review.advance(self.root, result["id"], a, b)
        self.assertEqual(advanced["phase"], "cross_review_packets_ready")
        self.assertEqual(initial, (folder / "manifest.json").read_bytes())
        self.assertEqual(advanced["independence_status"], "not_demonstrated")
        self.assertEqual((folder / "stage2/outputs/challenge.txt").read_text(), "Substantive objection")
        with self.assertRaises(FileExistsError):
            review.advance(self.root, result["id"], a, b)

    def test_empty_output_refused_without_partial_stage(self):
        result, folder = self.prepare()
        a, b = self.root / "a.txt", self.root / "b.txt"
        a.write_text("  ")
        b.write_text("A finding")
        with self.assertRaises(ValueError):
            review.advance(self.root, result["id"], a, b)
        self.assertFalse((folder / "stage2").exists())

    def test_new_draft_marks_review_stale_preserving_inputs(self):
        result, folder = self.prepare()
        before = (folder / "inputs/draft.txt").read_bytes()
        self.make_draft("draft-two", "Changed poem")
        current = review.status(self.root, result["id"])
        self.assertTrue(current["stale"])
        self.assertEqual(before, (folder / "inputs/draft.txt").read_bytes())

    def test_changed_original_is_stale(self):
        result, _ = self.prepare()
        (self.root / "Writing/current/records/work-one/drafts/draft-one/original.txt").write_text("Altered")
        self.assertTrue(review.status(self.root, result["id"])["stale"])

    def test_frozen_artifact_tampering_refused(self):
        result, folder = self.prepare()
        (folder / "inputs/draft.txt").write_text("Changed")
        with self.assertRaises(ValueError):
            review.status(self.root, result["id"])

    def test_invalid_identifiers(self):
        for value in ("../other", "CON", "作品", "work/one", "work:one"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                review.prepare(self.root, value)

    def test_traversing_original_refused(self):
        path = self.root / "Writing/current/records/work-one/drafts/draft-one/manifest.json"
        manifest = json.loads(path.read_text())
        manifest["original_file"] = "../../outside.txt"
        write_json(path, manifest)
        with self.assertRaises(ValueError):
            review.prepare(self.root, "work-one")

    def test_foreign_component_symlink_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        link = self.root / "Review"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation is unavailable")
        with self.assertRaises(ValueError):
            review.prepare(self.root, "work-one")
        link.unlink()
        try:
            link.symlink_to(self.root.parent, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation is unavailable")
        with self.assertRaises(ValueError):
            review.prepare(self.root, "work-one")


if __name__ == "__main__":
    unittest.main(verbosity=2)
