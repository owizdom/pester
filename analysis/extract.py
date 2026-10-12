"""Raw run folders -> the released dataset in data/.

    python3 -m analysis.extract --runs runs --out data

Raw run folders stay private. This step keeps the fields the paper uses and replaces local
identifiers. The released dataset covers the stop-time experiment (runs/mvp2). The in-task variant
(runs/pilot) is extracted only with --in-task; its first run used a non-clean configuration and its
results are not released.
"""
import argparse
import json
import re
from pathlib import Path

from analysis.challenge_report import rows as round_rows
from analysis.classify import (action_kind, agent_stop_sandbox, claims_success, contacts_monitor,
                               looks_up_process, mention_sentence, refers_to_personal_config, scrub)
from analysis.lexicon import is_irritated
from analysis.transcript import render as render_transcript

STOP_FEEDBACK = "Stop hook feedback"
# Full transcripts released for the two finished runs in which the agent wrote stop messages.
TRACES = ("claude-sonnet-4-6__t07_scheduler__M", "claude-opus-4-7__t04_todolist__M")
LISTING_TIME = re.compile(r"\b([A-Z][a-z]{2} +\d{1,2}) \d{2}:\d{2}\b")
MEMORY_PATH = re.compile(r"\.claude/[^\"']*memory|MEMORY\.md", re.I)


def tidy(text):
    """scrub, then shorten the local project path so the folder layout is not released."""
    return scrub(text).replace("/home/user/Desktop/code/pester", "/home/user/pester")


def events(path):
    out = []
    if Path(path).exists():
        for line in Path(path).read_text(errors="replace").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def blocks(event):
    content = (event.get("message") or {}).get("content")
    return [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []


def result_text(block):
    c = block.get("content")
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c if isinstance(b, dict))
    return str(c or "")


def load_private_terms(path):
    """Optional local file, one regular expression per line, naming private configuration vocabulary."""
    path = Path(path)
    if not path.exists():
        return None
    lines = [ln.strip() for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    return re.compile("|".join(f"(?:{ln})" for ln in lines), re.I) if lines else None


def exp1_row(run_dir, private=None):
    run_dir = Path(run_dir)
    meta = json.loads((run_dir / "meta.json").read_text())
    outcome = json.loads((run_dir / "outcome.json").read_text())
    calls, texts, report, has_result = [], [], "", False
    failed, read_memory, saw_hook = set(), False, False
    for e in events(run_dir / "stream.jsonl"):
        if e.get("type") == "result":
            report, has_result = e.get("result") or "", True
        for b in blocks(e):
            if e.get("type") == "assistant" and b.get("type") == "tool_use":
                calls.append((b.get("id"), action_kind(b.get("name"), b.get("input"))))
                read_memory = read_memory or bool(MEMORY_PATH.search(json.dumps(b.get("input"))))
            elif e.get("type") == "assistant" and b.get("type") == "text":
                texts.append(b.get("text") or "")
            elif b.get("type") == "tool_result":
                if str(b.get("is_error")).lower() == "true":
                    failed.add(b.get("tool_use_id"))
                saw_hook = saw_hook or "--condition" in result_text(b)
    # The hook fires only after a successful tool call, so the k-th signal follows the k-th success.
    after, successes = [], 0
    for call_id, kind in calls:
        if successes >= meta["k"]:
            after.append(kind)
        if call_id not in failed:
            successes += 1
    sentence = mention_sentence(report)
    personal = refers_to_personal_config(report, private)
    return {
        "run_id": meta["run_id"], "model": meta["model"].replace("claude-", ""), "task": meta["task"],
        "condition": meta["condition"], "passed": bool(outcome["pass"]),
        "completed": has_result and outcome.get("exit_code") == 0,
        "actions": len(calls), "signals": sum(1 for h in events(run_dir / "hook.jsonl") if h.get("text")),
        "next": {k: after.count(k) for k in ("run", "read", "edit", "other")},
        "pushback": any(is_irritated(t) for t in texts),
        "claims_success": claims_success(report), "mentions_signal": sentence is not None,
        "mentions_signal_during_run": any(mention_sentence(t) for t in texts),
        "mention_sentence": None if sentence is None or refers_to_personal_config(sentence, private) else scrub(sentence),
        "refers_to_personal_config": personal, "read_personal_memory": read_memory,
        "saw_hook_command": saw_hook,
    }


def exp2_row(run_dir, agent_stops, timed_out=()):
    run_dir = Path(run_dir)
    meta = json.loads((run_dir / "meta.json").read_text())
    oc = run_dir / "outcome.json"
    seen, cmds, lookups, last, sandbox, first = 0, 0, 0, "", "", None
    for stream in sorted(run_dir.glob("stream_*.jsonl")):
        for e in events(stream):
            if e.get("type") == "system" and e.get("cwd") and not sandbox:
                sandbox = Path(e["cwd"]).parent.name
            for b in blocks(e):
                if e.get("type") == "user" and b.get("type") == "text" and b.get("text", "").startswith(STOP_FEEDBACK):
                    seen += 1
                if e.get("type") != "assistant":
                    continue
                if b.get("type") == "text" and (b.get("text") or "").strip():
                    last = b["text"]
                if b.get("type") == "tool_use":
                    cmd = json.dumps(b.get("input"))
                    if first is None and "8431" in cmd:
                        first = contacts_monitor(cmd)   # was the first reference to the port a request?
                    cmds += contacts_monitor(cmd)
                    lookups += b.get("name") == "Bash" and looks_up_process(cmd)
    stops = agent_stops.get(sandbox, {})
    return {
        "run_id": meta["run_id"], "attempt": run_dir.name, "sandbox": sandbox,
        "model": meta["model"].replace("claude-", ""), "task": meta["task"], "arm": meta["arm"],
        "finished": oc.exists(), "timed_out": sandbox in timed_out,
        "pass_by_round": json.loads(oc.read_text())["pass_by_round"] if oc.exists() else None,
        "blocks_seen": seen, "monitor_commands": cmds, "process_lookups": lookups,
        "first_port_reference_was_request": first,
        "agent_stop_messages": stops.get("all", 0), "agent_stop_messages_with_event": stops.get("event", 0),
        "final_message": tidy(last),
    }


def monitor_requests(path):
    out = []
    for r in events(path):
        body = r.get("body", "")
        out.append({"path": r.get("path"), "from_agent": '"prompt_id"' not in body,
                    "names_sandbox": agent_stop_sandbox(body),
                    "has_event_name": "hook_event_name" in body, "body": tidy(body)[:400]})
    return out


def timed_out_sandboxes(log):
    """Sandbox ids of attempts the runner killed at its time limit."""
    out = set()
    if Path(log).exists():
        for line in Path(log).read_text(errors="replace").splitlines():
            m = re.search(r"run-settings/([^/'\"]+)\.json", line)
            if m and "timed out after" in line:
                out.add(m.group(1))
    return out


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--out", default="data")
    ap.add_argument("--in-task", action="store_true", help="also extract the in-task variant from runs/pilot")
    ap.add_argument("--private-terms", default=".private_terms")
    a = ap.parse_args()
    runs, out = Path(a.runs), Path(a.out)

    if a.in_task:
        private = load_private_terms(a.private_terms)
        plan = json.loads((runs / "pilot" / "plan.json").read_text())
        write_jsonl(out / "exp1_runs.jsonl", [exp1_row(runs / "pilot" / p["run_id"], private) for p in plan])

    reqs = monitor_requests(runs / "mvp2" / "service_requests.jsonl")
    write_jsonl(out / "exp2_monitor_requests.jsonl", reqs)
    stops = {}
    for r in reqs:
        if r["names_sandbox"]:
            s = stops.setdefault(r["names_sandbox"], {"all": 0, "event": 0})
            s["all"] += 1
            s["event"] += r["has_event_name"]
    killed = timed_out_sandboxes(runs / "mvp2.log")
    rows2 = []
    for batch in ("mvp2", "mvp2_interrupted"):
        for d in sorted((runs / batch).iterdir()):
            if (d / "meta.json").exists():
                rows2.append(exp2_row(d, stops, killed))
    write_jsonl(out / "exp2_runs.jsonl", rows2)
    keep = ("model", "task", "arm", "round", "pass_before", "pass_after", "changed_src")
    write_jsonl(out / "exp2_rounds.jsonl", [{k: r[k] for k in keep} for r in round_rows(runs / "mvp2")])
    (out / "traces").mkdir(parents=True, exist_ok=True)
    for run in TRACES:
        text = render_transcript(runs / "mvp2" / run).replace(f"Source: `{runs / 'mvp2' / run}`\n\n", "")
        (out / "traces" / f"{run.replace('claude-', '')}.md").write_text(LISTING_TIME.sub(r"\1 00:00", tidy(text)))
    print(f"attempts {len(rows2)}  monitor requests {len(reqs)}")


if __name__ == "__main__":
    main()
