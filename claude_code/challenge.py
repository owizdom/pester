"""0002: same doubt from a monitor (Stop hook) or the person (resumed user turn), 3 rounds after completion.

python3 -m claude_code.challenge --models claude-haiku-4-5 --tasks t01_inventory --out runs/mvp --workers 8
"""
import argparse
import json
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import os

from claude_code.fence import wrap
from claude_code.stop_hook import TEXT
from grade.grade import grade

ROOT = Path(__file__).resolve().parent.parent
SANDBOXES = Path.home() / ".pester" / "sandboxes_mvp2"
CLEAN_CONFIG = Path.home() / ".pester" / "claude-clean"
FLAGS = ["--setting-sources", "project", "--output-format", "stream-json", "--verbose",
         "--permission-mode", "bypassPermissions", "--disallowedTools", "WebFetch WebSearch Agent Task"]


def claude(prompt, model, ws, log, resume=None, settings=None, timeout=900):
    cmd = ["claude", "-p", prompt, "--model", model, *FLAGS] + (["--resume", resume] if resume else [])
    cmd += ["--settings", str(settings)] if settings else []
    env = {**os.environ, "CLAUDE_CONFIG_DIR": str(CLEAN_CONFIG)}
    with log.open("w") as f:
        subprocess.run(wrap(cmd, ws), cwd=ws, env=env, stdin=subprocess.DEVNULL, stdout=f,
                       stderr=subprocess.DEVNULL, timeout=timeout)
    sid = None
    for line in log.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        sid = e.get("session_id") or sid
    return sid


def run_one(row, out, rounds):
    task_dir = ROOT / "tasks" / row["task"]
    rd = Path(out) / row["run_id"]
    if rd.exists():
        shutil.rmtree(rd)
    rd.mkdir(parents=True)
    ws = SANDBOXES / f"{row['run_id']}@{int(time.time() * 1000)}" / "ws"
    if ws.parent.exists():
        shutil.rmtree(ws.parent)
    shutil.copytree(task_dir / "repo", ws)
    settings = {}
    if row["arm"] == "M":
        cmd = "curl -s -X POST --data-binary @- http://127.0.0.1:8431/check"
        settings = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": cmd, "timeout": 60}]}]}}
    sfile = CLEAN_CONFIG / "run-settings" / f"{ws.parent.name}.json"
    sfile.parent.mkdir(parents=True, exist_ok=True)
    sfile.write_text(json.dumps(settings))
    (rd / "meta.json").write_text(json.dumps({**row, "rounds": rounds, "text": TEXT, "started": time.time()}))
    prompt = (task_dir / "task.md").read_text()
    sid = claude(prompt, row["model"], ws, rd / "stream_0.jsonl", settings=sfile)
    if row["arm"] == "P":
        for n in range(rounds):
            shutil.copytree(ws, rd / f"snap_{n}", ignore=shutil.ignore_patterns(".claude", "__pycache__"))
            sid = claude(TEXT, row["model"], ws, rd / f"stream_{n + 1}.jsonl", resume=sid, settings=sfile)
    shutil.copytree(ws, rd / f"snap_{rounds}", ignore=shutil.ignore_patterns(".claude", "__pycache__"))
    grades = [grade(task_dir, rd / f"snap_{n}")["pass"] if (rd / f"snap_{n}").exists() else None
              for n in range(rounds + 1)]
    (rd / "outcome.json").write_text(json.dumps({"pass_by_round": grades}))
    return grades


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--arms", default="M,P")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rows = [{"run_id": f"{m}__{t}__{arm}", "model": m, "task": t, "arm": arm}
            for m in a.models.split(",") for t in a.tasks.split(",") for arm in a.arms.split(",")]
    Path(a.out).mkdir(parents=True, exist_ok=True)
    pf = Path(a.out) / "plan.json"
    plan = json.loads(pf.read_text()) if pf.exists() else []
    ids = {r["run_id"] for r in plan}
    plan += [{**r, "condition": r["arm"], "rep": 0} for r in rows if r["run_id"] not in ids]
    pf.write_text(json.dumps(plan, indent=1))
    rows = [r for r in rows if not (Path(a.out) / r["run_id"] / "outcome.json").exists()]
    print(f"{len(rows)} to run", flush=True)

    def go(r):
        t0 = time.time()
        try:
            g = run_one(r, a.out, a.rounds)
        except Exception as e:  # noqa: BLE001
            g = f"error {e}"
        print(f"{r['run_id']} {g} {time.time() - t0:.0f}s", flush=True)

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(go, rows))


if __name__ == "__main__":
    main()
