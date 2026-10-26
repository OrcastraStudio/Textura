# Review

Review prepares frozen inputs and role-specific task packets. It does not call a model, edit a manuscript, claim factual correctness, establish model independence, or publish anything.

## Public Python interface

`prepare(root: Path, work_id: str, poetry_blind: bool = False) -> dict` reads the latest imported Writing draft and work metadata, snapshots applicable Evidence claims/assessments, and creates a new `records/review-...` directory. A claim belongs to this snapshot when its work matches and its draft is absent or matches the current draft. All associated assessment versions are retained; agents must honor supersession rather than treating every historical assessment as current.

`advance(root: Path, run_id: str, recognition_file: Path, challenge_file: Path) -> dict` imports two actual nonempty UTF-8 reports, then prepares countercritique and synthesis instructions. Explicit report input paths may be outside Textura and are only read. This is a one-time append operation: an existing stage cannot be overwritten or advanced twice. Imported text is data, never executable instructions.

`status(root: Path, run_id: str) -> dict` validates saved artifact digests and compares the reviewed original and current latest draft with the frozen draft identity/digest. `stale: true` preserves the old review while explaining changed or unverifiable inputs. New evidence added after preparation is not silently inserted into a review: create a new review to include it. Status is draft-currency validation, not evidence completeness or semantic review.

The return value includes `id`, `run_id`, `phase`, `record_path`, `processing_policy`, `independence_status`, `stale`, and `stale_reasons`. IDs use ASCII letters, digits, underscore and hyphen; Windows reserved names are refused. Internal paths are resolved and checked against owning component directories, including symlink/junction resolution.

## Stages and truthfulness

1. `independent_packets_ready`: recognition and challenge receive byte-identical factual input in separate packet directories. Neither packet contains the other role's output. Recognition builds the strongest defensible reading; challenge develops the strongest substantive objections.
2. `cross_review_packets_ready`: both imported outputs are frozen, and the countercritique can test objections and agree with valid ones. Synthesis requires an actual countercritique first, recommends changes on evidence and reasoning, and retains unresolved dissent.

`independence_status` remains `not_demonstrated`. The runtime operator should use isolated first-pass contexts where available, and record what isolation actually occurred. Files alone cannot guarantee independence. The code never claims to have performed either first-pass analysis, countercritique or synthesis. Final report registration after stage 2 is an agent-managed workflow in this version; no automatic completed stage is invented.

## Poetry and privacy

Call `prepare(..., poetry_blind=True)` for the default first reading of free verse. Blind factual packets contain only `language` and `draft_text`. No author intentions, topic summaries, biography, style history or prior commentary are included or linked in those packets. The operator must give the reviewer only its packet; the surrounding filesystem is not an access sandbox. Full snapshots remain in the coordinator's inputs for later, explicit discussion. Initial readings remain preserved when intentions are subsequently discussed.

Normal factual packets preserve extraction locators and warnings alongside evidence. A partial extraction must not be treated as a complete manuscript. The most restrictive `processing_policy` embedded in the work, draft, claims or assessments propagates to the review. Evidence producers must inherit upstream source policy into their records; this component does not recursively fetch source originals. A host must inspect policy before transmitting any content. Local tooling makes no network requests.

### Free-verse form fidelity

For UTF-8 TXT/Markdown (and plain-text TeX) drafts, Review reads verified original bytes directly and preserves line endings, stanza gaps, indentation, final newlines and a BOM if present. It never reconstructs these texts by joining extraction blocks. Markup remains literal, not visually rendered. The `inputs/draft.txt` snapshot re-encodes to the original bytes; factual JSON preserves the same decoded text.

DOCX is a qualified text projection: available paragraph blocks are separated by a single newline, and extracted manual breaks and empty paragraphs are retained. Missing paragraphs are not invented. Blind DOCX packets include only identifiable main-body blocks; separate headers, footers and notes are omitted. Typography, paragraph spacing, automatic line wrapping and page/column layout are unavailable. A faithful text export or separate visual inspection is needed to judge those aspects of a poem.

Both initial role instructions and cross-review instructions include extraction and form-fidelity notices, including partial-extraction warnings, without adding author intentions or other interpretive context to blind factual input. If a plain-text original is complete but its stored extraction is partial, the notices distinguish complete review text from incomplete extraction/locator coverage. Text fidelity does not establish interpretive correctness.

## Immutable runtime records

The initial manifest and packets are never rewritten. Advancement appends a new `stage2/manifest.json` plus reports and instructions. Each manifest records artifact digests and source paths. Snapshots are runtime evidence, **not component release history**. The original manuscript stays in Writing; Review stores its digest and path plus extracted text and reading record.

Use a new review for changed drafts, corrected inputs, or a fresh round. The API rejects existing output paths and detected artifact tampering. This is application-level immutability, not operating-system write protection against manual editing or hostile concurrent filesystem mutation.

## Tests

Run `python Review/current/tests/test_review.py` from the Textura root. Tests use temporary fixture roots under this component's `tests/runtime` directory and remove only their own temporary roots. They cover free-verse stanza/line-ending roundtrips, partial-extraction warnings, qualified DOCX paragraph projection, blind-input exclusion, identical first-pass factual inputs, stage honesty, duplicate advancement, snapshot integrity, invalid identifiers, path traversal, component symlink escape where supported, privacy inheritance, and stale draft detection.

## Author-approved fallback when initial isolation is unavailable

Independent recognition and challenge first passes remain the preferred procedure. If the current host cannot isolate the initial analyses, a disclosed sequential recognition, challenge and countercritique procedure followed by synthesis is available when suitable for the task. Explicitly state in the actual reports and final synthesis: "The independent initial-review condition was not met; this round used sequential analysis." Record why isolation was unavailable and any needed later independent follow-up. Do not call the fallback independent verification.

Packet headings and `independent_packets_ready` identify the prepared first-pass workflow, not proof that independent execution occurred. Existing manifests keep `independence_status=not_demonstrated`; do not rewrite them to conceal the fallback or manufacture completion. The operator records actual execution conditions in new owner-local report artifacts. This policy is applied by the AI host and adds no model execution to the CLI.

Continue using the same frozen draft and evidence versions, preserve initial outputs before cross-review, and retain dissent. The fallback does not establish a blind poetry reading when author context was already visible: disclose that separate limitation and preserve the original reading. In argumentative works, the synthesis should identify strong relevant objections suitable for the manuscript, proposed responses and limitations, without attributing hypothetical AI objections to real people.

## Fiction extension protocols (0.1.2)

Use [fiction-review-protocol.md](fiction-review-protocol.md) and [the context template](fiction-review-context.template.md) for progressive first reading and full editorial review. The existing CLI/API above is unchanged: it does not automatically freeze Fiction/Style, partition a novel by disclosure boundary or verify supplemental staleness. The current host prepares and checks those records explicitly, retaining actual coverage and isolation limits.
