# LibraryBridge

The optional adapter exposes read-only Bibliotheca Magna search, show and cite through its documented local CLI. It is disabled and unconfigured in this source edition; the external library and its records are not bundled. All core Textura commands remain usable without it.

## Configuration and requirements

Before enabling the bridge, inspect the actual external library's instructions and command interface for compatibility. After preserving Configuration history, set bibliotheca.enabled to true and bibliotheca.root to the absolute local library root, then reseal Configuration. The adapter expects tools/bm.mjs and AGENTS.md. Node.js is discovered through TEXTURA_NODE or PATH. No runtime or library is installed automatically.

doctor reports local availability only. A disabled or unset bridge returns a clear configuration error without launching an external command. search/show/cite use argument arrays, not shell interpolation. The adapter does not implement ingestion, writeback, shared-setting updates or synchronization.

## Reference boundaries

Old conversations and summaries provide leads with dates and context; they are not original evidence or the author's current beliefs. Reviewed flags do not establish global document truth. Preserve actual access, extraction, assessment and author-adoption states separately.

Prepare selected outgoing material with [the outgoing template](outgoing-template.json). An unselected proposal or prepared packet does not authorize transfer. Any later author-requested operation must use an actually implemented provider interface, not direct edits to library originals. Optional milestone suggestions run only within the current requested workflow; there is no background monitor.

## Shared fictional settings

The [planned shared-setting interface](shared-setting-interface.md) describes exact-version adoption and ownership for an optional future provider. [The outgoing setting template](shared-setting-outgoing.template.json) is preparation only. A configured library's existence does not implement this service. Work-local settings remain usable without any external provider.
