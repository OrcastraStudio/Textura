# Source edition changes — Textura 0.1.2

## v0.1.2-rc.1 public preview (2026-10-26)

Published [v0.1.2-rc.1](https://github.com/OrcastraStudio/Textura/releases/tag/v0.1.2-rc.1) as a Pre-release from `fce94bd7f4f6310510415a030170db186ae7ef82`. The attached ZIP contains exactly that commit's 198 tracked files. Its manifest and SHA256 checksums were verified after public download. The extracted source passed 63 tests with 1 symbolic-link-related skip on Windows/Python 3.12.14. No functional code changed for this release.

This later main-branch documentation update records the completed publication and preserves Governance's prior definitions in history/v0003. It does not move the tag or replace the released assets. Earlier sections record the preparation state at their respective checks.

## Public source publication and maintenance (2026-10-26)

The first public source publication was completed and verified on `main` at [OrcastraStudio/Textura](https://github.com/OrcastraStudio/Textura), starting with commit [0e320cc](https://github.com/OrcastraStudio/Textura/commit/0e320cc2fe3454c7f6768e1bad81a80d05a37054). MIT and OrcastraStudio attribution are in effect. No tag or published GitHub Release exists as of the status check; formal release decisions remain open.

This maintenance update synchronizes publication-status documents, preserves Governance's prior definitions in `history/v0002`, and refreshes its seal and the outer manifest. It retains the `git-publication-r2` edition identifier and changes no executable workflow. See [publication verification](GIT_VALIDATION.md) and [release decisions](PENDING_DECISIONS.md).

## Git publication preparation revision 2 (2026-10-26)

Current edition identifier: git-publication-r2. MIT selected by the author with copyright attribution to OrcastraStudio. README now explains the toolkit to readers, includes game reviews and distinguishes software licensing from independent creative works. Configuration and Governance definitions were snapshotted before applying the decision. No executable writing workflow changed. See [changelog](CHANGELOG.md), [license scope](LICENSE_STATUS.md) and [release decisions](PENDING_DECISIONS.md).

## Initial source adaptation (2026-10-02)

Edition identifier: 0.1.2-open-source-candidate. Base functional release: Textura 0.1.2. Component versions retain their own version history; they need not all match the system release.

This is an explicitly adapted source edition, not a byte-identical copy of the personal installation.

- Retains all 20 core components, executable record workflow, evidence/reading mechanics, tests and style/fiction protocols.
- Removes private runtime data, author presets, component history snapshots, personal decision evidence, host-specific logs and machine paths.
- Rewrites personal governance material into generic design and configurable starter policy documents. No author aesthetic profile is shipped.
- Leaves Bibliotheca disabled with root unset. doctor handles its absence; bridge commands return a clear configuration error before attempting an external process.
- Uses Python and optional Node from explicit environment configuration or PATH rather than a Codex cache layout.
- Makes new CLI organization/source records inherit the configured processing default, local_only for this candidate, while supporting explicit per-record override and restrictive parent inheritance.
- Adds public-edition regression tests for optional integration and processing defaults. Updates the synthetic CLI fixture registry to include Fiction.
- Regenerates component definition seals. Empty history directories establish this edition's starting state; private history is not converted into public history.

No model integration, online retrieval engine, graphical editor, automatic style statistics, automatic long-fiction continuity engine, new Bibliotheca write interface, backup service or publishing service was added. Word import remains text projection with documented limitations; TeX input is text, not a built-in compiler.

The local release builder, private source recipe and private maintenance audit records are not part of this source edition. Public manifests describe public files only. Future release preparation must re-review changed source definitions and overlays.
