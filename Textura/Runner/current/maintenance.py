"""Structural validation and component-local version snapshots."""
from pathlib import Path
import json
import re
import shutil
from storage import read_json, write_json, inside, identifier, DIRECTORY, RESERVED, now, file_digest, mkdir

RUNTIME_DIRS = {"records", "outputs", "cache", "__pycache__", ".pytest_cache"}

def registry(root):
    return read_json(Path(root)/"Configuration"/"current"/"components.json")["components"]

def definition_files(current):
    for file in sorted(Path(current).rglob("*")):
        relative = file.relative_to(current)
        if any(p in RUNTIME_DIRS for p in relative.parts) or file.name == "release-manifest.json":
            continue
        if file.is_symlink() or getattr(file, "is_junction", lambda: False)():
            raise ValueError("Definition links are not allowed in version snapshots")
        if file.is_file():
            inside(current, file)
            yield file

def seal(root, component):
    component = identifier(component)
    if component not in {c["name"] for c in registry(root)}:
        raise ValueError("Unregistered component")
    current = inside(root, Path(root)/component/"current")
    result = {"component": component, "version": read_json(current/"component.json")["version"],
              "sealed_at": now(), "scope": "Definition files only; excludes runtime records, outputs and caches",
              "files": {str(f.relative_to(current)).replace("\\", "/"): file_digest(f) for f in definition_files(current)}}
    write_json(current/"release-manifest.json", result, boundary=Path(root)/component, replace=True)
    return result

def snapshot(root, component, reason):
    component = identifier(component)
    if component not in {c["name"] for c in registry(root)} or not reason.strip():
        raise ValueError("Snapshot requires a registered component and reason")
    expected = Path(root).resolve()/component
    base = inside(root, expected)
    if base != expected:
        raise ValueError("Component roots cannot alias other directories")
    current, history = inside(base, base/"current"), inside(base, base/"history")
    files = list(definition_files(current))
    if (current/"release-manifest.json").exists():
        files.append(current/"release-manifest.json")
    existing = [int(d.name[1:]) for d in history.iterdir() if re.fullmatch(r"v\d{4,}", d.name)]
    version = f"v{max(existing, default=0)+1:04d}"
    dest = inside(base, history/version)
    mkdir(dest.parent, base)
    dest.mkdir(exist_ok=False)
    entries = {}
    for file in files:
        relative = file.relative_to(current)
        target = dest/"snapshot"/relative
        mkdir(target.parent, base)
        shutil.copy2(file, target)
        entries[relative.as_posix()] = file_digest(target)
    metadata = {"component": component, "archive_id": version, "created_at": now(), "reason": reason,
                "scope": "Full component definitions; runtime records/outputs/caches excluded",
                "original_base": "current", "files": entries,
                "restore": "Archive the active definitions first, then copy selected files from this snapshot into this component's current. Never edit this archive."}
    write_json(dest/"version.json", metadata, boundary=base)
    (dest/"version.md").write_text(f"# {component} {version}\n\nCreated: {metadata['created_at']}\n\nReason: {reason}\n\n{metadata['scope']}\n\nOriginal base: current/\n\nRestore: {metadata['restore']}\n\nFile digests and exact paths: version.json\n", encoding="utf-8")
    return metadata

def validate(root):
    root = Path(root).resolve()
    errors, warnings = [], []
    try:
        components = registry(root)
    except (OSError, ValueError) as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": []}
    names = {c["name"] for c in components}
    if len(names) != len(components):
        errors.append("Duplicate registered component names")
    for child in root.iterdir():
        if not child.is_dir() or child.name not in names:
            errors.append(f"Unowned root entry: {child.name}")
    for path in root.rglob("*"):
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            errors.append(f"Unexpected filesystem link: {path.relative_to(root)}")
            continue
        if path.is_dir() and (not DIRECTORY.fullmatch(path.name) or path.name.upper() in RESERVED):
            errors.append(f"Invalid directory name: {path.relative_to(root)}")
    for component in components:
        name = component["name"]
        current = root/name/"current"
        try:
            identifier(name)
            if not (root/name/"history").is_dir():
                errors.append(f"{name}: missing history directory")
            for required in ("README.md", "component.json", "release-manifest.json"):
                if not (current/required).is_file():
                    errors.append(f"{name}: missing {required}")
            for dependency in component.get("depends_on", []):
                if dependency not in names:
                    errors.append(f"{name}: unknown dependency {dependency}")
            if (current/"release-manifest.json").exists():
                release = read_json(current/"release-manifest.json")
                actual = {p.relative_to(current).as_posix(): file_digest(p) for p in definition_files(current)}
                if actual != release["files"]:
                    errors.append(f"{name}: active definitions differ from release manifest; archive before editing and reseal after validation")
            for archive in (root/name/"history").glob("v*/version.json"):
                manifest = read_json(archive)
                for relative, expected in manifest["files"].items():
                    p = inside(archive.parent/"snapshot", archive.parent/"snapshot"/relative)
                    if not p.is_file() or file_digest(p) != expected:
                        errors.append(f"{name}: historical snapshot mismatch {archive.parent.name}/{relative}")
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f"{name}: {exc}")
    from sources import get_source
    from evidence import check_reference
    from writing import latest
    from storage import records, require_record
    for directory in (root/"Sources"/"current"/"records").glob("*"):
        if directory.is_dir() and not (directory/"manifest.json").is_file():
            errors.append(f"Incomplete source import: {directory.name}")
    for p in (root/"Sources"/"current"/"records").glob("*/manifest.json"):
        try:
            item = read_json(p)
            if item.get("original_file"):
                original = inside(p.parent, p.parent/item["original_file"])
                if file_digest(original) != item["sha256"]:
                    errors.append(f"Source changed: {item['id']}")
            elif item["capture_scope"] != "link_only":
                errors.append(f"Source has neither original nor link_only scope: {item['id']}")
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f"Source {p.parent.name}: {exc}")
    try:
        for r in records(root, "Reading", "readings"):
            source = get_source(root, r["source_id"])
            if r["source_sha256"] != source["sha256"]:
                errors.append(f"Reading version mismatch: {r['id']}")
        for work in records(root, "Topics", "work"):
            base = root/"Writing"/"current"/"records"/work["id"]
            if (base/"latest.json").exists():
                latest(root, work["id"])
            for p in (base/"drafts").glob("*/manifest.json"):
                d = read_json(p)
                if file_digest(inside(p.parent, p.parent/d["original_file"])) != d["sha256"]:
                    errors.append(f"Draft original changed: {d['id']}")
        for c in records(root, "Evidence", "claims"):
            if c.get("work_id"):
                require_record(root, "Topics", "work", c["work_id"])
            if c.get("topic_id"):
                require_record(root, "Topics", "topic", c["topic_id"])
            if c.get("draft_id"):
                read_json(root/"Writing"/"current"/"records"/identifier(c["work_id"])/"drafts"/identifier(c["draft_id"])/"manifest.json")
        for a in records(root, "Evidence", "assessments"):
            require_record(root, "Evidence", "claims", a["claim_id"])
            if a["verdict"] in {"supported", "contradicted", "mixed"} and not a["evidence"]:
                errors.append(f"Assessment missing evidence: {a['id']}")
            for ref in a["evidence"]:
                check_reference(root, ref)
        from review import status as review_status
        for p in (root/"Review"/"current"/"records").glob("*/manifest.json"):
            result = review_status(root, p.parent.name)
            if result.get("stale"):
                warnings.append(f"Review needs re-check against current draft: {p.parent.name}")
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f"Record integrity: {exc}")
    return {"valid": not errors, "errors": errors, "warnings": warnings,
            "scope": "Filesystem ownership, definition hashes and selected record/reference integrity. No semantic fact verification or publication approval."}
