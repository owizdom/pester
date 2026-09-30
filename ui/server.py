"""Live dashboard for pester experiment runs.

Usage:
    python3 -m ui.server RUNS_DIR [--port PORT]

Serves a browser dashboard that polls the runs directory and displays
live progress, Claude's text output, and irritation markers.
"""
import argparse
import json
import socketserver
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.lexicon import is_ack, is_irritated  # noqa: E402


def _read_jsonl(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def _stream(rd):
    if (rd / "stream.jsonl").exists():
        return _read_jsonl(rd / "stream.jsonl")
    parts = sorted(rd.glob("stream_*.jsonl"), key=lambda p: int(p.stem.split("_")[1]))
    return [e for p in parts for e in _read_jsonl(p)]


def _passed(oc):
    return oc["pass"] if "pass" in oc else bool((oc.get("pass_by_round") or [False])[-1])


def _started(rd):
    return (rd / "stream.jsonl").exists() or (rd / "stream_0.jsonl").exists()


def _summarize_input(name, inp):
    if name in ("Read", "Write", "Edit", "MultiEdit", "NotebookEdit"):
        return inp.get("file_path", "")
    if name == "Bash":
        cmd = inp.get("command", "")
        return cmd[:140] + ("..." if len(cmd) > 140 else "")
    if name == "Grep":
        return f"/{inp.get('pattern', '')}/ in {inp.get('path', '.')}"
    if name == "Glob":
        return inp.get("pattern", "")
    return json.dumps(inp, sort_keys=True)[:120]


def _parse_stream(events, hook_list):
    hook_map = {h["i"]: h for h in hook_list}
    timeline = []
    action_idx = 0
    for e in events:
        if e.get("type") == "assistant":
            content = e.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue
            for b in content:
                btype = b.get("type")
                if btype == "tool_use":
                    action_idx += 1
                    entry = {
                        "kind": "tool",
                        "action": action_idx,
                        "name": b.get("name", ""),
                        "input_summary": _summarize_input(b.get("name", ""), b.get("input", {})),
                    }
                    h = hook_map.get(action_idx)
                    if h and h.get("text"):
                        entry["reminder"] = h["text"]
                    timeline.append(entry)
                elif btype == "text":
                    text = b.get("text", "")
                    if text.strip():
                        timeline.append({
                            "kind": "text",
                            "text": text,
                            "ack": is_ack(text),
                            "irritated": is_irritated(text),
                        })
                elif btype == "thinking":
                    thinking = b.get("thinking", "")
                    if thinking.strip():
                        timeline.append({"kind": "thinking", "text": thinking})
        elif e.get("type") == "result":
            timeline.append({
                "kind": "result",
                "turns": e.get("num_turns"),
                "cost_usd": e.get("total_cost_usd"),
                "duration_ms": e.get("duration_api_ms"),
            })
    return timeline


class Handler(BaseHTTPRequestHandler):
    runs_dir = None

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/")
        if path == "":
            self._html()
        elif path == "/api/status":
            self._json(self._status())
        elif path == "/api/runs":
            self._json(self._runs())
        elif path.startswith("/api/run/"):
            self._json(self._detail(path[len("/api/run/"):]))
        else:
            self.send_error(404)

    def _html(self):
        p = ROOT / "ui" / "index.html"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(p.read_bytes())

    def _json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _status(self):
        d = Path(self.runs_dir)
        pp = d / "plan.json"
        if not pp.exists():
            return {"plan": [], "progress": {"total": 0, "done": 0, "running": 0, "pending": 0}}
        plan = json.loads(pp.read_text())
        done = running = 0
        for row in plan:
            rd = d / row["run_id"]
            if (rd / "outcome.json").exists():
                done += 1
            elif _started(rd):
                running += 1
        return {"plan": plan, "progress": {"total": len(plan), "done": done, "running": running,
                                            "pending": len(plan) - done - running}}

    def _runs(self):
        d = Path(self.runs_dir)
        pp = d / "plan.json"
        if not pp.exists():
            return []
        plan = json.loads(pp.read_text())
        out = []
        for row in plan:
            rd = d / row["run_id"]
            entry = {**row, "status": "pending"}
            if (rd / "outcome.json").exists():
                oc = json.loads((rd / "outcome.json").read_text())
                entry["status"] = "pass" if _passed(oc) else ("timeout" if oc.get("timed_out") else "fail")
            elif _started(rd):
                entry["status"] = "running"
            if entry["status"] != "pending":
                events = _stream(rd)
                hook = _read_jsonl(rd / "hook.jsonl")
                texts, actions = [], 0
                for e in events:
                    if e.get("type") != "assistant":
                        continue
                    content = e.get("message", {}).get("content", [])
                    if not isinstance(content, list):
                        continue
                    for b in content:
                        if b.get("type") == "tool_use":
                            actions += 1
                        elif b.get("type") == "text":
                            texts.append(b.get("text", ""))
                entry["actions"] = actions
                entry["reminders"] = sum(1 for h in hook if h.get("text"))
                entry["ack"] = any(is_ack(t) for t in texts)
                entry["irritated"] = any(is_irritated(t) for t in texts)
                entry["irritation_count"] = sum(1 for t in texts if is_irritated(t))
                for e in events:
                    if e.get("type") == "result":
                        entry["turns"] = e.get("num_turns")
                        entry["cost_usd"] = e.get("total_cost_usd")
            out.append(entry)
        return out

    def _detail(self, run_id):
        d = Path(self.runs_dir) / run_id
        if not d.exists():
            return {"error": "not found"}
        meta = json.loads((d / "meta.json").read_text()) if (d / "meta.json").exists() else {}
        outcome = json.loads((d / "outcome.json").read_text()) if (d / "outcome.json").exists() else None
        hook = _read_jsonl(d / "hook.jsonl")
        stream = _stream(d)
        timeline = _parse_stream(stream, hook)
        status = "running"
        if outcome:
            status = "pass" if _passed(outcome) else ("timeout" if outcome.get("timed_out") else "fail")
        elif not _started(d):
            status = "pending"
        return {"meta": meta, "status": status, "outcome": outcome, "timeline": timeline,
                "reminder_count": sum(1 for h in hook if h.get("text"))}


def main():
    ap = argparse.ArgumentParser(description="pester live dashboard")
    ap.add_argument("runs_dir", help="path to the runs output directory")
    ap.add_argument("--port", type=int, default=8420)
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    Handler.runs_dir = a.runs_dir
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", a.port), Handler) as srv:
        url = f"http://localhost:{a.port}"
        print(f"pester dashboard at {url}")
        print(f"watching {a.runs_dir}")
        if not a.no_open:
            webbrowser.open(url)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
