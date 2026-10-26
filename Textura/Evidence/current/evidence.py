"""Claim and assessment ledger. Referential checks are not semantic fact proof."""
from pathlib import Path
from storage import envelope, save_record, require_record, read_json, owned, identifier, file_digest
from sources import get_source

VERDICTS = {"supported", "contradicted", "mixed", "inconclusive", "not_applicable"}
KINDS = {"fact", "quotation", "number", "causal", "interpretation", "speculation", "value"}

def claim(root, statement, *, work_id=None, topic_id=None, kind="fact", priority="normal", supersedes=None):
    if not statement.strip() or (not work_id and not topic_id):
        raise ValueError("A claim needs a statement and work or topic")
    if kind not in KINDS or priority not in {"high", "normal", "low"}:
        raise ValueError("Invalid claim kind or priority")
    policy = "cloud_allowed"
    draft_id = None
    if work_id:
        work = require_record(root, "Topics", "work", work_id)
        policy = work["processing_policy"]
        try:
            from writing import latest
            draft_id = latest(root, work_id)["id"]
        except FileNotFoundError:
            pass
    if topic_id:
        topic = require_record(root, "Topics", "topic", topic_id)
        if topic["processing_policy"] == "local_only":
            policy = "local_only"
    if supersedes:
        old = require_record(root, "Evidence", "claims", supersedes)
        if old.get("work_id") != work_id or old.get("topic_id") != topic_id:
            raise ValueError("Superseded claim must have the same ownership scope")
        if old.get("processing_policy") == "local_only":
            policy = "local_only"
    return save_record(root, "Evidence", "claims", envelope("claim", "claim", statement=statement,
        work_id=work_id, topic_id=topic_id, draft_id=draft_id, kind=kind, priority=priority,
        processing_policy=policy, supersedes=supersedes, initial_status="unassessed"))

def check_reference(root, ref):
    reading = require_record(root, "Reading", "readings", identifier(ref["reading_id"]))
    source = get_source(root, reading["source_id"])
    reading_sha256 = file_digest(owned(root, "Reading", "records", "readings", reading["id"]+".json"))
    anchors = {"source_id": source["id"], "source_sha256": source.get("sha256"), "reading_sha256": reading_sha256}
    for key, expected in anchors.items():
        if key in ref and ref[key] != expected:
            raise ValueError(f"Evidence reference anchor changed: {key}")
    if not source.get("original_file") or source.get("sha256") != reading.get("source_sha256"):
        raise ValueError("Evidence must reference the acquired source version")
    original = owned(root, "Sources", "records", source["id"], source["original_file"])
    if file_digest(original) != source["sha256"]:
        raise ValueError("Evidence original was changed")
    locator, excerpt = ref.get("locator"), ref.get("excerpt", "")
    if not isinstance(excerpt, str) or not excerpt.strip():
        raise ValueError("Evidence needs an exact excerpt")
    matching = [b for b in reading.get("blocks", []) if b.get("locator") == locator]
    if not matching or not any(excerpt in b["text"] for b in matching):
        raise ValueError("Excerpt not present at the claimed extraction locator")
    original_inspected = ref.get("original_inspected")
    if original_inspected is not None and not isinstance(original_inspected, bool):
        raise ValueError("original_inspected must be a boolean or null (unknown)")
    chain = ref.get("attribution_chain", [])
    if not isinstance(chain, list) or not all(isinstance(item, str) for item in chain):
        raise ValueError("attribution_chain must be a list of explanatory strings")
    return {"source_id": source["id"], "source_sha256": source["sha256"], "reading_id": reading["id"], "reading_sha256": reading_sha256,
            "locator": locator, "excerpt": excerpt, "source_title": source["title"], "url": source.get("url"),
            "capture_scope": source["capture_scope"], "extraction_status": reading["extraction_status"],
            "processing_policy": source["processing_policy"],
            "original_inspected": original_inspected,
            "attribution_chain": chain,
            "source_version_note": ref.get("source_version_note")}

def assess(root, claim_id, verdict, rationale, refs, *, assessor="current-agent", supersedes=None):
    target = require_record(root, "Evidence", "claims", claim_id)
    if verdict not in VERDICTS or not rationale.strip():
        raise ValueError("Assessment needs an allowed verdict and rationale")
    if verdict in {"supported", "contradicted", "mixed"} and not refs:
        raise ValueError("Decisive assessments require checkable evidence")
    checked = [check_reference(root, ref) for ref in refs]
    previous_policy = "cloud_allowed"
    if supersedes:
        old = require_record(root, "Evidence", "assessments", supersedes)
        if old["claim_id"] != claim_id:
            raise ValueError("Cannot supersede another claim's assessment")
        previous_policy = old.get("processing_policy")
    policy = "local_only" if previous_policy == "local_only" or target["processing_policy"] == "local_only" or any(r["processing_policy"] == "local_only" for r in checked) else "cloud_allowed"
    return save_record(root, "Evidence", "assessments", envelope("assessment", "assessment", claim_id=claim_id,
        verdict=verdict, rationale=rationale, evidence=checked, assessor=assessor, supersedes=supersedes,
        processing_policy=policy, validation_scope="reference_integrity_only",
        semantic_review_status="assessor_judgment_recorded"))
