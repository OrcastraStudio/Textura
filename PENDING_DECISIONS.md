# Release decisions

Updated 2026-10-26 after publishing and verifying [v0.1.2-rc.1](https://github.com/OrcastraStudio/Textura/releases/tag/v0.1.2-rc.1). The repository is public, and the first tagged GitHub pre-release is available. Stable-release timing and support commitments remain open.

| ID | Decision | Status and current behavior |
| --- | --- | --- |
| OS01 | Code and documentation license; copyright holder and attribution wording | Resolved: MIT, Copyright (c) 2026 OrcastraStudio. See LICENSE and LICENSE_STATUS.md. |
| OS02 | Public repository, owner/account, publication date and release naming | Public source publication completed and verified on 2026-10-26 at [OrcastraStudio/Textura](https://github.com/OrcastraStudio/Textura); default branch `main`, initial commit [0e320cc](https://github.com/OrcastraStudio/Textura/commit/0e320cc2fe3454c7f6768e1bad81a80d05a37054). Local and remote commits matched during verification. The author subsequently approved and published [v0.1.2-rc.1](https://github.com/OrcastraStudio/Textura/releases/tag/v0.1.2-rc.1) on 2026-10-26, targeting `fce94bd7f4f6310510415a030170db186ae7ef82`. The Release is marked Pre-release; its source ZIP, manifest and SHA256 checksums were verified after public download. Stable-release timing remains undecided. |
| OS03 | Whether the conservative starter privacy policy and editorial defaults should become public defaults | New CLI organization/source records start local_only; editorial settings are configurable suggestions, not personal aesthetic rules. |
| OS04 | Supported host/OS/Python matrix and optional reader versions | Python 3.11+ is the documented baseline; only the actual local validation environment is claimed as tested. No dependency lock or platform certification. |
| OS05 | Maintainer contact, contribution process, issue templates, security reporting and support commitment | Contribution, conduct, support and security drafts supplied in Git revision 1; maintainer adoption, contact, private reporting setup and commitments remain pending. |
| OS06 | Optional Bibliotheca distribution, compatible external versions and future shared-setting provider contract | Disabled optional read-only adapter; no bundled library, write adapter or setting synchronization. |
| OS07 | Public examples, documentation translations and tutorial materials | README now explains the reader-facing purpose and an illustrative game-review workflow. No real author materials or completed case studies selected; further tutorials/translations remain open. |
| OS09 | Extend configured privacy defaults to all unscoped record producers and templates | CLI organization/source creation is covered. Unscoped State/direct Python defaults remain documented base behavior; prepared outgoing packets start local_only and must preserve input restrictions. |
| OS08 | License/attribution review for the intended optional dependency distribution | Optional libraries are not bundled; nothing installed automatically. |

Details may be decided independently. Record new decisions and preserve prior source revisions when release contents change. The original Git preparation revision 1 remains separate. The published source retains the `git-publication-r2` edition identifier and 0.1.2 executable workflow; subsequent Git commits record maintenance updates.
