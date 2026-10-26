# Third-party references and optional dependencies

No third-party library binaries are bundled. Python, Git, the AI host and any optional readers are separately obtained software with their own terms.

The core workflow uses Python's standard library. Reading optionally detects openpyxl for XLSX and PyMuPDF or pypdf for PDF. Node.js is needed only for a deliberately configured Bibliotheca Magna adapter; the external library is not bundled.

[Conceptual references](Textura/Governance/current/references.md) informed architecture; they do not imply copied upstream implementation or endorsement. This file is an inventory notice, not a substitute for required license texts if a future distribution actually bundles dependencies.

Dependency versions, notices and license compatibility must be reviewed against the actual final packaging choice. Textura's own grant is the [MIT License](LICENSE); it does not replace third-party terms.
