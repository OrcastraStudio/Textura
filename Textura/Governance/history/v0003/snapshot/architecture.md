# Component architecture

Textura combines local record-handling mechanics with AI-executed operating protocols. There is one authoritative owner for each kind of data. A reference to another component does not transfer ownership.

| Component | Owns | Main inputs and dependencies | Initial execution |
|---|---|---|---|
| Governance | Operating rules, starter policies, architecture | Applicable author scope; all component boundaries | Agent-readable documents |
| Configuration | Portable settings and defaults | Governance; current host capabilities | Local configuration |
| Contracts | Shared record contracts and identifiers | Governance; producer/consumer agreement | Local schema and validation guidance |
| Runner | Local command interface and orchestration mechanics | Configuration, Contracts; component handlers | Executable local commands |
| Topics | Topics, research objects, works and series relationships | Author goals; discovered links | Local records plus agent curation |
| Research | Search plans, research briefs and search logs | Topics; Sources; Evidence; limited LibraryBridge reference | Agent-executed retrieval and reasoning |
| Sources | Source metadata, original files and captured versions | Research or author-provided materials | Local registration and capture records |
| Reading | Reader implementation, standalone source extraction records and locator mapping | Sources originals; available readers | Text-first local readers; explicit gaps; draft projections are embedded with their Writing version |
| Translation | Translation notes, terminology and cross-language uncertainty | Reading; Sources originals | Agent-executed translation |
| Evidence | Single claim/assessment ledger and evidence relationships | Writing; Sources; Reading; Translation; Analysis | Local records; semantic assessment by agents/authors |
| Analysis | Requested analysis plans, methods and derived results | Source data and reading records | Agent-executed analysis with reproducible artifacts |
| Writing | Manuscript versions and candidate edits | Topics; Research; Evidence; author input | Local version records and AI collaboration |
| Style | Selected sample references, scoped observations, preferences, provisional goals and voice/practice/reference analyses | Writing; Sources/Reading; author choices | Agent-executed protocols and templates; no statistics engine |
| Fiction | Material maps, structural alternatives, work-local settings, knowledge states, continuity and impacts | Topics; Writing; LibraryBridge version references | Agent-executed protocols and templates; no CLI handler |
| Review | Frozen review inputs, three perspectives and synthesis | Writing version; Evidence snapshot; genre criteria; manually scoped supplemental Fiction/Style records | Local freeze mechanics and agent reasoning; extended fiction contexts remain agent-managed |
| State | Key decisions, open questions and handoff records | All module outcomes | Local continuity records |
| Publishing | Prepared full works, excerpts and platform adaptations | Accepted manuscript; citations; author output goals | Agent-prepared outputs; manual publication |
| Feedback | Author-selected reader comments and analyses | Published-work references; selected comments | Agent-executed analysis |
| LibraryBridge | Bibliotheca Magna references and selected outgoing packets | BM documented local interface; Sources and State | Read-only bridge and preparation; no BM writes |
| Quality | Structural verification and AMS audit evidence | Contracts; component implementations; observed tests | Local checks and human/agent audit |

## Main flows

```text
Topics -> Research -> Sources -> Reading -> Translation (when needed)
                                   |          |                 |
                                   +----------+-----------------+-> Evidence
Sources/Reading -> Analysis (on request) --------------------------> Evidence
Topics/Research/Evidence -> Writing -> Review -> author decision -> Writing
Writing/Evidence -> Publishing -> author publishes -> selected Feedback -> Topics
LibraryBridge -> limited Research reference
selected records -> LibraryBridge outgoing packet
Writing/planning notes -> Fiction -> structural/continuity proposals -> Writing/Review
selected text references -> Style -> scoped analyses/practice goals -> Writing/Review
future shared-setting provider -> LibraryBridge exact-version references -> Fiction adoption
all meaningful outcomes -> State references and handoff
```

Style supplies genre-sensitive criteria to Writing and Review. It does not independently overwrite a manuscript. Evidence changes can trigger re-review, and manuscript changes can trigger reassessment; both are explicit new work against recorded versions.

## Interfaces and trust

Use [Contracts](../../Contracts/current/README.md) for shared record shapes, [settings](../../Configuration/current/settings.json) for defaults, and [Runner](../../Runner/current/COMMAND.md) for actual command behavior. Markdown templates are agent work aids, not extra CLI record types or proof that a specialized service exists.

Bibliotheca Magna remains a separate system. Its notes can suggest sources or connections but do not substitute for original evidence. Initial bridge output is a selected packet for a later authorized library workflow, not an automatic ingest, promotion or archive.

AI reasoning cannot be made into factual proof by a successful schema check. Reviewers consume the same frozen evidence, so agreement is not independent external corroboration. Recognition/questioning independence is procedural; the host's ability to provide isolated contexts must be stated accurately.

## Extension seams

Future readers add formats without changing source identity. Future output adapters consume accepted versions and citation records without replacing them. Future AI hosts read local contracts, decisions and handoffs without inheriting hidden chat context. New paid integrations, autonomous retrieval depth and external actions remain scoped to actual author requests.

## Style and fiction extension in 0.1.2

Read [collaboration design](style-fiction-design.md) and [decisions](style-fiction-decisions.md). Fiction is a registered protocol component with structure and world/continuity subfunctions. It references work IDs and manuscript versions. Review's supplemental fiction/style contexts and LibraryBridge's formal-setting contract are agent-managed or planned interfaces, not new CLI capabilities.

Personal workflow configuration stays in Configuration's owner-local records, selected by an explicit reference. Preliminary creative aims are not public defaults. This candidate carries no personal preset. Licensing and publication are tracked in [release-pending.md](release-pending.md).
