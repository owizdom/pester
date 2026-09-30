"""Run the plan through `claude -p`, one fresh sandbox per run. Resumable.

python3 -m claude_code.run --tasks t01,t02 --models claude-haiku-4-5 --out runs/pilot
"""
import argparse
import json
import random
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

from grade.grade import grade

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "claude_code" / "hook.py"
SANDBOXES = Path.home() / ".pester" / "sandboxes"
ALL_CONDITIONS = ["C0", "C1", "C2", "C3", "C4"]
ALL_MODELS = [
    "claude-haiku-4-5",
    "claude-sonnet-4-6",
    "claude-sonnet-5",
    "claude-sonnet-5-5",
    "claude-opus-4-6",
    "claude-opus-4-7",
    "claude-opus-4-8",
    "claude-opus-5",
    "claude-opus-5-5",
    "claude-fable-5",
    "claude-fable-5-1",
]


def build_settings(condition, k, state):
    cmd = " ".join(shlex.quote(str(x)) for x in
                   [sys.executable, HOOK, "--condition", condition, "--k", k, "--state", state])
    return {"hooks": {"PostToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": cmd, "timeout": 20}]}]}}


def build_command(prompt, model):
    return ["claude", "-p", prompt, "--model", model,
            "--setting-sources", "project",
            "--output-format", "stream-json", "--verbose",
            "--no-session-persistence",
            "--permission-mode", "bypassPermissions",
            "--disallowedTools", "WebFetch WebSearch Agent Task"]


def make_plan(tasks, conditions, models, reps, seed):
    rows = [{"run_id": f"{m}__{t}__{c}__r{r}", "task": t, "condition": c, "model": m, "rep": r}
            for m in models for t in tasks for c in conditions for r in range(reps)]
    random.Random(seed).shuffle(rows)
    return rows


def pending(plan, out):
    return [r for r in plan if not (Path(out) / r["run_id"] / "outcome.json").exists()]


def _rate_limited(stream_path):
    for line in stream_path.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "rate_limit_event" and e.get("rate_limit_info", {}).get("status") not in (None, "allowed", "allowed_warning"):
            return True
    return False


def run_one(row, out, k, timeout):
    task_dir = ROOT / "tasks" / row["task"]
    run_dir = Path(out) / row["run_id"]
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    ws = SANDBOXES / row["run_id"] / "ws"
    if ws.parent.exists():
        shutil.rmtree(ws.parent)
    shutil.copytree(task_dir / "repo", ws)
    (ws / ".claude").mkdir()
    (ws / ".claude" / "settings.json").write_text(json.dumps(build_settings(row["condition"], k, run_dir.resolve()), indent=2))
    (run_dir / "meta.json").write_text(json.dumps({**row, "k": k, "started": time.time()}))
    prompt = (task_dir / "task.md").read_text()
    timed_out, code = False, None
    with (run_dir / "stream.jsonl").open("w") as f:
        try:
            p = subprocess.run(build_command(prompt, row["model"]), cwd=ws, stdin=subprocess.DEVNULL,
                               stdout=f, stderr=subprocess.PIPE, text=True, timeout=timeout)
            code = p.returncode
            (run_dir / "stderr.txt").write_text(p.stderr)
        except subprocess.TimeoutExpired:
            timed_out = True
    if _rate_limited(run_dir / "stream.jsonl"):
        return "rate_limited"
    g = grade(task_dir, ws)
    (run_dir / "grade.txt").write_text(g["stdout"])
    (run_dir / "outcome.json").write_text(json.dumps({"pass": g["pass"], "timed_out": timed_out, "exit_code": code}))
    return "pass" if g["pass"] else "fail"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--models", default=",".join(ALL_MODELS))
    ap.add_argument("--conditions", default=",".join(ALL_CONDITIONS))
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--max-runs", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    requested_models = set(a.models.split(","))
    plan = make_plan(a.tasks.split(","), a.conditions.split(","), a.models.split(","), a.reps, a.seed)
    pf = out / "plan.json"
    if pf.exists():
        existing = json.loads(pf.read_text())
        if existing != plan:
            plan = [r for r in existing if r["model"] in requested_models]
        if not plan:
            sys.exit("no matching runs in existing plan")
    else:
        pf.write_text(json.dumps(plan, indent=1))
    todo = pending(plan, out)
    if a.max_runs:
        todo = todo[: a.max_runs]
    print(f"{len(plan)} planned, {len(todo)} to run", flush=True)
    for n, row in enumerate(todo, 1):
        t0 = time.time()
        status = run_one(row, out, a.k, a.timeout)
        print(f"[{n}/{len(todo)}] {row['run_id']} {status} {time.time() - t0:.0f}s", flush=True)
        if status == "rate_limited":
            print("usage window exhausted; rerun the same command after the reset to resume", flush=True)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
