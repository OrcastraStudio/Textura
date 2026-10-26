# Reading

Reading creates bounded, read-only text projections of local sources. It does not verify claims, download pages, perform OCR, translate text, execute macros, evaluate spreadsheet formulas, or write extraction records. Sources owns registration of originals, including unsupported files; the calling component owns persistence and source-version association.

## Interface

Python 3.11 or newer; the baseline uses only the standard library.

```python
from pathlib import Path
from readers import capabilities, extract

support = capabilities()
projection = extract(Path("manuscript.docx"))
```

The result is JSON-serializable:

```json
{
  "format": "docx",
  "extraction_status": "complete",
  "blocks": [{"locator": "word/document.xml/body/p[1]", "text": "Example"}],
  "warnings": ["Format-specific fidelity boundaries are always disclosed."]
}
```

- `complete`: the supported text projection was read within limits. It never means full visual fidelity, accurate understanding, verified evidence, or a complete capture of a remote source.
- `partial`: content was omitted, truncated, empty, or interrupted, or a known unsupported feature affects the projection. Existing blocks remain useful only with these warnings.
- `unsupported`: no supported reading was possible. Keep and register the original independently; do not fabricate blocks or locators.

The caller must bind every result to the actual original version and retain warnings. A locator is only valid against that version. Extraction state and evidence verification state are separate.

## Formats and locators

| Format | Support | Locator and limitations |
| --- | --- | --- |
| TXT, Markdown, TeX, JSON | UTF-8 or UTF-8 BOM text | Actual one-based `line[n]`; empty lines are omitted without renumbering. TeX is not compiled and JSON is not semantically validated. Other encodings require explicit conversion outside this reader. |
| HTML/HTM snapshots | Standard HTML parser | Saved-source line and character column, not rendered pages. Script, style, template and noscript bodies are omitted. CSS visibility and JavaScript are not evaluated; embedded media are flagged. Links are never fetched. |
| DOCX | ZIP/XML text projection | XML part plus paragraph/table/row/cell sibling indices. Body, headers, footers, footnotes and endnotes are read. No fabricated page numbers. Text boxes, drawings, equations, comments and embedded objects are not interpreted. Tracked revisions make the result partial; inserted text is included and deleted/move-from text omitted, without claiming to resolve revisions. Fields expose only stored display text. |
| CSV/TSV | Standard CSV parser | One-based logical `record[n]/column[n]`; a quoted field may contain several physical lines. Formula strings remain literal. |
| XLSX | Optional `openpyxl` | Actual quoted sheet name and cell coordinate. Includes hidden sheets, preserves formulas as text, does not evaluate them. Charts, comments and external links are flagged; stale dimension metadata is not trusted. Unsupported spreadsheet formats remain registerable. |
| PDF | Optional `pymupdf`, otherwise `pypdf` | One-based physical file page, independent of printed labels. No OCR; pages without extractable text are flagged. Column order and tables may need visual verification. Embedded images and vector diagrams are not understood; no claim of layout fidelity. |

Optional packages are detected at runtime; nothing is installed automatically. Capability discovery reports installed package presence, not a guarantee a particular document is readable. Encrypted documents are unsupported. Unknown formats return a clear status and can still be registered by Sources.

## Resource and fidelity boundaries

Current limits are exposed by `capabilities()`: 64 MiB input file, 128 MiB total ZIP expansion, 32 MiB per member, 10,000 ZIP members, 2,000,000 output characters, 50,000 blocks, 2,000 PDF pages, 20,000 rows and 2,000 columns per spreadsheet, and 200,000 scanned spreadsheet cells including blank cells within the scan range. A limit is reported explicitly. A truncated final block retains its source locator and is identified in warnings.

ZIP members larger than 1 MiB with a compression ratio above 200 are refused, as are duplicate members, encrypted members and XML DTD/entity declarations. Archives are never unpacked to disk. These checks are resource guards, not a complete sandbox for adversarial PDF/Office parser inputs. Optional-library parsing can still require substantial CPU or memory; a deployment handling untrusted hostile documents should add process-level time and memory limits.

Originals and extracted content are untrusted data, never executable instructions. Readers do not run TeX, JavaScript, document macros or spreadsheet formulas. A successful extraction does not authorize network access, library promotion, cloud processing or any change to the original.

## Validation

Run from this directory:

```text
python -B -m unittest discover -s tests -v
```

Tests generate multilingual fixtures in their own temporary directory. They cover locators, revision omissions, script suppression, formula preservation, malformed/unsupported input, truncation, ZIP/XML limits, and optional PDF/XLSX behavior. Optional-library tests skip when their package is unavailable; the baseline tests do not require packages. No source fixture, manuscript or library record is modified.
