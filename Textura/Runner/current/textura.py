"""Portable Textura command entry. Local records only; the AI host does reasoning."""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
CODE_ROOT = Path(__file__).resolve().parents[2]
for component in ("Contracts", "Topics", "Sources", "Reading", "Writing", "Evidence", "Review", "State", "LibraryBridge", "Runner"):
    sys.path.insert(0, str(CODE_ROOT/component/"current"))

def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=CODE_ROOT, help="Data installation; code always comes from this launcher installation")
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("status", "doctor", "validate"):
        sub.add_parser(name)
    for kind in ("topic", "work", "object", "series"):
        s = sub.add_parser(kind, help="Create an append-only organization record")
        s.add_argument("--title", required=True)
        s.add_argument("--topic", dest="topic_id")
        s.add_argument("--language", required=kind == "work")
        s.add_argument("--genre")
        s.add_argument("--policy", choices=("cloud_allowed", "local_only"), default=None)
    s = sub.add_parser("source", help="Register a file snapshot or link-only reference; never fetch a URL")
    s.add_argument("--title", required=True)
    s.add_argument("--file", type=Path)
    s.add_argument("--url")
    s.add_argument("--scope", choices=("complete", "partial", "unknown", "link_only"), default="unknown")
    s.add_argument("--policy", choices=("cloud_allowed", "local_only"), default=None)
    s = sub.add_parser("read")
    s.add_argument("source_id")
    s = sub.add_parser("draft")
    s.add_argument("work_id")
    s.add_argument("--file", type=Path, required=True)
    s = sub.add_parser("claim")
    s.add_argument("--statement", required=True)
    s.add_argument("--work", dest="work_id")
    s.add_argument("--topic", dest="topic_id")
    s.add_argument("--kind", default="fact", choices=("fact", "quotation", "number", "causal", "interpretation", "speculation", "value"))
    s.add_argument("--priority", default="normal", choices=("high", "normal", "low"))
    s.add_argument("--supersedes")
    s = sub.add_parser("assess")
    s.add_argument("claim_id")
    s.add_argument("--verdict", required=True, choices=("supported", "contradicted", "mixed", "inconclusive", "not_applicable"))
    s.add_argument("--rationale", required=True)
    s.add_argument("--evidence-file", type=Path, help="JSON array of exact reading references; default []")
    s.add_argument("--assessor", default="current-agent")
    s.add_argument("--supersedes")
    s = sub.add_parser("review")
    r = s.add_subparsers(dest="action", required=True)
    q = r.add_parser("prepare")
    q.add_argument("work_id")
    q.add_argument("--blind", action="store_true", help="Poem-only inputs; automatic for poetry and free_verse")
    q = r.add_parser("advance")
    q.add_argument("run_id")
    q.add_argument("--recognition-file", type=Path, required=True)
    q.add_argument("--challenge-file", type=Path, required=True)
    q = r.add_parser("status")
    q.add_argument("run_id")
    s = sub.add_parser("decision")
    s.add_argument("--kind", required=True, choices=("author_decision", "ai_proposal", "observation", "open_question"))
    s.add_argument("--text", required=True)
    s.add_argument("--work", dest="work_id")
    s.add_argument("--basis")
    s = sub.add_parser("handoff")
    s.add_argument("--work", dest="work_id")
    s = sub.add_parser("snapshot", help="Archive component definitions before maintenance edits")
    s.add_argument("component")
    s.add_argument("--reason", required=True)
    s = sub.add_parser("seal", help="Record current definition hashes after initial build or archived maintenance")
    s.add_argument("component")
    s = sub.add_parser("bm", help="Read-only Bibliotheca Magna access")
    s.add_argument("action", choices=("search", "show", "cite"))
    s.add_argument("value")
    for name in ("version", "file", "extraction", "line"):
        s.add_argument("--"+name)
    return p

def dispatch(a):
    root = a.root.resolve()
    if not root.is_dir():
        raise ValueError("Textura root does not exist")
    from storage import read_json, require_record
    import maintenance
    command = a.command
    if command == "status":
        settings = read_json(root/"Configuration/current/settings.json")
        return {"system": "Textura", "release": settings["release"], "root": str(root),
                "components": maintenance.registry(root), "automatic_model_calls": False,
                "entry": "Governance/current/README.md", "audit_owner": "Quality/current/records/audits"}
    if command == "doctor":
        from readers import capabilities
        from library_bridge import node_binary, configured_library
        settings = read_json(root/"Configuration/current/settings.json")
        library = configured_library(settings)
        node = None
        if library is not None:
            try:
                node = node_binary()
            except ValueError:
                pass
        return {"python": sys.version.split()[0], "python_executable": sys.executable,
                "reading": capabilities(), "node": node,
                "bibliotheca_configured": library is not None,
                "bibliotheca_entry_available": library is not None and (library/"tools/bm.mjs").is_file() and (library/"AGENTS.md").is_file(),
                "network_tested": False, "accounts_tested": False, "models_executed": False}
    if command == "validate":
        return maintenance.validate(root)
    if command in {"topic", "work", "object", "series", "source"}:
        settings = read_json(root/"Configuration/current/settings.json")
        a.policy = a.policy or settings.get("default_processing_policy", "local_only")
        if a.policy not in {"local_only", "cloud_allowed"}:
            raise ValueError("Invalid default_processing_policy")
    if command in {"topic", "work", "object", "series"}:
        from topics import create
        return create(root, command, a.title, topic_id=a.topic_id, language=a.language, genre=a.genre, processing_policy=a.policy)
    if command == "source":
        from sources import register
        return register(root, title=a.title, file=a.file, url=a.url, scope=a.scope, processing_policy=a.policy)
    if command == "read":
        from sources import read_source
        return read_source(root, a.source_id)
    if command == "draft":
        from writing import import_draft
        return import_draft(root, a.work_id, a.file)
    if command == "claim":
        from evidence import claim
        return claim(root, a.statement, work_id=a.work_id, topic_id=a.topic_id, kind=a.kind, priority=a.priority, supersedes=a.supersedes)
    if command == "assess":
        from evidence import assess
        refs = read_json(a.evidence_file) if a.evidence_file else []
        if not isinstance(refs, list) or not all(isinstance(r, dict) for r in refs):
            raise ValueError("Evidence file must contain a JSON array of reference objects")
        return assess(root, a.claim_id, a.verdict, a.rationale, refs, assessor=a.assessor, supersedes=a.supersedes)
    if command == "review":
        import review
        if a.action == "prepare":
            work = require_record(root, "Topics", "work", a.work_id)
            blind = a.blind or work.get("genre", "").lower() in {"poetry", "poem", "free_verse", "free-verse"}
            return review.prepare(root, a.work_id, poetry_blind=blind)
        if a.action == "advance":
            return review.advance(root, a.run_id, a.recognition_file, a.challenge_file)
        return review.status(root, a.run_id)
    if command == "decision":
        from state_records import decision
        return decision(root, a.kind, a.text, work_id=a.work_id, basis=a.basis)
    if command == "handoff":
        from state_records import handoff
        return handoff(root, a.work_id)
    if command == "snapshot":
        return maintenance.snapshot(root, a.component, a.reason)
    if command == "seal":
        return maintenance.seal(root, a.component)
    if command == "bm":
        from library_bridge import run
        return run(root, a.action, a.value, version=a.version, file=a.file, extraction=a.extraction, line=a.line)
    raise ValueError("Unsupported command")

def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    try:
        result = dispatch(args)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if args.command == "validate" and not result["valid"] else 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(json.dumps({"error": str(exc), "command": args.command}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
