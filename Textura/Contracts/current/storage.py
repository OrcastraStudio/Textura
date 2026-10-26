"""Shared, local-only record primitives. No model calls or semantic verification."""
from __future__ import annotations
import hashlib
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,95}$")
DIRECTORY = re.compile(r"^[A-Za-z0-9_-]+$")
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1,10)), *(f"LPT{i}" for i in range(1,10))}

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value) or value.upper() in RESERVED:
        raise ValueError("Invalid ASCII record/component identifier")
    return value

def new_id(prefix):
    return f"{identifier(prefix)}-{uuid.uuid4().hex[:16]}"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def file_digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def inside(root, path):
    base = Path(root).resolve()
    candidate = Path(path).resolve()
    if not candidate.is_relative_to(base):
        raise ValueError("Path escapes its owning component/workspace")
    return candidate

def owned(root, component, *parts):
    identifier(component)
    actual_names = {p.name for p in Path(root).iterdir() if p.is_dir()}
    if component not in actual_names:
        raise ValueError("Unknown component or incorrectly cased component name")
    expected = Path(root).resolve() / component
    base = inside(root, expected)
    if str(base) != str(expected):
        raise ValueError("Component roots cannot alias other directories")
    return inside(base, base / "current" / Path(*parts))

def mkdir(path, boundary):
    path = inside(boundary, path)
    relative = path.relative_to(Path(boundary).resolve())
    for part in relative.parts:
        if not DIRECTORY.fullmatch(part) or part.upper() in RESERVED:
            raise ValueError(f"Invalid ASCII directory name: {part}")
    path.mkdir(parents=True, exist_ok=True)
    return path

def read_json(path):
    path = Path(path)
    if path.stat().st_size > 32*1024*1024:
        raise ValueError("Record exceeds 32 MiB limit")
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write_json(path, value, *, boundary, replace=False):
    path = inside(boundary, path)
    mkdir(path.parent, boundary)
    if path.exists() and not replace:
        raise FileExistsError(f"Record already exists: {path.name}")
    temporary = path.with_name(f".pending-{uuid.uuid4().hex}.json")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        if not replace and path.exists():
            raise FileExistsError("Concurrent record write detected")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return value

def envelope(record_type, prefix, **fields):
    return {"schema_version": "1.0", "id": new_id(prefix), "record_type": record_type,
            "created_at": now(), **fields}

def records(root, component, category):
    folder = owned(root, component, "records", category)
    result = []
    if folder.exists():
        for path in sorted(folder.glob("*.json")):
            record = read_json(inside(folder, path))
            if identifier(path.stem) != record.get("id"):
                raise ValueError("Record filename and ID do not match")
            result.append(record)
    return result

def require_record(root, component, category, record_id):
    record = read_json(owned(root, component, "records", category, identifier(record_id)+".json"))
    if record.get("id") != record_id:
        raise ValueError("Record filename and ID do not match")
    return record

def save_record(root, component, category, record):
    base = Path(root) / component
    return write_json(owned(root, component, "records", category, identifier(record["id"])+".json"), record, boundary=base)
