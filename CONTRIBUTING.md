# Contributing

Textura is an early source edition licensed under [MIT](LICENSE), with copyright attribution to OrcastraStudio. Submit only material you have the right to contribute under the project's license, and identify any third-party material and its terms. See [license scope](LICENSE_STATUS.md).

Report a problem using [the bug template](ISSUE_TEMPLATE/bug_report.md), or describe a proposal using [the feature template](ISSUE_TEMPLATE/feature_request.md). These files are portable copy-and-paste templates; hosting-platform automatic selection is not claimed. Avoid real manuscripts, private sources, credentials and local account paths.

Before modifying a component, read its README and Textura/Governance/current/AGENTS.md. Preserve its definitions using the documented snapshot command before substantive changes; keep new records and implementation history with their owner. Document observed behavior and actual limitations. Do not turn an AI suggestion into an author decision.

From the repository root, run:

    python -B Textura/Runner/current/textura.py validate
    python -B Textura/Quality/current/run_checks.py

For changed definitions, snapshot first, edit, perform relevant checks, then seal only the affected component and validate again. Never reseal merely to hide an unexplained mismatch. Update public documentation and run python -B Maintainer/release.py refresh followed by verify before a release. Refresh is release bookkeeping, not permission to publish.

Use synthetic fixtures. Do not submit runtime records, personal presets or model-generated claims of tests that were not executed. Explain AI assistance accurately when relevant to reviewing the contribution.

The optional library connector is disabled by default. Changes must work without a configured library. Larger services, dependencies or structural changes should be discussed before implementation. No response time, merge promise or long-term support commitment is established.
