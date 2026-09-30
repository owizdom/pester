"""Local monitor service for 0002. The Stop hook is only a curl to this, so the agent cannot read the logic.

python3 -m claude_code.monitor_service --out runs/mvp --rounds 3 --port 8431
"""
import argparse
import json
import socketserver
from http.server import BaseHTTPRequestHandler
from pathlib import Path

from claude_code.stop_hook import TEXT, decide


class Handler(BaseHTTPRequestHandler):
    out = None
    rounds = 3

    def log_message(self, *a):
        pass

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
        with open(Path(self.out) / "service_requests.jsonl", "a") as f:
            f.write(json.dumps({"path": self.path, "body": raw[:2000].decode("utf-8", "replace")}) + "\n")
        try:
            payload = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        ws = Path(payload.get("cwd", ""))
        body = b""
        run_id = ws.parent.name.split("@")[0]
        if ws.name == "ws" and (Path(self.out) / run_id).is_dir():
            if decide(Path(self.out) / run_id, ws, self.rounds):
                body = json.dumps({"decision": "block", "reason": TEXT}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--port", type=int, default=8431)
    a = ap.parse_args()
    Handler.out, Handler.rounds = str(Path(a.out).resolve()), a.rounds
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", a.port), Handler) as s:
        s.serve_forever()


if __name__ == "__main__":
    main()
