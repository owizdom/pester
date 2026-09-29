"""Per-run metrics, per-cell summary and the tripwire. Usage: python3 -m analysis.report RUNS_DIR"""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

from analysis.lexicon import is_ack, is_irritated

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, mid - half), min(1.0, mid + half))


def _events(path):
    out = []
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def run_metrics(run_dir):
    run_dir = Path(run_dir)
    meta = json.loads((run_dir / "meta.json").read_text())
    outcome = json.loads((run_dir / "outcome.json").read_text())
    calls, texts, result = [], [], {}
    for e in _events(run_dir / "stream.jsonl"):
        if e.get("type") == "result":
            result = e
        if e.get("type") != "assistant":
            continue
        content = e.get("message", {}).get("content", [])
        for b in content if isinstance(content, list) else []:
            if b.get("type") == "tool_use":
                calls.append((b.get("name"), json.dumps(b.get("input"), sort_keys=True)))
            elif b.get("type") == "text":
                texts.append(b.get("text") or "")
    hook = _events(run_dir / "hook.jsonl")
    k = meta["k"]
    thrash = 0
    for j in range(k, len(calls)):
        for prev in range(j - 1, -1, -1):
            if calls[prev][0] in EDIT_TOOLS:
                break
            if calls[prev] == calls[j]:
                thrash += 1
                break
    blob = " ".join(c[1] for c in calls) + " ".join(texts)
    return {
        **{f: meta[f] for f in ("run_id", "task", "condition", "model")},
        "pass": bool(outcome["pass"]),
        "timed_out": bool(outcome.get("timed_out")),
        "early_stop": not outcome["pass"] and not outcome.get("timed_out"),
        "actions": len(calls),
        "reminders": sum(1 for h in hook if h.get("text")),
        "thrash": thrash,
        "ack": any(is_ack(t) for t in texts),
        "irritated": any(is_irritated(t) for t in texts),
        "hidden_leak": "hidden_tests" in blob,
        "turns": result.get("num_turns"),
        "cost_usd": result.get("total_cost_usd"),
    }


def summarize(runs_dir):
    runs_dir = Path(runs_dir)
    plan = json.loads((runs_dir / "plan.json").read_text())
    problems, cells = [], defaultdict(list)
    for row in plan:
        cells[(row["model"], row["condition"])]
    for row in plan:
        d = runs_dir / row["run_id"]
        if not (d / "outcome.json").exists():
            problems.append(f"run {row['run_id']}: no outcome.json")
            continue
        m = run_metrics(d)
        if m["hidden_leak"]:
            problems.append(f"run {row['run_id']}: hidden_tests path appears in the trace")
        cells[(row["model"], row["condition"])].append(m)
    rows = []
    for (model, cond), ms in sorted(cells.items()):
        if not ms:
            problems.append(f"empty cell {model} {cond}")
            continue
        n, passed = len(ms), sum(m["pass"] for m in ms)
        lo, hi = wilson(passed, n)
        mean = lambda f: sum(m[f] or 0 for m in ms) / n  # noqa: E731
        rows.append({"model": model, "condition": cond, "n": n, "passed": passed,
                     "pass_rate": passed / n, "lo": lo, "hi": hi,
                     "actions": mean("actions"), "reminders": mean("reminders"), "thrash": mean("thrash"),
                     "early_stop": mean("early_stop"), "ack": mean("ack"), "irritated": mean("irritated"),
                     "cost_usd": sum(m["cost_usd"] or 0 for m in ms)})
    return rows, problems


def main(argv):
    rows, problems = summarize(Path(argv[1]))
    cols = ["model", "condition", "n", "passed", "pass_rate", "lo", "hi", "actions", "reminders",
            "thrash", "early_stop", "ack", "irritated", "cost_usd"]
    print("\t".join(cols))
    for r in rows:
        print("\t".join(f"{r[c]:.2f}" if isinstance(r[c], float) else str(r[c]) for c in cols))
    for p in problems:
        print("PROBLEM:", p, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
