# Fiction operating protocol

## 1. Establish the bounded task

Identify the work, branch or experiment, intended form, language, available Writing draft/version, requested assistance, and applicable author decisions. If a work does not yet have a manuscript, say so and use material references without inventing a draft identity.

A brief direction is enough to begin. Offer a useful next layer of planning and retain open questions; do not force a full outline, fixed ending or exhaustive setting dossier before exploration. Scale the record to the story and current task.

Use only task-supported working goals and keep preliminary aims provisional. Do not assume completed-novel experience, a universal aesthetic standard or a preferred organizing principle for every user.

## 2. Map material and compare possible centers

Retain where each material item came from and what is actually available. Separate author material, manuscript passages, external research, existing settings and AI suggestions. Missing source text or context is a gap, not permission to reconstruct it as an original.

Materials may be rearranged, combined, transformed or extended as proposals. Label additions and transformations, preserve their antecedents, describe their likely effect, and record their author-decision reference before treating them as an adopted plan. Adoption into a plan is distinct from adoption into the manuscript.

Offer single-center and multi-center arrangements when comparison is useful. For each alternative explain its organizing focus, character/relationship changes, thematic or emotional connections, likely gains, tradeoffs, requirements and uncertainties. Neither structural pattern is intrinsically better. Do not silently select one or invent a universal scoring system.

## 3. Keep story records and branches distinct

Each record identifies its work, branch, relevant scene or span, draft/setting version, record state, and basis. Cross-reference stable record identities and actual readable locators; never infer a Word page number from a paragraph index.

Within a branch distinguish:

- **Event/setting layer:** what the work's accepted setting or supplied text establishes, proposes or leaves open about the fictional world.
- **Narrative assertion layer:** what narration claims, with its speaker or narrative position and textual basis.
- **Character cognition layer:** what a particular character knows, believes, misunderstands, suspects, intends to conceal or is alleged to conceal at a particular point.
- **Reader-information layer:** what the text has disclosed to a reader by a stated scene or reading boundary; distinguish explicit disclosure from possible inference.

A statement in one layer does not automatically become a fact in another. A narrator may be unreliable; a character may lie or be mistaken. Dialogue, rumor and metaphor need contextual reading. Do not label concealment, intention or world truth as established solely because an AI can invent a coherent explanation.

Keep branch-specific changes separate. Shared ancestors or reused scenes do not authorize propagation to another branch. Explicitly record adoption, divergence or a proposed merge, including its affected versions.

Separate **not yet decided** from **deliberately ambiguous**. Deliberate ambiguity needs an author decision or an identified provisional interpretation, with its intended scope. Do not resolve it merely to make a ledger complete, and do not excuse an unexplained contradiction by inventing an intention to be ambiguous.

## 4. Check knowledge and continuity against scenes

For a relevant character and point in the story, identify the information, its source, when it could have been acquired, what the character believes, and any evidence of misunderstanding or concealment. Anchor findings to scene/version references and retain uncertainty about off-page events.

Use timelines, cause-and-effect links, relationships and recurring motifs only as far as supported or explicitly proposed. Separate observed textual effects from planning intentions. If an early passage is unavailable, do not claim a later echo, contradiction or successful setup has been checked against it.

For a manuscript/setting conflict preserve both statements and their exact versions side by side. State the conflict, plausible interpretations, affected characters/scenes/works, urgency and uncertainty. Group clarification requests by impact, allowing continued work on independent material. Do not silently overwrite the manuscript, formal setting or author's preference.

Work-specific divergence from a shared setting is recorded locally with its explicit decision and scope. It does not change the shared setting's formal version or make every other work inconsistent.

## 5. Respect shared-setting authority

Author-selected formal shared settings may be maintained by a future explicitly configured provider. Textura retains working material, local settings, selected formal-version references, experiments and modification proposals. The separation applies only to items actually selected for sharing; do not transfer every character or location.

Follow [the shared-setting interface design](../../LibraryBridge/current/shared-setting-interface.md). The BM module and operational interface are not implemented by this component. Do not guess endpoints, commands, version identifiers or write permissions.

For each shared setting record the exact obtainable version and the work's explicit adoption decision. Unchanged acquired provider snapshots and excerpts, with provenance and capture limitations, belong to LibraryBridge/current/records/. Fiction refers to those records; any content it derives for modification must be explicitly labeled as a modification draft with its base-version reference, never a second acquired snapshot or formal version. If the module or requested version is unavailable, disclose that status and work only from identified available material. Never silently replace a pinned version with the newest one.

A future formal update produces a proposed difference and impact assessment. No work adopts it automatically. Library transfer and formalization follow actual author scope and the library's implemented procedure; a prepared proposal alone triggers neither a write nor synchronization.

## 6. Apply adopted changes through their owners

Use the State reference establishing an adopted change. Preserve the before/after references and distinguish an accepted direction, a planned revision, and prose actually incorporated into a new Writing version.

Prepare an impact list including, where relevant, scene order, events, causal dependencies, character knowledge, relationships, clues and later payoffs, thematic or imagistic echoes, voice assumptions and adopted shared-setting references. Explain each link's basis and mark speculative impacts as such.

Propose manageable review batches by importance, dependency or affected span. Complete and record only the checks actually performed; retain untouched, pending, blocked and unresolved items. Later batches must not inherit an unsupported "all clear" from an earlier local check.

Send candidate prose to Writing, voice questions to Style, real-world factual questions to Evidence, and review requests to Review. Recheck against the actual resulting versions. Completed local revision does not establish whole-work consistency.

## 7. Supply honest review context

Select the relevant manuscript and Fiction/Style versions and state whether the reviewer is reading a bounded excerpt, the full available manuscript, a plan, or mixed material. Record extraction gaps and unavailable passages. Summaries aid navigation; they do not establish that omitted scenes were read.

Declare the reviewer's knowledge boundary. A first reader receives only the manuscript prefix reached so far, neutral reading instructions and the selected reading perspective. Do not provide author intentions, planning notes, setting records or earlier reader/editor interpretations, including those about already-read scenes. Keep coordinator metadata, revealing filenames and links out of reader-visible material. An editor-oriented pass may explicitly receive selected full-context records. If excluded information was already visible, disclose that an unspoiled first reading was not achieved.

Recognition, questioning and questioning-the-questioning continue under Review's actual execution conditions. They judge narrative effect, coherence and meaningful alternatives without demanding that fiction resolve every tension or express a single author thesis.

The existing Review CLI does not automatically freeze Fiction/Style context. Fiction retains its source records and coordinator-side preparation checklist. The runtime agent prepares formal frozen supplemental inputs and the actual context manifest under Review/current/records/fiction-contexts/, using [Review's context template](../../Review/current/fiction-review-context.template.md). Record the link to the Review run if one exists, otherwise identify a protocol-only review; document actual input versions, coverage, integrity checks and what each reviewer received. Fiction refers to that Review-owned context rather than maintaining a second manifest. Do not claim native CLI validation, supplemental-currency checks, isolation, completion or input integrity that was not actually performed. A changed draft or relevant setting requires a new explicitly scoped review; historical findings remain attached to their original inputs.

## 8. Preserve decisions and limits

Fiction owns its specialized maps and findings; State owns the author's decisions and cross-session handoff. Record accepted, rejected, superseded and unresolved alternatives without rewriting history. Keep significant reasons and dissent.

Privacy restrictions follow source materials and derivatives. Reference links are not authorization to expose restricted or spoiler-sensitive material to another role. No automatic publishing, library transfer, backup or monitoring is introduced by this protocol.
