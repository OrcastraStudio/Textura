# Textura command reference

From the extracted Textura directory with PowerShell:

```powershell
& '.\Runner\current\textura.ps1' status
& '.\Runner\current\textura.ps1' doctor
& '.\Runner\current\textura.ps1' validate
```

Alternatively use Python 3.11+ with `Runner/current/textura.py`. Set `TEXTURA_PYTHON` to a Python executable if discovery fails. Optional PDF/XLSX readers are reported by `doctor`; absent readers report unsupported extraction instead of installing anything. All examples below show the arguments after the launcher. IDs returned by preceding operations must replace example IDs. These examples are instructions, not preloaded works or research results.

| Arguments | Effect and owner |
|---|---|
| `status` | Report Configuration registry and operational boundaries |
| `doctor` | Report local runtime/readers and existence of the configured library entry; no account/network tests |
| `validate` | Check component ownership, release hashes and selected record relationships; no semantic verification |
| `topic --title "A question"` | Create a Topics topic |
| `object --title "An object" --topic topic-ID` | Create a research object |
| `series --title "A series" --topic topic-ID` | Create a series record |
| `work --title "An essay" --topic topic-ID --language en --genre essay` | Create an independent work |
| `source --title "A source" --file "../materials/source.pdf" --url "https://example.org/source" --scope partial` | Preserve a local source snapshot; capture scope describes the acquired artifact, not source reliability |
| `source --title "A lead" --url "https://example.org/source"` | Register a link-only lead; no download or full-text claim |
| `read source-ID` | Create Reading text/locator records for an acquired source |
| `draft work-ID --file "../materials/draft.docx"` | Import an immutable draft snapshot and advance its latest pointer |
| `claim --work work-ID --statement "A claim" --kind fact --priority high` | Record a claim, bound to the latest draft if one exists |
| `assess claim-ID --verdict inconclusive --rationale "Full text unavailable"` | Record an explicit unresolved assessment |
| `assess claim-ID --verdict supported --rationale "Reasoned analysis" --evidence-file "../materials/refs.json"` | Check exact references, then record the assessor's judgment; does not prove the judgment |
| `review prepare work-ID` | Freeze manuscript/evidence and create separate recognition/challenge packets |
| `review advance review-ID --recognition-file "../reports/recognition.md" --challenge-file "../reports/challenge.md"` | Preserve completed initial reports and prepare countercritique/synthesis instructions |
| `review status review-ID` | Check review artifacts, stage and manuscript staleness |
| `decision --kind author_decision --text "Keep the ending" --work work-ID --basis "Author instruction, dated ..."` | Record a key confirmed decision with its basis |
| `handoff --work work-ID` | Save a portable State handoff referencing the work's records |
| `snapshot Style --reason "Before updating genre criteria"` | Archive this component's definitions in its own history |
| `seal Style` | Record active hashes after an initial build or properly archived and validated maintenance |
| `bm search "query"` | Use the configured Bibliotheca Magna search interface, read-only |
| `bm show BM-R-ID` | Read the selected library record |
| `bm cite BM-R-ID --version v001 --file F01 --extraction E01 --line 2` | Obtain a library locator using its documented interface |

Use `--help` after the launcher or a command for all arguments. Global `--root PATH` precedes the command and changes the data root only. Organization/source commands use Configuration's default_processing_policy (local_only in this candidate) when --policy is omitted. They accept --policy local_only and --policy cloud_allowed; work policy inherits a restrictive parent topic. `cloud_allowed` does not independently authorize transmission or external publication.

Evidence files contain a JSON array, for example:

```json
[
  {
    "reading_id": "reading-ID",
    "locator": "COPY_THE_EXACT_LOCATOR_FROM_THE_READING_RECORD",
    "excerpt": "Copy an exact excerpt from that block.",
    "original_inspected": false,
    "attribution_chain": ["The acquired article attributes this statement to an original not yet inspected."],
    "source_version_note": "Explain edition or translation uncertainty when relevant."
  }
]
```

Always replace every placeholder. A match verifies reference consistency, not authorship, publication authenticity, interpretive validity or causal reasoning. Decisive verdicts need evidence. Use an explicit new assessment with `--supersedes assessment-ID` to revise a judgment; claims similarly accept `--supersedes claim-ID`. Preserve unresolved or dissenting assessments.

For `free_verse`, `free-verse`, `poem` or `poetry`, the first review is automatically blind. `--blind` can request this for another genre. There is no automatic unblinding command: discuss author intent after the initial blind review and record that later discussion explicitly. Prepared files do not establish reviewer independence; use isolated contexts where the host supports them, otherwise disclose sequential role review. Final synthesis and author acceptance are agent-recorded work under Review/State, not inferred by the launcher.

`seal` is maintenance bookkeeping, not authorization to discard history. Read [storage-and-versioning.md](../../Governance/current/storage-and-versioning.md) before changes. A new component requires its own current/history directories, README, component metadata and interface, plus a Configuration registry update; archive Configuration before editing its released registry. Do not create root files or global backups. There is no automatic component scaffolder in this release.

## Optional external library

Bibliotheca is disabled and unconfigured in this candidate. Before using bm, configure bibliotheca.enabled=true and an absolute bibliotheca.root after preserving Configuration history, then reseal Configuration. Node.js is needed only for that optional bridge; use TEXTURA_NODE or PATH. The core CLI and tests require no Codex installation or model account. Library availability does not imply interface compatibility or permission to transfer material.

Example materials/ and reports/ directories are outside the component-only Textura installation root. Supply your actual input paths; do not create generic data directories at that root.
