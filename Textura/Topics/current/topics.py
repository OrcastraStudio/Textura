"""Topic/work organization; relationships are explicit, never inferred as fact."""
from storage import envelope, save_record, require_record

def create(root, kind, title, *, topic_id=None, language=None, genre=None, processing_policy="cloud_allowed"):
    if kind not in {"topic", "work", "object", "series"}:
        raise ValueError("Unknown organization object")
    if not title.strip():
        raise ValueError("A display title is required")
    if topic_id:
        topic = require_record(root, "Topics", "topic", topic_id)
        if topic.get("processing_policy") == "local_only":
            processing_policy = "local_only"
    if processing_policy not in {"cloud_allowed", "local_only"}:
        raise ValueError("Invalid processing policy")
    if kind == "work" and not language:
        raise ValueError("A work needs an explicit language")
    record = envelope(kind, kind, title=title, topic_id=topic_id,
                      processing_policy=processing_policy, status="active", relationships=[])
    if kind == "work":
        record.update(language=language, genre=genre or "unspecified", language_relationship="independent")
    return save_record(root, "Topics", kind, record)
