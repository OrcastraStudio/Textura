# Git publication preparation validation

## Revision 2 — 2026-10-26

- Git 2.55.0.windows.5 staged the intended 184 public files, including the MIT License and the outer manifest. The staged paths exactly match the manifest inventory plus MANIFEST.json.
- A Git tree archive reproduced every staged file byte-for-byte. All 20 required component history directories survived. Public Configuration and Governance snapshots preserve the definitions preceding the license/status update.
- Runtime records, outputs and caches are excluded from the staged tree. Pattern checks found no matching credential tokens, private-key headers or personal absolute paths in the public file inventory; this bounded scan is not a comprehensive security audit.
- The revised installation passed structural validation and 64 synthetic tests: 63 passed, 1 skipped because symbolic-link creation was unavailable. All 94 installation links and 39 outer-document links resolved. See VALIDATION.md.
- The original revision 1 source files still match their manifest. The original archive/checksums do not identify revision 2.
- Validation prose was finalized after the checks, followed by a fresh manifest and staged-tree byte comparison. These checks do not certify a remote upload, hosted checkout or published release.

Test environment: Windows and Python 3.12.14. No new OS/Python compatibility claim or automated CI is established. Live GitHub authentication and hosted verification remain separate steps.

## Historical revision 1 — 2026-10-02

Revision: 0.1.2 Git publication preparation r1. Locally checked on 2026-10-02; not remotely published.

- Git 2.55.0.windows.5 staged all 162 intended public files.
- With core.autocrlf=true, a Git tree archive reproduced every tracked file byte-for-byte. No user identity, commit, tag, remote or network operation was needed for this test.
- All 20 required history directories survived through tracked .gitkeep placeholders.
- The extracted Git tree passed native structural validation, manifest verification and the 64-test synthetic acceptance suite: 63 passed, 1 skipped because the host could not create a symbolic link.
- The manifest verifier detected an intentional synthetic change to SUPPORT.md; after restoration it verified the tree again.
- Original 0.1.2 executable component files and seals are unchanged. Added tooling is limited to outer release-manifest verification and refresh.
- Final release-note/validation text is finalized after the test run. Final packaging checks independently verify the resulting complete file hashes.

Test environment: Windows 11 and Python 3.12.14. Other OS/Python versions, live hosting behavior, authentication, actual remote pushes and automatic template discovery were not tested. Portable issue templates can be copied manually on any host. No automated CI workflow is configured.

Machine-specific reports and temporary Git metadata remain outside this public source package. These checks do not select a license or certify source truth, literary quality, security, or universal privacy enforcement.
