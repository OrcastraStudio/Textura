# Fiction

Fiction is an agent-executed design and continuity component for short stories and long novels. It owns story maps, structure alternatives, work-local settings, character and event relationships, continuity findings, and shared-setting version references. It adds English operating instructions and blank templates only: no command, model call, automatic analysis, synchronization, or example work is implemented.

## Inputs and outputs

| Function | Inputs | Outputs |
| --- | --- | --- |
| Material and structure mapping | Author-provided material references; a Writing draft/version when available; author goals and open questions | A traceable material map; provisional story focus; single-center or multi-center alternatives; questions and staged planning proposals |
| World and continuity | Draft scenes; work-local setting records; explicitly selected shared-setting versions | Separate event, narration, character-knowledge and reader-information records; branch-scoped timeline and relationship findings; conflicts requiring clarification |
| Revision impact | An actual State decision; old and new setting/draft references | Affected-scene and dependency list; proposed review batches; completion, unresolved and unreviewed states |
| Review support | Selected Fiction source records; draft version; declared review scope | A preparation checklist and source references handed to Review, which owns the formal frozen context and runtime manifest |

Start from a brief direction when that is all the author has. Add detail as it becomes useful; a short story does not require a novel-sized dossier. Blank fields and genuine unknowns must remain visible. No story shape, central character, complete outline, universal taste, or fixed planning method is imposed.

## Ownership and interfaces

- **Writing** owns manuscript snapshots, trial prose, candidate wording and adoption in the manuscript. Fiction refers to them and proposes structural changes; it never keeps a competing authoritative manuscript.
- **Style** owns author/work/narrator/character voice profiles and scoped style observations. Fiction supplies story context and consumes applicable references.
- **Review** owns review rounds, formal frozen supplemental contexts and runtime manifests, role reports and synthesis. Fiction retains its source records and preparation checklist, then hands selected references to Review; it does not manufacture completed reviews.
- **State** owns author decisions and handoffs. Specialized Fiction records cite those decisions and preserve unresolved alternatives; they do not create a second decision ledger.
- **Evidence** owns assessments about the real world. Internal fictional truth, a character's belief, a narrator's statement and actual external evidence are distinct.
- **Bibliotheca Magna** is intended to own author-selected formal shared-setting versions through a future module. Fiction owns work-local settings, experiments, selected version references, proposed changes and derivatives explicitly labeled as modification drafts. Unchanged acquired provider snapshots and excerpts belong to LibraryBridge. A work continues to use its explicitly adopted version until an update is explicitly adopted.
- **LibraryBridge** will carry the documented shared-setting interface. Its present adapter does not implement that future module, automatic synchronization, or library writes. Do not invent commands or replace missing versions with whichever version is newest.

Use [the operating protocol](protocol.md), [style and fiction decisions](../../Governance/current/style-fiction-decisions.md), [shared contracts](../../Contracts/current/style-fiction-contracts.md), and [the proposed shared-setting interface](../../LibraryBridge/current/shared-setting-interface.md). Interface design does not imply an operational connection.

## Working records

Complete only the useful sections of the blank templates and save records under `current/records/` when authorized work begins:

- [Story map](story-map.template.md): material provenance, focus and structure alternatives.
- [Continuity record](continuity.template.md): event layers, knowledge, uncertainty and conflicts.
- [Change impact](change-impact.template.md): adopted change, affected dependencies and staged checks.
- [Review preparation checklist](review-context.template.md): coordinator-side source selection and handoff to Review. It does not own or certify a frozen review context.

Fiction source records and preparation checklists stay with this component and refer to their actual work, branch and versions. Formal frozen review contexts and runtime manifests belong under `Review/current/records/fiction-contexts/`, using [Review's context template](../../Review/current/fiction-review-context.template.md); Fiction records link to them. Preserve predecessor relationships and frozen records. Implementation history belongs under `history/`; initial creation has no earlier release to snapshot.

## Current review limitation

The existing Review CLI freezes its documented Writing/Evidence inputs; it does not automatically collect or freeze Fiction or Style records. A runtime agent must explicitly select the source records, preserve the formal supplemental context under `Review/current/records/fiction-contexts/`, bind it to the review run when one exists, and disclose its actual coverage and restrictions. A completed template is not evidence that a reviewer read it, that isolated contexts existed, or that a full novel was reviewed.
