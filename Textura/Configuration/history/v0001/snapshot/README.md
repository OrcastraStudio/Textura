# Configuration

`settings.json` contains configurable starter settings. `components.json` is the ownership registry. Neither file grants permission to spend money, transmit restricted content, publish, scrape logged-in services or modify an external library.

This source candidate contains no personal preset. Style and fiction remain configurable for different authors and works. If a user creates a versioned workflow preset, store it under Configuration/current/records/author-presets/ and select it explicitly. A preset is not a sample-derived Style finding and is not automatically enforced by the CLI.

## Processing and integrations

New CLI organization and source records default to local-only processing. An explicit cloud policy and authorized task scope are needed for cloud use; descendants retain restrictive source policies. A policy label is host guidance, not encryption or an operating-system access barrier.

Bibliotheca Magna is disabled and its root is unset. The ordinary workflow does not require it. Configure a selected local installation only when needed; follow [LibraryBridge](../../LibraryBridge/current/README.md). Do not store credentials or API keys here. The shared_fictional_settings fields describe a planned optional provider boundary, not an implemented write service.

Automatic paid calls, publication, library writeback, adoption of external settings and backup services are not configured. No provider account or API entitlement is bundled.

## Defaults and maintenance

The agent_defaults describe [starter editorial policy](../../Governance/current/decisions.md). They are not personal author decisions, an automatic disclosure generator, scheduler or backup implementation. Work choices may override editorial defaults while provenance and processing restrictions remain required.

Internal references are relative to the installation root. Archive Configuration before substantive changes to released settings or registry entries, then seal and validate. Work-specific preferences belong with their own records instead of silently changing global defaults.

New components declare name, purpose, dependencies, execution mode and current entry. Follow [storage and versioning](../../Governance/current/storage-and-versioning.md). No component scaffolder is implemented.

## Processing policy scope

The configured CLI default applies to topic, object, series, work and source creation. Derived records follow their documented input policies. Unscoped State decisions retain the base implementation's cloud_allowed label, and handoffs use the most restrictive included record (cloud_allowed for an empty set). Direct Python producer calls retain their existing defaults. Therefore this is not a universal local-only enforcement setting. Bind sensitive decisions to a local_only work, and the host must inspect actual records and obtain the applicable scope before any cloud transmission. No local command transmits content. Extending the configured default to all unscoped records is a pending release decision.
