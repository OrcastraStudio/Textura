"""Explicit, read-only bridge to the existing Bibliotheca Magna CLI."""
from pathlib import Path
import json
import os
import shutil
import subprocess
from storage import read_json

def node_binary():
    requested = os.environ.get("TEXTURA_NODE", "node")
    executable = shutil.which(requested)
    if executable:
        return executable
    raise ValueError("Node.js is unavailable; set TEXTURA_NODE or configure PATH")

def configured_library(settings):
    config = settings.get("bibliotheca", {})
    if config.get("enabled") is not True:
        return None
    value = config.get("root")
    if not isinstance(value, str) or not value.strip():
        return None
    library = Path(value).expanduser()
    if not library.is_absolute():
        raise ValueError("The enabled Bibliotheca root must be an absolute local path")
    return library.resolve()

def run(root, action, value, *, version=None, file=None, extraction=None, line=None):
    if action not in {"search", "show", "cite"}:
        raise ValueError("Only search, show and cite are implemented in the bridge")
    if not value or value.startswith("-"):
        raise ValueError("A literal query/ID is required")
    settings = read_json(Path(root)/"Configuration/current/settings.json")
    library = configured_library(settings)
    if library is None:
        raise ValueError("Bibliotheca is disabled or unconfigured; explicitly enable it and configure its root first")
    script = library/"tools/bm.mjs"
    if not script.is_file() or not (library/"AGENTS.md").is_file():
        raise ValueError("Configured Bibliotheca Magna entry is unavailable")
    args = [node_binary(), str(script), action]
    args.append(value)
    options = {"version": version, "file": file, "extraction": extraction, "line": line}
    if action != "cite" and any(v is not None for v in options.values()):
        raise ValueError("Locator options are only supported for cite")
    for key, option in options.items():
        if option is not None:
            if not str(option).strip() or str(option).startswith("-"):
                raise ValueError("Citation locator values must be nonempty literals")
            args.extend(["--"+key, str(option)])
    result = subprocess.run(args, cwd=library, capture_output=True, text=True, encoding="utf-8", timeout=60, shell=False)
    if result.returncode:
        raise ValueError(f"Bibliotheca command failed ({result.returncode}): {result.stderr or result.stdout}")
    return {"bridge_action": action, "write_performed": False, "library_root": str(library),
            "result": json.loads(result.stdout), "interpretation": "Library notes and conversations are limited-reference leads; inspect original evidence for factual support."}
