# Release decisions

Updated 2026-10-26. Confirmed choices and remaining questions are distinguished below. Local preparation and a license grant do not themselves establish a published release or a support commitment.

| ID | Decision | Status and current behavior |
| --- | --- | --- |
| OS01 | Code and documentation license; copyright holder and attribution wording | Resolved: MIT, Copyright (c) 2026 OrcastraStudio. See LICENSE and LICENSE_STATUS.md. |
| OS02 | Public repository, owner/account, publication date and release naming | Repository selected and created by the author: https://github.com/OrcastraStudio/Textura (Public). Upload verification, formal release date and tag remain pending at this preparation stage. |
| OS03 | Whether the conservative starter privacy policy and editorial defaults should become public defaults | New CLI organization/source records start local_only; editorial settings are configurable suggestions, not personal aesthetic rules. |
| OS04 | Supported host/OS/Python matrix and optional reader versions | Python 3.11+ is the documented baseline; only the actual local validation environment is claimed as tested. No dependency lock or platform certification. |
| OS05 | Maintainer contact, contribution process, issue templates, security reporting and support commitment | Contribution, conduct, support and security drafts supplied in Git revision 1; maintainer adoption, contact, private reporting setup and commitments remain pending. |
| OS06 | Optional Bibliotheca distribution, compatible external versions and future shared-setting provider contract | Disabled optional read-only adapter; no bundled library, write adapter or setting synchronization. |
| OS07 | Public examples, documentation translations and tutorial materials | README now explains the reader-facing purpose and an illustrative game-review workflow. No real author materials or completed case studies selected; further tutorials/translations remain open. |
| OS09 | Extend configured privacy defaults to all unscoped record producers and templates | CLI organization/source creation is covered. Unscoped State/direct Python defaults remain documented base behavior; prepared outgoing packets start local_only and must preserve input restrictions. |
| OS08 | License/attribution review for the intended optional dependency distribution | Optional libraries are not bundled; nothing installed automatically. |

Details may be decided independently. Record new decisions and preserve prior source revisions when release contents change. The original Git preparation revision 1 remains separate; this working edition is revision 2.
