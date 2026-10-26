# Quality

Quality owns integration tests, acceptance runs and references to AMS audit results. Component-specific tests remain in Reading and Review. Synthetic fixtures never become real topics, manuscripts or evidence.

Run with Python 3.11+:

```text
python Quality/current/run_checks.py
```

The command runs the Reading, Review and Quality suites in separate processes, checks local Markdown links, then invokes structural validation. It stores a new report under this component's `current/records/runs/`. Use `--skip-structure` only during the initial build before definitions are sealed; such a report explicitly lacks that check. Tests create isolated directories below their owning component and clean them after use. Do not run tests concurrently with changes to definitions or production records.

Test success establishes only the covered mechanical behavior. It does not certify source authenticity, evidence interpretation, translation accuracy, literary quality, model independence, host privacy enforcement or successful publication. Read each run's skipped tests and limits. Machine-local reader availability is reported by Runner `doctor`.

AMS static results and semantic review are separate. Official AMS evidence/reports remain within AMS's own components. Textura stores an English receipt here with the exact run ID, report locations, actual coverage and conclusion. A successful AMS process exit is not a compliance score or automatic semantic approval. Do not change its historical static `review_status=pending`; the new semantic review states what was actually reviewed.

This initial release has no automatic ongoing monitoring. Subsequent changes must retain the affected component's history, rerun relevant checks, reseal that component, and use a new audit record when an audit is performed.
