# Writing

Authors may import supported Word or text drafts and discuss changes through their chosen AI host. `writing.py` imports a selected draft into an immutable version with a SHA-256 and reader output. `latest.json` selects the active submitted draft. It is the only replaceable pointer; earlier draft bodies and manifests remain preserved. Importing the same bytes reuses the existing active snapshot.

Do not edit an author's external Word file as a side effect of reading or reviewing it. Candidate edits, reasons and author adoption belong to this component's work records and State decisions. Before a materially changed draft is used, import a new snapshot; earlier opinions remain bound to their previous version. Word pagination is not inferred from paragraph indexes. The text projection cannot stand in for complete Word formatting or tracked-changes acceptance.

Agent workflow: discuss the intent; offer angles or structure when requested; present candidate paragraph changes with reasons; record adoption; preserve the original; re-check affected factual claims. Independent works may have different languages, voices and structures. A future LaTeX adapter must retain source/claim/version links.

Implemented: local draft import and active-version selection. Not implemented: live Word monitoring, automatic revision acceptance, faithful Word round-trip rendering or LaTeX compilation. Agent-created publishable documents require their own rendering/visual QA workflow.

## Exploratory arguments and objections

The starter editorial policy permits clearly marked hypotheses or interpretations when their status, evidence, counterexamples and gaps are explicit; authors may choose differently for a work. Do not silently promote an exploratory statement into an established premise later in the same or another work. Preserve the author's ability to choose differently for a specific piece.

In argumentative works, select strong objections directly relevant to the central argument and incorporate them naturally into the body or notes. Offer a reasoned response or acknowledge the remaining limitation. The full review record need not be reproduced in the finished article. Hypothetical AI objections remain analysis, not statements attributed to actual scholars or readers. Publishing owns reader-facing citation/disclosure/correction presentation; these defaults do not authorize overwriting an external author manuscript.

## Style, fiction and practice handoffs

Writing remains the owner of actual manuscript, trial, exercise and candidate prose versions. Style supplies expression goals and analyses; Fiction supplies structural goals, planning notes and impact references. Neither component keeps an alternative authoritative manuscript. Author-selected style samples refer to the precise Writing version; practice is not automatically added to the sample catalogue.

Use the existing import workflow for actual supported text and preserve adoption references in State. Release 0.1.2 supplies no special practice/scene import command or Word automation; no manuscript content is bundled. Reordered or rewritten passages need new version/locator references before old observations are reused. See the [shared protocol contract](../../Contracts/current/style-fiction-contracts.md).
