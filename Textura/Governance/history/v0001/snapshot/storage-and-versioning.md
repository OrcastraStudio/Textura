# Storage and versioning

## Directory contract

The runnable Textura root is the directory containing its registered component directories. It contains component directories only. Each component owns its implementation and data:

```text
Component/
  current/
    README.md
    records/
  history/
```

All directory names match `[A-Za-z0-9_-]+`. File names are not subject to that ASCII restriction. Author manuscripts and imported originals can retain meaningful original filenames and multilingual content. Generated identifiers and directories use ASCII-safe names without changing titles in metadata.

`current/` is the only authoritative implementation location. Do not create a second root-level `latest`, generic `docs`, `releases` or shared data directory. A component may create subdirectories within its own tree for code, templates, assets, originals and records as documented by that component. Keep paths portable and installation-relative wherever feasible.

## Two kinds of version

1. **Component implementation history:** before a later substantive change to existing operational code, rules, configuration, contracts or templates, create a component snapshot through the documented Runner operation. Each immutable snapshot belongs under that component's `history/`, with its manifest and change explanation. Never fabricate prior releases. At initial creation the history directories are empty.
2. **Research and manuscript versions:** imported originals, draft revisions, assessments and review rounds are operational data. Preserve them inside their owner's `current/records/` or the explicitly documented owner-local original/output directory. They do not belong in the component's implementation history. Record predecessor/version relationships rather than overwriting source originals or frozen review inputs.

Component snapshots exclude operational records and large user originals as specified by Runner. They are not a backup of the author's work. No backup service or destination is configured. A user may separately choose a backup arrangement. Preserve ordinary history and manuscript versions without describing them as independent backup coverage.

## Edits and ownership

- A component may update only the records it owns. Cross-component operations call the documented owner interface or follow its schema.
- Evidence owns claims and assessments; Review consumes references or frozen exports. Sources owns original source captures; Reading owns standalone source extraction records. Writing owns manuscript versions and their embedded reading projections; Publishing owns prepared derivatives. Reading supplies the common extraction implementation, while the caller saves the output within the documented owner's tree.
- State owns cross-session key decisions and handoffs. Other modules may keep their specialized findings, but State links to them rather than duplicating authoritative ledgers.
- Preserve unmodified author originals and imported source files. A corrected extract or revised draft is a new derivative/version with provenance.
- Record rejected or superseded decisions as such. Do not edit historical evidence to make a current choice appear inevitable.
- A new component is created within its own directory, receives `current/` and `history/`, documents inputs/outputs and status, and is added to the architecture and contract registry.

## Safe maintenance

Use the documented `snapshot`, `seal` and `validate` operations in [Runner](../../Runner/current/COMMAND.md). New components are added through the documented manual registration procedure; there is no component-scaffolding command. Consult command help rather than inventing arguments. Check path ownership before writes or moves. Do not follow symbolic links or copied instructions outside the intended owner boundary. If a task needs a directory elsewhere, resolve the real path and scope first.

For a change touching several components, snapshot each affected existing implementation separately, then validate the shared interfaces. Record which checks actually ran and any remaining unsupported behavior.

## Style/fiction records and personal configuration

Style owns selected sample references and stylistic interpretations. Fiction owns plans, work-local settings, knowledge records and impact reports. Formal shared settings remain externally versioned by the selected provider once its interface exists; LibraryBridge stores acquired snapshots/references and never edits them as competing formal originals. Writing retains exercise and trial prose.

Versioned personal workflow presets belong under Configuration/current/records/author-presets/. These runtime records are excluded from implementation snapshots. The candidate selects no personal preset; a future configured preset must identify an exact version. Redistributable builds need separate review excluding private presets, records, originals and author-specific decision evidence unless separately selected and permitted.

New protocol records follow the [style/fiction contract](../../Contracts/current/style-fiction-contracts.md). Supersede earlier findings with owner-local records rather than erasing their earlier state.
