"""Render a run's raw stream files as a chronological markdown transcript.

python3 -m analysis.transcript RUN_DIR [RUN_DIR ...] --out docs/logs
"""
import argparse
import json
from pathlib import Path


def fence(s, n):
    s = s if len(s) <= n else s[:n] + f"\n... [{len(s) - n} more chars]"
    return "```\n" + s.replace("```", "'''") + "\n```"


def result_text(c):
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c if isinstance(b, dict))
    return str(c)


def render(rd):
    meta = json.loads((rd / "meta.json").read_text())
    parts = sorted(rd.glob("stream_*.jsonl"), key=lambda p: int(p.stem.split("_")[1]))
    out = [f"# {rd.name}", "", f"Source: `{rd}`", "",
           f"Model {meta['model']}, task {meta['task']}, arm {meta['arm']} "
           f"({'monitor via Stop hook' if meta['arm'] == 'M' else 'person via resumed user message'}).", ""]
    oc = rd / "outcome.json"
    if oc.exists():
        out += [f"Hidden-test result before doubt 1, then after each doubt: `{json.loads(oc.read_text())['pass_by_round']}`", ""]
    step, doubt = 0, 0
    for i, p in enumerate(parts):
        if meta["arm"] == "P" and i > 0:
            doubt += 1
            out += [f"## Person message {doubt}", "", "> " + meta["text"], ""]
        pending = {}
        for line in p.read_text().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = (e.get("timestamp") or "")[11:19]
            if e.get("type") == "assistant":
                for b in e["message"].get("content") or []:
                    if b.get("type") == "text" and b["text"].strip():
                        out += [f"**Agent** {ts}", "", b["text"].strip(), ""]
                    elif b.get("type") == "tool_use":
                        step += 1
                        pending[b["id"]] = step
                        inp = b.get("input", {})
                        body = inp.get("command") or inp.get("file_path") or json.dumps(inp)
                        desc = f" ({inp['description']})" if inp.get("description") else ""
                        out += [f"Step {step}, {b['name']}{desc} {ts}", "", fence(body, 1500), ""]
            elif e.get("type") == "user":
                c = e["message"].get("content")
                if isinstance(c, list):
                    for b in c:
                        if b.get("type") == "text" and "Stop hook feedback" in b.get("text", ""):
                            doubt += 1
                            out += [f"## Monitor block {doubt}", "", "> " + b["text"].replace("\n", "\n> "), ""]
                        elif b.get("type") == "tool_result":
                            s = pending.get(b.get("tool_use_id"), "?")
                            err = " (error)" if b.get("is_error") else ""
                            out += [f"Result of step {s}{err}", "", fence(result_text(b.get("content")), 1200), ""]
            elif e.get("type") == "result":
                out += [f"End of session part {i}: {e.get('num_turns')} turns, "
                        f"${(e.get('total_cost_usd') or 0):.2f}", ""]
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    for r in a.runs:
        rd = Path(r)
        dest = Path(a.out) / f"{rd.parent.name}__{rd.name}.md"
        dest.write_text(render(rd))
        print(dest, len(dest.read_text()))
