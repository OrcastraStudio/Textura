# Record contracts — 1.0

## Shared fields and ownership

JSON uses UTF-8, `schema_version: "1.0"`, ASCII `id`, `record_type`, and UTC `created_at`. A display title or original filename can contain any supported language. Unknown metadata is null or an explicit unknown state; never invent dates, authors, original-language text or locators. Relative artifact paths are resolved against the documented owning directory, never the caller's working directory.

| Object | Owner | Contract |
|---|---|---|
| topic, object, series, work | Topics | Stable ID, title, explicit relationships, language/genre for a work. Language versions are independent unless explicitly related. |
| source | Sources | URL if known, original filename, capture completeness, content digest, local/cloud policy, acquisition time. A link-only record has no full-text claim. |
| reading | Reading | Source ID and digest, extraction status, blocks with actual locators, warnings. Synthetic extraction line numbers are labeled as such. |
| draft | Writing | Work ID, immutable original, digest, extracted reading, version ID. `latest.json` selects the active imported version, not the largest ID. |
| claim | Evidence | Statement, kind, priority, work/topic relationship, draft ID if applicable. Interpretation, speculation and value judgments are distinguished from empirical assertions. |
| assessment | Evidence | Claim ID, verdict, rationale, source/reading/hash/locator/excerpt references, assessor, checked time. Supersedes by ID, never rewrites a prior assessment. |
| review | Review | Frozen draft/evidence inputs, role packets, submitted outputs, phase, independence disclosure, staleness check. Packet creation is not completion of an AI review. |
| decision / handoff | State | Author decision vs AI proposal vs observation vs pending question. Important disagreements and uncertainty survive summarization. |

## Evidence invariants

Allowed verdicts: `supported`, `contradicted`, `mixed`, `inconclusive`, `not_applicable`. Decisive verdicts need evidence references and a substantive rationale. A successful technical validator confirms referential integrity only; it cannot decide whether the quoted passage logically supports a conclusion. Attribution, quote fidelity and claim support are separate checks. AI-generated criticism is labeled as such; it is not a documented external view.

Each cited excerpt points to the actual acquired source version and extraction. A secondary-source chain explicitly names the material actually read and the original not inspected. Reposts sharing an origin are not independent corroboration. No global truth badge is assigned to a document, work, library or review.

## Changes and privacy

Append new source/draft/assessment/decision records. An original is immutable after registration. A newer reading does not silently re-anchor old citations. Changed draft hashes invalidate the currency of earlier review inputs; they do not delete those reviews. A changed claim receives a new record with a supersedes link and requires a new assessment.

`processing_policy` is `cloud_allowed` or `local_only`. Descendants inherit the more restrictive policy. Host-executed AI must inspect this field before transmitting content. Local tools do not contact a cloud service. A local-only record is not made cloud-safe by summarizing or translating it. Temporary/no-save author instructions override ordinary capture defaults; operate in a deliberately temporary session rather than registering persistent records.

## Agent-produced module records

Research, Translation, Analysis, Style, Publishing and Feedback have module-specific templates and protocols. These remain agent-executed workflows in 0.1.2, not hidden automated services. Required review of an agent-filled record: source links resolve, quoted text is real, input versions are fixed, status is honest, processing policy inherited, and the record resides under its owner. No template instructs an agent to reveal private reasoning; save concise findings, reasons, evidence and author-facing decisions only.

## Style and fiction protocol extension (0.1.2)

Read [style-fiction-contracts.md](style-fiction-contracts.md) for selected samples, layered voices, narrative states, structural alternatives, exact shared-setting adoption and supplemental reviews. These are agent record conventions, not new native CLI categories. Existing validators do not automatically validate their semantic fields or supplemental review currency.
