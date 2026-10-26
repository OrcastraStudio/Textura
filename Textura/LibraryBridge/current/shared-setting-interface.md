# Optional shared fictional-setting interface

Status: proposed optional interface contract; a formal shared-setting module and write adapter are not implemented. The Bibliotheca bridge is disabled by default. If deliberately configured, its CLI supports documented read-only search/show/cite only.

## Authority and scope

A deliberately configured future provider may maintain author-selected formal shared-setting versions. Textura/Fiction owns work-local settings, working branches, experiments and change proposals. Fiction records which exact shared version each work adopts. LibraryBridge owns acquired references/snapshots and transfer receipts, not an independently editable formal canon.

Use an optional provider boundary for the shared core. A user without Bibliotheca can use independent Textura work-local settings; another formal shared-setting provider requires an explicit implemented adapter. No shared-setting provider is required for ordinary local fiction planning.

Ordinary research remains limited reference with selected preservation. Old conversations remain dated evidence of earlier discussion, not the author's current belief. A fictional-setting record needs an explicit fictional nature and author-adoption basis; the library's reviewed flag is not author approval or proof of real-world truth.

## Required future read information

- Stable provider and setting identity, exact version and actual file/content locator.
- Actual content, or an explicit link-only/missing/partial state.
- Input digest or provider integrity reference and acquisition time/scope.
- Work/branch/timeline applicability and author-approved versus proposed status.
- Predecessor/version relations, change description and any local-only handling.
- A verifiable reference for the author decision establishing formal status.

These describe needed meaning, not existing BM fields or commands. Confirm exact encoding and version/update behavior against the selected provider's actual contract before writing an adapter.

## Work adoption and changes

1. Obtain the selected exact version through the documented provider capability when available; retain provenance in LibraryBridge records.
2. Fiction records work/branch adoption and the corresponding author decision. Do not interpret newest-available as adopted.
3. A new formal version generates a difference/impact proposal. Each work independently chooses whether and when to adopt it; rejected or deferred adoption remains visible.
4. Textura develops proposed changes locally. Transfer only selected scope with its actual author instruction, base version, changes, reasons, affected works and processing restrictions.
5. Only a genuine successful library operation can produce a library version/receipt. A prepared packet or selected proposal is not a completed update. Never replace library originals with direct file edits.
6. If versions conflict, preserve both and clarify by impact; do not merge silently or overwrite based on recency.

If the future module is absent, use local working plans and keep external formal status pending. If a selected version is unavailable, an actually acquired immutable snapshot may be used with its acquisition state and limitations; otherwise report the gap. Never substitute another version silently.

## Packet and receipt

Use [the outgoing template](shared-setting-outgoing.template.json) for preparation only. Formal publication/update semantics, idempotency, failures and conflict receipts remain unresolved interface work. The existing generic preservation packet remains suitable for ordinary selected research and milestone archives.

All acquired snapshots, version-reference records, pending packets and actual receipts remain within LibraryBridge/current/records/. Fiction's adoption records refer to them. Private author content and local-only restrictions propagate to packets and derivatives.

The template and protocol perform no external contact, shared-setting creation, library update, synchronization or messaging.
