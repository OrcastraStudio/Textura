# Textura 0.1.2 source distribution candidate

Textura is a local system for author-led research and writing with an AI collaborator. It organizes topics, evidence, manuscripts, review and publication preparation. Operational instructions are primarily English; manuscripts, quotations and author dialogue may use any language.

This sanitized source edition is derived from Textura 0.1.2 and licensed under [MIT](../../../LICENSE), with copyright attribution to OrcastraStudio. See [release status](release-pending.md) for the selected repository and remaining release decisions.

## Start here

The runnable Textura root contains component directories only. This file is its Governance-owned entry point.

1. Read [AGENTS.md](AGENTS.md), [starter policies](decisions.md) and [storage-and-versioning.md](storage-and-versioning.md).
2. Read [architecture.md](architecture.md) for ownership and boundaries.
3. Read [Contracts](../../Contracts/current/README.md) and [Configuration](../../Configuration/current/README.md).
4. Read [Runner commands](../../Runner/current/COMMAND.md), then the task's component protocols.
5. Before resuming a work, read its current version, evidence references and key state records. An old conversation does not establish the latest author position.

With Python 3.11 or newer, run `python Runner/current/textura.py status` from the Textura root. Begin with `status`, `doctor` and `validate`. These commands check local structure and consistency; they do not establish factual truth. The core record workflow uses the Python standard library. Optional readers and the library bridge have separately documented requirements.

## Capability boundaries

- **Local mechanics:** create and check records, retain originals, extract supported text, freeze review inputs, maintain component snapshots and expose an optional read-only Bibliotheca Magna bridge. Registering a URL does not fetch it. Preparing a review packet does not execute a review.
- **Agent-executed work:** a separately available AI host researches, interprets, translates, evaluates evidence and discusses manuscripts using the protocols. Textura does not bundle a model, provider account or search service.
- **Style and Fiction:** blank templates and protocols are supplied, not an automatic statistics service, fiction state engine or progressive-review packet builder.
- **Future adapters:** OCR/transcription, broader output rendering, advanced Word editing and LaTeX production need actual implemented capabilities before use.

The starter configuration contains no personal workflow preset, private creative corpus or private implementation history. New CLI organization and source records default to local-only handling. External cloud use needs explicit scope and an appropriate processing policy; a policy label is not an access-control mechanism.

Bibliotheca Magna is optional, disabled and unconfigured. The local workflow works without it. No automatic paid call, library write, publication or backup service is configured.

## Ownership and extensions

`current/` is authoritative for each component. `history/` stores append-only implementation snapshots. The initial sanitized edition started with empty histories; public Configuration and Governance snapshots now preserve the definitions preceding the MIT decision. Work records remain in the owner's `current/records/`. Source/manuscript versions are data, not software history.

For style and fiction, read [capabilities](style-fiction-decisions.md), [module collaboration](style-fiction-design.md), [Style](../../Style/current/README.md) and [Fiction](../../Fiction/current/README.md). Authors choose their own aesthetic aims and samples. [Open items](style-fiction-open-items.md) distinguish planned capabilities from implemented ones.

The projects in [references.md](references.md) are conceptual references. Mentioning them does not install them, imply certification or license this candidate.
