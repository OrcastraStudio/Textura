"""Meaningful fidelity and failure-boundary tests; fixtures stay in a temporary directory."""
import importlib.util
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import readers

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="textura-reading-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, data):
        path = self.root / name
        path.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)
        return path

    def docx(self, body, extras=None):
        path = self.root / "稿件.docx"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("word/document.xml", f'<w:document xmlns:w="{W}"><w:body>{body}</w:body></w:document>')
            for name, content in (extras or {}).items():
                archive.writestr(name, content)
        return path

    def test_utf8_lines_preserve_empty_line_offsets_and_no_writes(self):
        path = self.write("诗歌.md", "\ufeff中文\n\nfrançais Deutsch\n")
        before = {p: p.read_bytes() for p in self.root.iterdir()}
        result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "complete")
        self.assertEqual(result["blocks"], [{"locator": "line[1]", "text": "中文"}, {"locator": "line[3]", "text": "français Deutsch"}])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.iterdir()})
        json.dumps(result)

    def test_invalid_utf8_is_not_silently_replaced(self):
        result = readers.extract(self.write("bad.txt", b"hello\xffworld"))
        self.assertEqual(result["extraction_status"], "unsupported")
        self.assertFalse(result["blocks"])

    def test_unknown_format_remains_registerable(self):
        result = readers.extract(self.write("recording.mp3", b"not decoded"))
        self.assertEqual(result["extraction_status"], "unsupported")
        self.assertIn("Sources", " ".join(result["warnings"]))

    def test_output_truncation_is_transparent(self):
        path = self.write("long.txt", "abcdef\nsecond")
        with patch.object(readers, "MAX_OUTPUT_CHARS", 4):
            result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "partial")
        self.assertEqual(result["blocks"][0]["text"], "abcd")
        self.assertIn("truncated", " ".join(result["warnings"]))

    def test_file_limit_is_checked_before_read(self):
        path = self.write("large.txt", "abcdef")
        with patch.object(readers, "MAX_FILE_BYTES", 3):
            result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "unsupported")
        self.assertFalse(result["blocks"])

    def test_html_source_locators_and_script_suppression(self):
        source = '<html>\n<script>malicious();</script><style>secret</style>\n<p>Known &amp; visible</p><img src="https://invalid.local/image.png"></html>'
        result = readers.extract(self.write("snapshot.html", source))
        text = " ".join(b["text"] for b in result["blocks"])
        self.assertEqual(text, "Known & visible")
        self.assertTrue(result["blocks"][0]["locator"].startswith("html-source:line[3]"))
        self.assertEqual(result["extraction_status"], "partial")

    def test_csv_multiline_records_and_formulas_are_literal(self):
        result = readers.extract(self.write("data.csv", 'name,note\n"作者","line one\nline two"\nformula,=1+1\n'))
        blocks = {b["locator"]: b["text"] for b in result["blocks"]}
        self.assertEqual(blocks["record[2]/column[2]"], "line one\nline two")
        self.assertEqual(blocks["record[3]/column[2]"], "=1+1")

    def test_docx_paragraph_table_and_footnote_locators(self):
        note = f'<w:footnotes xmlns:w="{W}"><w:footnote w:id="2"><w:p><w:r><w:t>出处</w:t></w:r></w:p></w:footnote></w:footnotes>'
        body = '<w:p><w:r><w:t>正文</w:t><w:footnoteReference w:id="2"/></w:r></w:p><w:tbl><w:tr><w:tc><w:p><w:r><w:t>表格</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
        result = readers.extract(self.docx(body, {"word/footnotes.xml": note}))
        blocks = {b["locator"]: b["text"] for b in result["blocks"]}
        self.assertEqual(blocks["word/document.xml/body/p[1]"], "正文[footnote:2]")
        self.assertEqual(blocks["word/document.xml/body/tbl[1]/tr[1]/tc[1]/p[1]"], "表格")
        self.assertEqual(blocks["word/footnotes.xml/footnote[id=2]/p[1]"], "出处")
        self.assertFalse(any("page[" in key for key in blocks))

    def test_docx_revisions_comments_and_textboxes_are_partial(self):
        body = '<w:p><w:r><w:t>Kept</w:t></w:r><w:del><w:r><w:delText>Deleted</w:delText></w:r></w:del><w:ins><w:r><w:t>Inserted</w:t></w:r></w:ins><w:r><w:drawing><w:txbxContent><w:p><w:r><w:t>Hidden box</w:t></w:r></w:p></w:txbxContent></w:drawing></w:r></w:p>'
        result = readers.extract(self.docx(body, {"word/comments.xml": f'<w:comments xmlns:w="{W}"/>'}))
        self.assertEqual(result["extraction_status"], "partial")
        self.assertEqual(result["blocks"][0]["text"], "KeptInserted")
        warnings = " ".join(result["warnings"])
        self.assertIn("comments", warnings)
        self.assertIn("text boxes", warnings)

    def test_docx_dtd_is_rejected_before_entity_expansion(self):
        path = self.root / "entity.docx"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("word/document.xml", '<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "expanded">]><x>&a;</x>'.encode("utf-16"))
        result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "unsupported")
        self.assertIn("DTD/entity", " ".join(result["warnings"]))

    def test_docx_list_labels_and_link_destinations_are_not_invented(self):
        body = '<w:p><w:pPr><w:numPr><w:numId w:val="3"/></w:numPr></w:pPr><w:hyperlink><w:r><w:t>Source title</w:t></w:r></w:hyperlink></w:p>'
        result = readers.extract(self.docx(body))
        self.assertEqual(result["extraction_status"], "partial")
        self.assertEqual(result["blocks"][0]["text"], "Source title")
        self.assertIn("list numbering", " ".join(result["warnings"]))
        self.assertIn("target URLs", " ".join(result["warnings"]))

    def test_compression_bomb_is_refused(self):
        path = self.root / "bomb.docx"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("word/document.xml", b"a" * (2 * 1024 * 1024))
        result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "unsupported")
        self.assertIn("compression ratio", " ".join(result["warnings"]))

    def test_encrypted_zip_flag_is_refused(self):
        path = self.docx('<w:p><w:r><w:t>text</w:t></w:r></w:p>')
        data = bytearray(path.read_bytes())
        central = data.index(b"PK\x01\x02")
        flags = struct.unpack_from("<H", data, central + 8)[0]
        struct.pack_into("<H", data, central + 8, flags | 1)
        path.write_bytes(data)
        result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "unsupported")
        self.assertIn("Encrypted", " ".join(result["warnings"]))

    def test_missing_optional_packages_return_clear_status(self):
        with patch.object(readers, "_available", return_value=False):
            for name in ("file.xlsx", "file.pdf"):
                result = readers.extract(self.write(name, b"original retained"))
                self.assertEqual(result["extraction_status"], "unsupported")
                self.assertIn("optional", " ".join(result["warnings"]))

    @unittest.skipUnless(importlib.util.find_spec("openpyxl"), "optional openpyxl unavailable")
    def test_xlsx_sheet_cell_formula_and_stale_dimension(self):
        from openpyxl import Workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "作者's"
        sheet["A1"] = "中文"
        sheet["C3"] = "=1+1"
        path = self.root / "table.xlsx"
        workbook.save(path)
        with zipfile.ZipFile(path) as archive:
            members = {i.filename: archive.read(i) for i in archive.infolist()}
        members["xl/worksheets/sheet1.xml"] = members["xl/worksheets/sheet1.xml"].replace(b'ref="A1:C3"', b'ref="A1:A1"')
        with zipfile.ZipFile(path, "w") as archive:
            for name, value in members.items():
                archive.writestr(name, value)
        result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "complete", result)
        blocks = {b["locator"]: b["text"] for b in result["blocks"]}
        self.assertEqual(blocks["'作者''s'!A1"], "中文")
        self.assertEqual(blocks["'作者''s'!C3"], "=1+1")

    @unittest.skipUnless(importlib.util.find_spec("openpyxl"), "optional openpyxl unavailable")
    def test_xlsx_limits_are_partial(self):
        from openpyxl import Workbook
        workbook = Workbook()
        workbook.active["A1"] = "start"
        workbook.active["Z9"] = "outside limit"
        path = self.root / "wide.xlsx"
        workbook.save(path)
        with patch.object(readers, "MAX_SHEET_COLUMNS", 2):
            result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "partial")
        self.assertEqual(len(result["blocks"]), 1)

    @unittest.skipUnless(importlib.util.find_spec("pypdf"), "optional pypdf unavailable")
    def test_pdf_physical_page_and_blank_page_warning(self):
        from pypdf import PdfWriter
        from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
        writer = PdfWriter()
        page = writer.add_blank_page(width=200, height=200)
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
        page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
        content = DecodedStreamObject()
        content.set_data(b"BT /F1 12 Tf 20 100 Td (Actual text) Tj ET")
        page[NameObject("/Contents")] = content
        writer.add_blank_page(width=200, height=200)
        path = self.root / "pages.pdf"
        with path.open("wb") as out:
            writer.write(out)
        result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "partial")
        self.assertEqual(result["blocks"][0]["locator"], "physical-page[1]")
        self.assertIn("Actual text", result["blocks"][0]["text"])
        self.assertIn("No extractable text", " ".join(result["warnings"]))

    @unittest.skipUnless(importlib.util.find_spec("pypdf"), "optional pypdf unavailable")
    def test_encrypted_pdf_is_not_claimed_read(self):
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        writer.encrypt("secret")
        path = self.root / "encrypted.pdf"
        with path.open("wb") as out:
            writer.write(out)
        result = readers.extract(path)
        self.assertEqual(result["extraction_status"], "unsupported")
        self.assertFalse(result["blocks"])


if __name__ == "__main__":
    unittest.main()
