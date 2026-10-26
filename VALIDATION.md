# Validation scope — Textura 0.1.2

## Publication-status maintenance (2026-10-26)

After synchronizing the repository and Governance publication-status documents, the existing acceptance suites were re-run on Windows with Python 3.12.14. Reading passed 18 tests; Review passed 11 and skipped 1 because symbolic-link creation was unavailable; Quality passed 34. Total: 63 passed, 1 skipped. The skipped case remains unverified on this host.

All 95 current installation-document links and 42 outer repository-document links resolved. Structural validation reported no errors or warnings. Governance's pre-update definitions were preserved in history/v0002, its current definitions were resealed, and the refreshed outer manifest verified 197 public file entries (198 files including MANIFEST.json).

The update changes publication-status documentation and integrity metadata, with no executable workflow change. Tests use synthetic data; generated reports and fixture outputs remain excluded from Git. The 0.1.2 functional version and git-publication-r2 edition identifier are retained. Earlier validation evidence follows with its original scope.

## Historical Git preparation revision 2 (2026-10-26)

The MIT source edition was checked locally on Windows with Python 3.12.14. Reading ran 18 passing tests; Review ran 11 passing tests and skipped 1 because symbolic-link creation was unavailable; Quality ran 34 passing tests. Total: 63 passed, 1 skipped. All 94 current installation-document links resolved, and structural validation reported no errors or warnings. A separate check resolved 39 links in the outer repository documents.

These checks use synthetic data. No live AI host, model API, author manuscript or external source library was involved. Generated local reports are excluded from Git. Configuration and Governance were snapshotted and resealed after license/status updates. The executable record workflow is unchanged. See GIT_VALIDATION.md for current Git packaging checks.

## Historical source-candidate validation (2026-10-02)

Validated locally on 2026-10-02 with Python 3.12.14 on Windows 11. Python 3.11+ is the documented baseline; other Python versions and operating systems were not executed in this preparation.

The synthetic acceptance suites ran 64 tests: 63 passed and 1 skipped. Reading: 18 passed. Review: 11 passed and 1 skipped because this host could not create a symbolic link. Quality: 34 passed, including seven public-edition regression tests. The skip is an untested case on this host, not a passed check.

The tested implementation includes optional-library absence handling, source/draft version integrity, evidence references, review packet boundaries, topic policy inheritance, CLI integration and portable library configuration. Ninety-two installation-document links resolved. Native structure validation found no errors or warnings.

With Python site-package loading disabled (-S), status, doctor and validate also succeeded from a directory outside the installation. PDF/XLSX readers correctly reported unavailable; the optional library bridge remained disabled. This check establishes baseline startup without third-party packages, not an exhaustive no-dependency test matrix.

The final bundle is rebuilt from the same tested definition inputs. Runtime reports, fixture output directories and private build receipts are excluded. Public component seals and the outer MANIFEST.json identify the delivered content; external SHA256SUMS.txt records the archive and manifest hashes.

Tests use synthetic data. No network service, model account, paid API, real source collection, personal manuscript or external library was queried. No literary judgment, source-authenticity claim, legal/license approval, hostile-document sandbox certification or live Word round-trip is established by these checks.

To run fresh checks in an extracted writable working copy, enter Textura/ and run:

    python -B Quality/current/run_checks.py

That command creates new local test reports and temporary fixtures. Keep the original archive for an unchanged copy of the candidate.

## Historical Git preparation revision 1

The functional core and original test evidence above are retained. Git revision 1 adds history-directory placeholders and repository documents/tooling. Its separate local Git and manifest checks are in GIT_VALIDATION.md. The original archive hash does not identify this revised package.
