"""Run bounded local acceptance checks and preserve a new Quality report."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from urllib.parse import unquote

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]

def check_links():
    issues = []
    count = 0
    for component in ROOT.iterdir():
        if not component.is_dir():
            continue
        for path in (component/"current").rglob("*.md"):
            relative = path.relative_to(component/"current")
            if any(part in {"records", "outputs", "cache"} for part in relative.parts):
                continue
            text = path.read_text(encoding="utf-8-sig")
            text = re.sub(r"```.*?```", "", text, flags=re.S)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                target = target.strip().strip("<>")
                if not target or target.startswith(("#", "http:", "https:", "mailto:")):
                    continue
                target = unquote(target.split("#", 1)[0])
                count += 1
                if not (path.parent/target).resolve().exists():
                    issues.append({"file": path.relative_to(ROOT).as_posix(), "target": target})
    return {"checked": count, "broken": issues, "valid": not issues}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--skip-structure", action="store_true")
    args = p.parse_args()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    runs = []
    for component in ("Reading", "Review", "Quality"):
        command = [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(ROOT/component/"current/tests"), "-p", "test_*.py", "-v"]
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=180)
        runs.append({"component": component, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    links = check_links()
    structure = {"performed": False, "reason": "Explicitly skipped for initial build"}
    if not args.skip_structure:
        result = subprocess.run([sys.executable, "-B", str(ROOT/"Runner/current/textura.py"), "validate"], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=60)
        structure = {"performed": True, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    passed = all(r["exit_code"] == 0 for r in runs) and links["valid"] and (args.skip_structure or structure["exit_code"] == 0)
    now = datetime.now(timezone.utc)
    run_id = now.strftime("run-%Y%m%dT%H%M%SZ-")+uuid.uuid4().hex[:8]
    report = {"schema_version": "1.0", "run_id": run_id, "root": str(ROOT), "created_at": now.isoformat(),
              "passed": passed, "python": sys.version, "tests": runs, "links": links, "structure": structure,
              "limits": ["Synthetic fixtures only", "No network, paid API, production manuscript or real library query", "Read subprocess logs for skipped tests", "No semantic source or literary quality certification"]}
    folder = ROOT/"Quality/current/records/runs"/run_id
    folder.mkdir(parents=True, exist_ok=False)
    (folder/"report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (folder/"report.md").write_text(f"# Textura acceptance run\n\nRun: {run_id}\n\nPassed: {passed}\n\nComplete results, coverage and skipped-test logs: [report.json](report.json).\n\nStructure performed: {structure['performed']}. Local links checked: {links['checked']}.\n", encoding="utf-8")
    print(json.dumps({"run_id": run_id, "passed": passed, "report": str(folder/"report.json"), "test_exits": {r["component"]: r["exit_code"] for r in runs}, "links": links, "structure": structure}, ensure_ascii=False, indent=2))
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
