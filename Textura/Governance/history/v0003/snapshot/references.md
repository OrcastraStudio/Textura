# Verified conceptual references

Checked against official project documentation on 2026-09-26. These inform boundaries and organization; no source code was copied, no dependency was installed merely for this comparison, and no upstream endorsement or certification is claimed.

| Project and official reference | Observed design | Textura application |
|---|---|---|
| [Pandoc: Using the pandoc API](https://www.pandoc.org/using-the-pandoc-api.html) | Readers convert input to a document representation; writers produce outputs. | Separate source reading from manuscript/publication output rather than couple every input to every output. Textura does not claim to implement the Pandoc AST. |
| [Zotero: Adding Files to your Library](https://www.zotero.org/support/attaching_files) | Bibliographic metadata and attached files are distinct; web snapshots preserve a captured page state. | Keep source identity, actual captured files and completeness separate. A metadata-only source is not a saved full text. |
| [Quarto: Authoring](https://quarto.org/docs/get-started/authoring/vscode) | Authoring supports structured documents, bibliographies, citation locators and multiple output formats. | Retain manuscript/citation information independently of platform-specific excerpts and future rendering adapters. |

These references do not validate Textura's semantic assessments. An official project's supported formats or integrations are not automatically Textura capabilities. Check the local Runner and component documentation for implemented behavior.
