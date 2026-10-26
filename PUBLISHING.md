# Publishing Textura with Git

The [OrcastraStudio/Textura repository](https://github.com/OrcastraStudio/Textura) is public. Its first source publication was completed and verified on 2026-10-26 on `main`, starting at commit [0e320cc](https://github.com/OrcastraStudio/Textura/commit/0e320cc2fe3454c7f6768e1bad81a80d05a37054); see [verification](GIT_VALIDATION.md). No tag or published GitHub Release exists as of that check. This guide covers subsequent source maintenance and a future formal release.

## 1. Select the publication scope

Use a working copy of this repository bundle, whose top level contains README.md and Textura/. Do not initialize or upload the personal Textura installation or its Distribution directory. Extract outside that personal installation; ordinary .git metadata must not be placed inside its component-only runtime tree.

Only this sanitized source bundle belongs in the repository. ZIP and SHA256SUMS.txt from the prepared release may be attached as release assets, rather than committed.

## 2. Confirm the recorded release identity

The author selected MIT, copyright attribution OrcastraStudio, and the public repository OrcastraStudio/Textura. The grant is in [LICENSE](LICENSE); [LICENSE_STATUS.md](LICENSE_STATUS.md) explains its scope. The published source retains the `git-publication-r2` edition identifier; a formal release tag is still undecided.

License metadata and status documents were updated consistently after preserving Configuration and Governance snapshots. Future component edits require a snapshot before editing, then affected-component seals and validation. Keep remaining support and community-policy decisions explicit in PENDING_DECISIONS.md.

Use the full current source when preparing archives. Earlier revision 1 ZIP files do not contain the MIT decision or current documentation.

## 3. Validate locally

From this bundle's repository root:

    python -B Textura/Runner/current/textura.py validate
    python -B Textura/Quality/current/run_checks.py
    python -B Maintainer/release.py verify

After deliberate release edits, use Maintainer/release.py refresh, then verify. The refresh tool updates the outer manifest, not component seals. Retain a fresh source archive/checksum if release content changes; never attach the older candidate ZIP as though it contained a newly selected license.

.gitkeep files retain each required history directory in Git. .gitattributes disables automatic line-ending conversion so checkout preserves existing component hashes. Do not bulk-normalize files without proper snapshots, seals and a new manifest.

## 4. Confirm the destination and authentication

The public repository already contains the initial source publication on `main`. Use its existing publication working copy and inspect `git status`, `git remote -v` and the latest remote `main` before maintenance. Preserve the existing repository-local author identity and use the authenticated GitHub connection. Never put access tokens in repository URLs or project files.

Official reference: [adding existing source to GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).

## 5. Inspect, commit and synchronize maintenance

Run these commands in the existing publication repository root, not in its Textura subdirectory. Initial Git setup and the `origin` remote are already in place.

    git status --short --branch
    git remote -v
    git ls-remote --heads origin main
    git diff --stat
    git diff

If the remote has advanced, inspect and integrate its changes before continuing. After the checks in section 3, stage only the reviewed maintenance files, affected component snapshots/seals and refreshed MANIFEST.json. Then inspect:

    git diff --cached --stat
    git diff --cached
    git ls-files

Runtime records, manuscripts, sources, secrets, private presets and local reports must not be staged. .gitignore prevents common accidental additions; it does not remove already tracked files. Keep the configured author name OrcastraStudio and the author's verified GitHub no-reply email. Do not guess an email or substitute a private registration address; see [GitHub commit email guidance](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address).

Commit the reviewed change with a descriptive message, then synchronize the authorized update:

    git push origin main

Verify that local and remote `main` match after the push. Do not use force-push to fix an unexpected conflict; inspect the remote history first.

## 6. Configure the project page and release

Copy the short text and topics from REPOSITORY_DESCRIPTION.md. Review and adopt community policies; configure the private reporting route described in SECURITY.md. Issue templates are provided as portable copy-and-paste documents; do not assume a host has enabled a template chooser.

Formal release creation remains pending and requires a maintainer decision. When authorized, create a draft release from the intended tested commit. Choose a tag; v0.1.2-rc.1 is only a suggested candidate identifier. Use RELEASE_DESCRIPTION.md as the body and mark a candidate as a pre-release. Attach the matching archive and checksums. Check licensing, pending decisions and the exact uploaded files before publishing the draft.

Official references: [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository), [private reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

## 7. Check the hosted copy

Clone the published repository into a new location and repeat native validation, tests and manifest verification. Confirm required history directories exist, the README renders, and no private files appear in tracked history.

Automated CI is not configured by this preparation. Adopt a tested platform/dependency matrix before advertising a CI badge or support guarantee. Future source revisions require a new manifest and release artifacts.
