# Publishing Textura with Git

The selected public repository is [OrcastraStudio/Textura](https://github.com/OrcastraStudio/Textura). This guide documents the upload procedure; it is not a receipt that an upload or release has occurred. Git tracks versions locally; GitHub hosts the shared repository.

## 1. Select the publication scope

Use a working copy of this repository bundle, whose top level contains README.md and Textura/. Do not initialize or upload the personal Textura installation or its Distribution directory. Extract outside that personal installation; ordinary .git metadata must not be placed inside its component-only runtime tree.

Only this sanitized source bundle belongs in the repository. ZIP and SHA256SUMS.txt from the prepared release may be attached as release assets, rather than committed.

## 2. Confirm the recorded release identity

The author selected MIT, copyright attribution OrcastraStudio, and the public repository OrcastraStudio/Textura. The grant is in [LICENSE](LICENSE); [LICENSE_STATUS.md](LICENSE_STATUS.md) explains its scope. This is Git preparation revision 2; a formal release tag is still undecided.

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

The author has created the public repository on GitHub without initial files. Confirm that it is still the intended destination before the first upload. README, LICENSE and .gitignore are supplied locally. Authenticate using GitHub's supported method. Never put access tokens in repository URLs or project files.

Official reference: [adding existing source to GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).

## 5. Initialize, inspect and upload

Run these commands in the prepared repository root, not in its Textura subdirectory. If initialization or staging was already completed, inspect the existing status rather than repeating setup blindly.

    git init -b main
    git status --short
    git add --dry-run .
    git add .
    git diff --cached --stat
    git diff --cached
    git ls-files

Inspect the staged files. Runtime records, manuscripts, sources, secrets, private presets and local reports must not be staged. .gitignore prevents common accidental additions; it does not remove already tracked files. Configure the author name OrcastraStudio and the author's exact GitHub-provided no-reply email locally for this repository. Copy that email from GitHub Settings > Emails; do not guess it or substitute a private registration email unintentionally. See [GitHub commit email guidance](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address).

Then:

    git commit -m "Publish Textura source under MIT"
    git remote add origin https://github.com/OrcastraStudio/Textura.git
    git push -u origin main

If origin is already configured, inspect git remote -v instead of adding it again. Do not use force-push to fix an unexpected conflict; inspect the remote history first.

## 6. Configure the project page and release

Copy the short text and topics from REPOSITORY_DESCRIPTION.md. Review and adopt community policies; configure the private reporting route described in SECURITY.md. Issue templates are provided as portable copy-and-paste documents; do not assume a host has enabled a template chooser.

Create a draft release from the intended tested commit. Choose a tag; v0.1.2-rc.1 is only a suggested candidate identifier. Use RELEASE_DESCRIPTION.md as the body and mark a candidate as a pre-release. Attach the matching archive and checksums. Check licensing, pending decisions and the exact uploaded files before publishing the draft.

Official references: [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository), [private reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

## 7. Check the hosted copy

Clone the published repository into a new location and repeat native validation, tests and manifest verification. Confirm required history directories exist, the README renders, and no private files appear in tracked history.

Automated CI is not configured by this preparation. Adopt a tested platform/dependency matrix before advertising a CI badge or support guarantee. Future source revisions require a new manifest and release artifacts.
