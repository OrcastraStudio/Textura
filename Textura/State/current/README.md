# State

Keep compact research and creation decisions with portable handoffs. `author_decision`, `ai_proposal`, `observation` and `open_question` are distinct kinds. Author decisions require an explicit basis; a suggestion never silently becomes consent or a permanent preference.

`state_records.py` saves key records and creates a handoff referencing active drafts and claims. Handoffs are append-only snapshots, not always-current dashboards. Prepare a new one after material changes. Read assessments individually: existence does not imply truth, completeness, consensus or currency. Retain important dissent, unresolved issues and reasons.

Only key records are saved by default. Preserve passages when they materially explain a decision. Full conversation archiving needs its own scope; never reconstruct missing messages or export private model reasoning. External library transfer, if requested, remains selective.

## Style and fiction continuation

The [shared capability description](../../Governance/current/style-fiction-decisions.md) is not a private author decision log. No personal State records are bundled. Reports of needs, observed features and provisional creative goals retain actual scope and must not become permanent preferences automatically.

Specialized Style/Fiction records stay with their owners. Reference them in decision text/basis and an explicit continuation note when needed. The current handoff function enumerates Topics/Writing/Evidence/State records; it does not automatically discover every Style/Fiction record or personal preset. On resumption, read the selected owner records and any configured preset as well as the current handoff.

## Processing policy scope

The configured CLI default applies to topic, object, series, work and source creation. Derived records follow their documented input policies. Unscoped State decisions retain the base implementation's cloud_allowed label, and handoffs use the most restrictive included record (cloud_allowed for an empty set). Direct Python producer calls retain their existing defaults. Therefore this is not a universal local-only enforcement setting. Bind sensitive decisions to a local_only work, and the host must inspect actual records and obtain the applicable scope before any cloud transmission. No local command transmits content. Extending the configured default to all unscoped records is a pending release decision.
