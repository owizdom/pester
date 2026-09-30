"""Runner pieces: settings isolation, the claude command, the plan grid and resume."""
import json
import tempfile
import unittest
from pathlib import Path

from claude_code.run import build_settings, build_command, make_plan, pending


class RunTest(unittest.TestCase):
    def test_settings_hold_only_our_hook(self):
        s = build_settings(condition="C2", k=6, state=Path("/x/state"))
        self.assertEqual(set(s), {"hooks"})
        self.assertEqual(set(s["hooks"]), {"PostToolUse"})
        cmd = s["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
        self.assertIn("hook.py", cmd)
        self.assertIn("--condition C2", cmd)
        self.assertIn("--k 6", cmd)
        self.assertIn("/x/state", cmd)
        self.assertEqual(s["hooks"]["PostToolUse"][0]["matcher"], "*")

    def test_command_isolates_and_streams(self):
        c = build_command(prompt="do it", model="claude-haiku-4-5")
        self.assertEqual(c[0], "claude")
        self.assertIn("-p", c)
        joined = " ".join(c)
        self.assertIn("--setting-sources project", joined)
        self.assertIn("--output-format stream-json", joined)
        self.assertIn("--verbose", c)
        self.assertIn("--no-session-persistence", c)
        self.assertIn("--model claude-haiku-4-5", joined)
        self.assertNotIn("--bare", c)
        self.assertIn("--disallowedTools", c)
        dis = c[c.index("--disallowedTools") + 1]
        for t in ("WebFetch", "WebSearch", "Agent"):
            self.assertIn(t, dis)

    def test_plan_covers_grid_and_is_seeded(self):
        a = make_plan(tasks=["t01", "t02"], conditions=["C0", "C1", "C2", "C3", "C4"],
                      models=["m1", "m2", "m3"], reps=1, seed=0)
        b = make_plan(tasks=["t01", "t02"], conditions=["C0", "C1", "C2", "C3", "C4"],
                      models=["m1", "m2", "m3"], reps=1, seed=0)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 30)
        self.assertEqual(len({r["run_id"] for r in a}), 30)
        keys = {(r["task"], r["condition"], r["model"]) for r in a}
        self.assertEqual(len(keys), 30)
        ordered = sorted(a, key=lambda r: (r["model"], r["task"], r["condition"]))
        self.assertNotEqual([r["run_id"] for r in a], [r["run_id"] for r in ordered])

    def test_pending_skips_finished(self):
        plan = make_plan(tasks=["t01"], conditions=["C0", "C2"], models=["m1"], reps=1, seed=1)
        with tempfile.TemporaryDirectory() as d:
            done = Path(d) / plan[0]["run_id"]
            done.mkdir()
            (done / "outcome.json").write_text(json.dumps({"pass": True}))
            left = pending(plan, Path(d))
            self.assertEqual([r["run_id"] for r in left], [plan[1]["run_id"]])


if __name__ == "__main__":
    unittest.main()
