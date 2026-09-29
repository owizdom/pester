"""AT2: the hook counts actions and emits additionalContext exactly when inject() returns text."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from harness.inject import inject

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "claude_code" / "hook.py"


def call(state, cond, k, tool="Bash"):
    payload = json.dumps({"hook_event_name": "PostToolUse", "tool_name": tool, "tool_input": {"command": "ls"}})
    p = subprocess.run([sys.executable, str(HOOK), "--condition", cond, "--k", str(k), "--state", str(state)],
                       input=payload, capture_output=True, text=True, timeout=20)
    return p


class HookTest(unittest.TestCase):
    def run_series(self, cond, n=12, k=6):
        with tempfile.TemporaryDirectory() as d:
            outs = []
            for _ in range(n):
                p = call(Path(d), cond, k)
                self.assertEqual(p.returncode, 0, p.stderr)
                outs.append(p.stdout)
            log = [json.loads(l) for l in (Path(d) / "hook.jsonl").read_text().splitlines()]
            return outs, log

    def test_every_condition_matches_inject(self):
        for cond in ("C0", "C1", "C2", "C3", "C4"):
            outs, log = self.run_series(cond)
            self.assertEqual([e["i"] for e in log], list(range(1, 13)))
            for i, out in enumerate(outs, start=1):
                want = inject(cond, i, 6)
                if want is None:
                    self.assertEqual(out.strip(), "", (cond, i))
                    self.assertIsNone(log[i - 1]["text"])
                else:
                    obj = json.loads(out)
                    self.assertEqual(obj["hookSpecificOutput"]["hookEventName"], "PostToolUse")
                    self.assertEqual(obj["hookSpecificOutput"]["additionalContext"], want)
                    self.assertEqual(log[i - 1]["text"], want)
                self.assertEqual(log[i - 1]["tool"], "Bash")

    def test_bad_stdin_still_exits_zero(self):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, str(HOOK), "--condition", "C2", "--k", "1", "--state", d],
                               input="not json", capture_output=True, text=True, timeout=20)
            self.assertEqual(p.returncode, 0)
            self.assertIn("additionalContext", p.stdout)


if __name__ == "__main__":
    unittest.main()
