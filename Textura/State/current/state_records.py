"""Key working decisions and portable handoffs, never reconstructed transcripts."""
from storage import envelope, save_record, records, require_record

def decision(root, kind, text, *, work_id=None, basis=None):
    if kind not in {"author_decision", "ai_proposal", "observation", "open_question"}:
        raise ValueError("Invalid decision kind")
    if not text.strip() or (kind == "author_decision" and not basis):
        raise ValueError("Author decisions require an explicit basis/reference to the author's instruction")
    policy = require_record(root, "Topics", "work", work_id)["processing_policy"] if work_id else "cloud_allowed"
    return save_record(root, "State", "decisions", envelope("decision", "decision", kind=kind,
        text=text, work_id=work_id, basis=basis, processing_policy=policy))

def handoff(root, work_id=None):
    works = records(root, "Topics", "work")
    if work_id:
        works = [require_record(root, "Topics", "work", work_id)]
    ids = {w["id"] for w in works}
    topics = records(root, "Topics", "topic")
    if work_id:
        topics = [t for t in topics if t["id"] in {w.get("topic_id") for w in works}]
    topic_ids = {t["id"] for t in topics}
    decisions = [d for d in records(root, "State", "decisions") if d.get("work_id") in ids or not d.get("work_id")]
    claims = [c for c in records(root, "Evidence", "claims") if not work_id or c.get("work_id") in ids or (not c.get("work_id") and c.get("topic_id") in topic_ids)]
    claim_ids = {c["id"] for c in claims}
    assessments = [a for a in records(root, "Evidence", "assessments") if a["claim_id"] in claim_ids]
    assessed = {a["claim_id"] for a in assessments}
    active = []
    from writing import latest
    for work in works:
        try:
            draft = latest(root, work["id"])
            active.append({"work_id": work["id"], "draft_id": draft["id"], "sha256": draft["sha256"]})
        except FileNotFoundError:
            active.append({"work_id": work["id"], "draft_id": None})
    payload = works+topics+decisions+claims+assessments
    policy = "local_only" if any(p.get("processing_policy") == "local_only" for p in payload) else "cloud_allowed"
    return save_record(root, "State", "handoffs", envelope("handoff", "handoff", work_id=work_id,
        works=works, topics=topics, active_drafts=active, decisions=decisions,
        assessment_ids=[a["id"] for a in assessments],
        unassessed_claim_ids=[c["id"] for c in claims if c["id"] not in assessed],
        notice="Assessment existence does not mean supported or current; inspect all verdicts, dissent and draft bindings before reuse.",
        claim_ids=[c["id"] for c in claims], processing_policy=policy,
        coverage="Structured local records only; no full conversation archive or private reasoning.",
        next_agent_instructions="Read Governance/current/README.md and this work's referenced records. Respect processing_policy before transmitting content. Preserve author decisions, proposals and uncertainty as distinct states."))
