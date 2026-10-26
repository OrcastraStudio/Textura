"""Immutable Word/text draft imports; author-selected latest pointer."""
from pathlib import Path
import shutil
from storage import envelope, owned, mkdir, read_json, write_json, require_record, file_digest, identifier, inside

def latest(root, work_id):
    work_id = identifier(work_id)
    pointer = read_json(owned(root, "Writing", "records", work_id, "latest.json"))
    draft_id = identifier(pointer["draft_id"])
    folder = owned(root, "Writing", "records", work_id, "drafts", draft_id)
    record = read_json(folder/"manifest.json")
    if pointer.get("work_id") != work_id or record.get("id") != draft_id or record.get("work_id") != work_id:
        raise ValueError("Draft pointer, directory and ownership do not match")
    original = record.get("original_file")
    if not isinstance(original, str) or Path(original).name != original or ":" in original:
        raise ValueError("Draft original must be a local filename within its record")
    inside(folder, folder/original)
    return record

def import_draft(root, work_id, file):
    from readers import extract
    work = require_record(root, "Topics", "work", work_id)
    source = Path(file).resolve()
    if not source.is_file() or source.stat().st_size > 256*1024*1024:
        raise ValueError("Draft missing or exceeds 256 MiB")
    before = file_digest(source)
    try:
        previous = latest(root, work_id)
    except FileNotFoundError:
        previous = None
    if previous and previous["sha256"] == before:
        existing = owned(root, "Writing", "records", work_id, "drafts", previous["id"], previous["original_file"])
        if file_digest(existing) != before:
            raise ValueError("Previously imported draft was altered")
        return {**previous, "reused_existing_snapshot": True}
    record = envelope("draft", "draft", work_id=work_id, sha256=before,
                      original_name=source.name, original_file="original"+(source.suffix.lower() or ".txt"),
                      previous_draft_id=previous["id"] if previous else None,
                      processing_policy=work["processing_policy"])
    folder = owned(root, "Writing", "records", work_id, "drafts", record["id"])
    mkdir(folder, Path(root)/"Writing")
    target = folder/record["original_file"]
    with source.open("rb") as src, target.open("xb") as dst:
        shutil.copyfileobj(src, dst)
    if file_digest(target) != before or file_digest(source) != before:
        raise ValueError("Draft changed during import; do not use incomplete capture")
    record["reading"] = extract(target)
    write_json(folder/"manifest.json", record, boundary=Path(root)/"Writing")
    write_json(owned(root, "Writing", "records", work_id, "latest.json"),
               {"draft_id": record["id"], "work_id": work_id}, boundary=Path(root)/"Writing", replace=True)
    return record
