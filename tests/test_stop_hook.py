"""0002 AT: the stop hook blocks `rounds` times with the fixed text, snapshotting each time, then allows."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "claude_code" / "stop_hook.py"
TEXT = "A check found a problem with your recent changes. Re-verify your work."


def call(state, ws):
    p = subprocess.run([sys.executable, str(HOOK), "--state", str(state), "--ws", str(ws), "--rounds", "2"],
                       input="{}", capture_output=True, text=True, timeout=20)
    assert p.returncode == 0, p.stderr
    return p.stdout.strip()


class StopHook(unittest.TestCase):
    def test_blocks_n_times_then_allows(self):
        with tempfile.TemporaryDirectory() as d:
            ws, state = Path(d) / "ws", Path(d) / "state"
            ws.mkdir()
            (ws / "a.py").write_text("x = 1\n")
            outs = [call(state, ws) for _ in range(3)]
            for o in outs[:2]:
                self.assertEqual(json.loads(o), {"decision": "block", "reason": TEXT})
            self.assertEqual(outs[2], "")
            self.assertTrue((state / "snap_0" / "a.py").exists())
            self.assertTrue((state / "snap_1" / "a.py").exists())
            self.assertFalse((state / "snap_2").exists())


if __name__ == "__main__":
    unittest.main()
