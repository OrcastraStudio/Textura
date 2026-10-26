# Style and fiction protocol contracts

Status: owner-local agent record conventions in release 0.1.2. These are not new CLI record handlers or automatically validated JSON schemas. Existing [record contracts](record-contracts.md), privacy propagation and original-preservation rules apply.

## Common references and provenance

A completed record identifies its stable ASCII record ID, owner, creation time, work/profile scope where applicable, actual input versions/digests and locators, processing policy, predecessor/supersession, author basis when claimed, and coverage limitations. Unknown or unacquired values remain explicit unknowns; never invent a draft, a library version, an author decision or a completed calculation.

Text/source originals remain with Writing or Sources; selected sample catalogues and material maps refer to them. Fiction can own original planning notes, while actual prose drafts, exercises and candidate wording belong to Writing. Topics retains work/topic/series identity. State decisions link to specialized owner records rather than duplicating them.

## Record families

| Family | Owner | Required meaning |
| --- | --- | --- |
| Sample catalogue | Style | Explicit selected/proposed/withdrawn scope, selection basis, actual text owner/version/range, language/genre and known collaboration or experiment context |
| Style profile/finding | Style | Observation, author-confirmed preference, provisional goal or proposed experiment; author/work/narrator/character layer; evidence/counterexamples, effects, scope and lifecycle |
| Reference study | Style | Actual edition/translation read, method/effect analysis, uncertainties and possible adaptations; original author and translator attribution kept distinct |
| Statistics/practice analysis | Style | Scope, method actually used, comparable inputs, results or not-performed status; practice purpose and feedback; prose references into Writing |
| Material map / structural alternative | Fiction | Provenance of material, proposed function, branch identity, focus, order, additions/changes, gains/losses, open questions and actual adoption basis |
| Local setting / continuity | Fiction | Work/branch/time applicability, statement layers, provenance, uncertainty and author decision where applicable |
| Change impact / conflict | Fiction | Old/new references, author-confirmed trigger, affected passages/dependencies, explicit conflict vs plausible effect, priority, completed and unreviewed scope |
| Work's shared-setting adoption | Fiction | Provider/setting/exact version reference, work/branch scope, adoption decision and local divergence, if any |
| Acquired shared-setting reference / outgoing proposal | LibraryBridge | Provider version provenance, actual acquisition/snapshot scope, selected update basis, actual result or pending state |
| Review context / findings | Review | Reading condition, fixed allowed inputs, excluded/unread scope, actual isolation conditions, outputs and unresolved differences |
| Decision / handoff | State | Existing native distinction between author_decision, ai_proposal, observation and open_question; references to the above records |

Lifecycle (current/superseded) is independent of record kind. Analysis selection does not approve every feature. A style goal is not a finding about existing writing. More specific scopes supply context; conflicts are discussed rather than silently rewriting the general profile.

## Narrative meaning has separate axes

Do not encode all story meaning in one true/false or approved/unapproved flag. Record separately:

- Layer: story event/setting, narrator assertion, character cognition or reader information.
- Provenance: actual manuscript/location, author planning note/decision, external source or AI interpretation/proposal.
- Author adoption: proposed, selected/confirmed, rejected, pending or unknown, with basis.
- Uncertainty: not yet decided, deliberately multivalent, interpretation or unknown; deliberate ambiguity needs an author basis.
- Applicability: work, alternative/branch, timeline/story time, scene boundary and reader cutoff.
- Character stance where relevant: knows, believes, suspects, misunderstands, conceals or unknown.
- Review coverage and lifecycle: read/not read, checked/not checked, current/superseded, with actual reasons.

These are human-readable conventions, not a claim of a new state engine. Do not infer all-knowing narration, character knowledge from reader knowledge, off-page motives from a convenient explanation, or real-world truth from accepted fiction.

## Versions and invalidation

Each input change may affect dependent interpretations. Preserve old findings; create a new owner-local record with predecessor and affected scope. Re-anchor after moves/reordering. A hash shows which bytes were used, not whether their claims or interpretations are valid.

A work adopts an exact formal shared version. Availability of a later version does not change adoption. Bibliotheca's current reviewed status is a claim-assessment label, not author acceptance of fictional canon. The future interface is described in [LibraryBridge](../../LibraryBridge/current/shared-setting-interface.md).

## Review and runtime limitations

Current Review CLI freezes Writing/Evidence only; it does not automatically include these new record families. A host may preserve selected supplemental inputs under Review's owner-local protocol workflow, with a separate actual coverage/integrity statement. Existing review status does not certify supplemental currency.

First-reader context excludes future events, author-intent profiles and prior interpretation. Coordinator metadata must not leak spoilers through filenames, titles or links. Context instructions are not OS access controls; report actual limitations. All derived records inherit the most restrictive processing policy.

Configuration owns personal workflow presets. Those are not Style sample findings, author-specific mature traits or shared public defaults. No actual corpus, private author preset or fiction project record is bundled in this candidate.
