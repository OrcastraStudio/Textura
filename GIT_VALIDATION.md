# Publication and Git validation

## Published pre-release verification — 2026-10-26

[v0.1.2-rc.1](https://github.com/OrcastraStudio/Textura/releases/tag/v0.1.2-rc.1) was published at 2026-10-26T21:47:15Z with draft=false and prerelease=true. Its annotated tag resolves to `fce94bd7f4f6310510415a030170db186ae7ef82`. A fresh GitHub clone supplied the ZIP's exact 198 tracked files; no personal installation or working-directory inventory was packaged.

The extracted ZIP passed startup, structure, snapshot and manifest checks; the existing acceptance suites passed 63 tests and skipped 1 because symbolic-link creation was unavailable. All 95 component-document links and 42 outer-document links resolved. The source ZIP, MANIFEST.json and SHA256SUMS.txt were downloaded from their public GitHub asset URLs and matched the local SHA256 hashes.

The following main-branch publication-record update adds Governance history/v0003 and refreshes current document seals and the outer manifest. That maintained inventory contains 211 manifest entries, or 212 files including MANIFEST.json. The released tag still contains 198 files; historical counts below retain their original scope.

## Public repository verification — 2026-10-26

- GitHub's repository API confirms [OrcastraStudio/Textura](https://github.com/OrcastraStudio/Textura) is Public, with default branch `main` and detected license MIT. LICENSE names Copyright (c) 2026 OrcastraStudio.
- The first published commit is [0e320cc](https://github.com/OrcastraStudio/Textura/commit/0e320cc2fe3454c7f6768e1bad81a80d05a37054) (`0e320cc2fe3454c7f6768e1bad81a80d05a37054`). Before this status-maintenance update, local HEAD and live remote `main` both matched it, and the publication working copy was clean.
- The baseline's 183 manifest entries matched their file hashes and sizes; the 184 Git-tracked paths matched those entries plus MANIFEST.json.
- GitHub's public Releases API returned no published releases, and the remote had no tags. Public source publication is complete; a formal GitHub Release remains pending.
- These checks verify the publication baseline. The preparation evidence below retains its original scope and does not claim a new hosted-checkout test run. Subsequent maintenance commits extend this history; the initial commit above is not a permanent claim about the current HEAD.

## Publication-status maintenance validation — 2026-10-26

Governance's definitions at the publication baseline were preserved byte-for-byte in history/v0002 before updating its current status documents. The current Governance seal and outer manifest were refreshed. The maintained inventory contains 197 public file entries, or 198 files including MANIFEST.json; historical preparation counts below still describe their original revisions.

The local acceptance run passed 63 tests and skipped 1 because symbolic-link creation was unavailable. All 95 current installation-document links and 42 outer repository-document links resolved, and structural validation found no errors or warnings. Validation prose was finalized after that run, then the final manifest was refreshed and verified again. Runtime reports and fixture outputs are excluded from the public inventory. See VALIDATION.md for the test scope.

## Historical preparation revision 2 — 2026-10-26

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
