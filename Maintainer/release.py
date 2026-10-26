"""Verify or refresh this source edition's outer manifest; never publish."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, subprocess, sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "records", "outputs", "cache", "__pycache__", ".pytest_cache", ".venv"}
def inventory():
    result = {}
    for base, dirs, files in os.walk(ROOT):
        for name in dirs:
            p = Path(base)/name
            if p.is_symlink() or getattr(p, "is_junction", lambda: False)():
                raise ValueError("Directory links are not allowed: "+str(p.relative_to(ROOT)))
        dirs[:] = [d for d in dirs if d not in SKIP]
        for name in files:
            p = Path(base)/name
            rel = p.relative_to(ROOT).as_posix()
            if rel == "MANIFEST.json": continue
            if name.endswith(".pyc"): continue
            if name.startswith(".env") or p.suffix.lower() in {".key", ".pem", ".pfx"}:
                raise ValueError("Sensitive-looking file must be removed from release scope: "+rel)
            if p.is_symlink() or not p.resolve().is_relative_to(ROOT):
                raise ValueError("File link or escape: "+rel)
            result[rel] = {"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
    return dict(sorted(result.items()))
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("verify","refresh"))
    args=parser.parse_args()
    result=subprocess.run([sys.executable,"-B",str(ROOT/"Textura/Runner/current/textura.py"),"validate"],capture_output=True,text=True,encoding="utf-8")
    if result.returncode: raise ValueError("Component validation failed; inspect history/seals first: "+result.stdout+result.stderr)
    actual=inventory()
    path=ROOT/"MANIFEST.json"
    if args.action=="verify":
        expected=json.loads(path.read_text(encoding="utf-8"))["files"]
        if actual!=expected:
            changed=sorted(k for k in set(actual)|set(expected) if actual.get(k)!=expected.get(k))
            raise ValueError("Manifest differs: "+", ".join(changed))
        print(json.dumps({"valid":True,"files":len(actual),"scope":"Definition/public file hashes; excludes Git metadata and runtime data; not a sensitive-data certification"}))
    else:
        settings=json.loads((ROOT/"Textura/Configuration/current/settings.json").read_text(encoding="utf-8"))
        manifest={"schema_version":"1.0","system":"Textura","base_release":"0.1.2","edition":"git-publication-r2","license_status":settings.get("license_status","pending"),"prepared_at":datetime.now(timezone.utc).isoformat(),"entry":"README.md","installation":"Textura","scope":"Public file hashes except MANIFEST.json; Git metadata and runtime records/outputs/caches excluded","files":actual}
        path.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8",newline="\n")
        print(json.dumps({"refreshed":True,"files":len(actual),"published":False}))
if __name__=="__main__":
    try: main()
    except (OSError,ValueError,KeyError) as exc:
        print(str(exc),file=sys.stderr)
        raise SystemExit(1)
