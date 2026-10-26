"""Register actually acquired local originals or honest URL-only records."""
from pathlib import Path
from urllib.parse import urlsplit
import shutil
from storage import envelope, owned, mkdir, write_json, read_json, file_digest, identifier, save_record, inside

def get_source(root, source_id):
    record = read_json(owned(root, "Sources", "records", identifier(source_id), "manifest.json"))
    if record.get("id") != source_id:
        raise ValueError("Source directory and record ID do not match")
    original = record.get("original_file")
    if original and (not isinstance(original, str) or Path(original).name != original or ":" in original):
        raise ValueError("Source original must be a local filename within its record")
    if original:
        folder = owned(root, "Sources", "records", source_id)
        inside(folder, folder/original)
    return record

def register(root, *, title, file=None, url=None, scope="unknown", processing_policy="cloud_allowed"):
    if not title.strip() or (not file and not url):
        raise ValueError("Source needs a title and a local file or URL")
    if url and (urlsplit(url).scheme not in {"https", "http"} or not urlsplit(url).netloc):
        raise ValueError("Source URL must be an absolute HTTP(S) URL")
    if scope not in {"complete", "partial", "unknown", "link_only"}:
        raise ValueError("Unknown capture scope")
    if processing_policy not in {"cloud_allowed", "local_only"}:
        raise ValueError("Invalid processing policy")
    source = Path(file).resolve() if file else None
    if source and (not source.is_file() or source.stat().st_size > 256*1024*1024):
        raise ValueError("Source file missing or exceeds the 256 MiB initial capture limit")
    if source and scope == "link_only":
        raise ValueError("A captured file cannot be declared link_only")
    record = envelope("source", "source", title=title, url=url, capture_scope=scope if source else "link_only",
                      processing_policy=processing_policy, verification_status="unassessed",
                      published_at=None, author=None, original_name=source.name if source else None,
                      original_file=None, sha256=None, acquisition_method="explicit_local_import" if source else "url_registration_only")
    folder = owned(root, "Sources", "records", record["id"])
    mkdir(folder, Path(root)/"Sources")
    if source:
        suffix = source.suffix.lower() if len(source.suffix) < 16 else ".bin"
        target = folder / ("original"+suffix)
        before = file_digest(source)
        with source.open("rb") as src, target.open("xb") as out:
            shutil.copyfileobj(src, out)
        after = file_digest(target)
        if before != after or before != file_digest(source):
            raise ValueError("Source changed during acquisition; incomplete capture retained for inspection")
        record.update(original_file=target.name, sha256=after)
    return write_json(folder/"manifest.json", record, boundary=Path(root)/"Sources")

def read_source(root, source_id):
    from readers import extract
    source = get_source(root, source_id)
    if not source["original_file"]:
        raise ValueError("URL-only source has no acquired content; acquire a file before reading")
    path = owned(root, "Sources", "records", source["id"], source["original_file"])
    if file_digest(path) != source["sha256"]:
        raise ValueError("Captured original digest changed")
    record = envelope("reading", "reading", source_id=source["id"], source_sha256=source["sha256"],
                      processing_policy=source["processing_policy"], **extract(path))
    return save_record(root, "Reading", "readings", record)
