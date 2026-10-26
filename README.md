# Textura

An author-led multilingual writing toolkit with AI-guided workflows, local version history, and traceable evidence for essays, poetry, fiction, and game reviews.

**License: [MIT](LICENSE) · Copyright (c) 2026 OrcastraStudio.** This is the early 0.1.2 source edition (`git-publication-r2`). The public [OrcastraStudio/Textura repository](https://github.com/OrcastraStudio/Textura) was first published and verified on 2026-10-26 from commit [0e320cc](https://github.com/OrcastraStudio/Textura/commit/0e320cc2fe3454c7f6768e1bad81a80d05a37054), on `main`. As of that date, no release tag or published GitHub Release exists. Formal release naming and support commitments remain open; see [release decisions](PENDING_DECISIONS.md).

## For readers

Textura is shared so readers can quickly understand the tools available to support the author's creative process. You do not need to install it to understand that process.

| Part of the process | Textura's role | Author's role |
| --- | --- | --- |
| Research and evidence | Organize sources, versions, quotations and claim assessments | Check sources and decide what supports an argument |
| Drafting and revision | Preserve drafts; provide protocols for discussing structure, wording and alternatives with an AI host | Set intentions, choose revisions and approve the final text |
| Review | Freeze selected inputs and record critiques, disagreements and open questions | Evaluate criticism and decide what to change |
| Disclosure | Support a brief account of actual AI assistance | Describe what was used in the particular published work |

For a game review, an illustrative workflow is to organize the author's own play notes and cited sources, discuss an outline with an AI host, revise the draft, check factual claims, and explain the actual assistance received. Firsthand play experience and critical judgments must come from the author. This example describes a possible workflow, not a record of an already completed review.

The repository shows the toolkit's capabilities and limits. It does not establish which tools were used for a specific work; that work's own disclosure should explain the actual contributions. The public source contains no private manuscripts or conversations.

MIT covers the software and accompanying project materials. Using the tool does not by itself place an author's independent articles, poems, fiction or game reviews under MIT. See [license scope](LICENSE_STATUS.md).

## Start

Install Python 3.11 or newer. Extract the complete bundle to a writable directory, open a terminal in the included Textura directory, then run:

    python -B Runner/current/textura.py status
    python -B Runner/current/textura.py doctor
    python -B Runner/current/textura.py validate

On Windows, you may use Runner/current/textura.ps1 with Python on PATH or TEXTURA_PYTHON set. No Codex installation, model account, Node.js or paid API is required for the core commands. No dependencies are installed automatically.

For AI-assisted work, explicitly load [the operating entry](Textura/Governance/current/README.md) and [agent rules](Textura/Governance/current/AGENTS.md) into your chosen host. The component-local AGENTS.md is not guaranteed to be discovered automatically. The host supplies research, interpretation and composition.

Read [commands](Textura/Runner/current/COMMAND.md), [architecture](Textura/Governance/current/architecture.md), [reading formats](Textura/Reading/current/README.md) and [edition changes](RELEASE_NOTES.md).

## What runs

The CLI creates topics, works, immutable source/draft snapshots, text extractions, claim assessments, frozen review packets, decisions and handoffs. Structural validation checks hashes and selected references. URL registration does not download a page. A recorded assessment is a reasoned judgment, not proof of a claim.

Style analysis, fiction structure/continuity, translation, research and literary review include operating protocols and blank templates. They are performed by the host/author; this release has no automatic fiction engine, style statistics engine or model orchestrator. See [capability boundaries](Textura/Governance/current/style-fiction-design.md).

New CLI organization and source records default to local_only. A deliberate --policy cloud_allowed or configured global default can permit cloud processing within the actual author-approved scope. Labels are instructions for the host, not encryption or a technical data-loss prevention barrier. No command calls a cloud model. The configurable default applies to CLI organization/source creation; unscoped State records and direct Python calls retain the base defaults. See Configuration's documented policy scope before storing sensitive decisions.

Bibliotheca Magna is an optional disabled connector with no bundled library data. Core operation does not depend on it. Publishing and backups are not automated.

## Check the installation

From the Textura directory:

    python -B Quality/current/run_checks.py

Tests generate isolated synthetic fixtures and preserve a fresh local report. Optional PDF/XLSX tests may skip if readers are unavailable. Testing writes to this extracted working copy; keep the original ZIP if you need the unchanged candidate. [Validation scope](VALIDATION.md) states what was actually checked for this package.

This bundle contains program definitions, generic documentation, blank templates, synthetic tests and public implementation snapshots. It carries no author corpus, private presets, conversation history, machine-specific audit logs, credentials or third-party library binaries.

## Repository publication and participation

See [publishing steps](PUBLISHING.md), [repository description](REPOSITORY_DESCRIPTION.md), [release description](RELEASE_DESCRIPTION.md), [contribution guidance](CONTRIBUTING.md), [security reporting](SECURITY.md), [conduct draft](CODE_OF_CONDUCT.md), [support](SUPPORT.md), [third-party notice](THIRD_PARTY_NOTICES.md) and [changelog](CHANGELOG.md).

All 20 required component history directories are retained in Git. Configuration and Governance contain public snapshots preserved before the MIT decision; Governance also preserves the state before this publication-status update. Git attributes preserve content bytes for existing seals. See [publication and Git verification](GIT_VALIDATION.md). The public source repository is available; a formal GitHub Release remains a separate pending step.
