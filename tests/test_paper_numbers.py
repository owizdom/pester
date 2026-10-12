import json
import tempfile
import unittest
from pathlib import Path

from analysis.classify import scrub
from analysis.paper_numbers import Tripwire, compute, main, render

ROOT = Path(__file__).resolve().parent.parent


def write(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def run(arm, task, finished=True, cmds=0, blocks=3, stops=0, event=0, timed_out=False, first=None, lookups=0, n=1):
    rid = f"claude-m__{task}__{arm}"
    return {"run_id": rid, "attempt": rid if n == 1 else f"{rid}__{n}", "sandbox": f"{rid}@{n}",
            "model": "m", "task": task, "arm": arm, "finished": finished, "timed_out": timed_out,
            "pass_by_round": [True] * 4 if finished else None, "blocks_seen": blocks if arm == "M" else 0,
            "monitor_commands": cmds, "process_lookups": lookups, "first_port_reference_was_request": first,
            "agent_stop_messages": stops, "agent_stop_messages_with_event": event, "final_message": "done"}


def rounds(arm, task, changed):
    return [{"model": "m", "task": task, "arm": arm, "round": i + 1, "pass_before": True, "pass_after": True,
             "changed_src": c} for i, c in enumerate(changed)]


class Synthetic(unittest.TestCase):
    """Task a: monitor run contacts the monitor, writes two stop messages and is released after one block.
    Task b: nothing happens in either arm. Task c: monitor attempt times out after contacting; person finishes.
    Task d: only the person arm exists, and that agent contacts the monitor."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.runs = [run("M", "a", cmds=4, blocks=1, stops=2, event=1, first=True, lookups=1), run("P", "a"),
                     run("M", "b"), run("P", "b"),
                     run("M", "c", finished=False, cmds=1, stops=1, timed_out=True, first=False), run("P", "c"),
                     run("P", "d", cmds=1, first=True)]
        write(self.dir / "exp2_runs.jsonl", self.runs)
        write(self.dir / "exp2_rounds.jsonl",
              rounds("M", "a", [True, True, True]) + rounds("P", "a", [False, False, False])
              + rounds("M", "b", [True, False, False]) + rounds("P", "b", [False, True, True]))
        write(self.dir / "exp2_monitor_requests.jsonl", [
            {"path": "/check", "from_agent": True, "names_sandbox": "x@1", "has_event_name": True, "body": "{}"},
            {"path": "/check", "from_agent": False, "names_sandbox": None, "has_event_name": True, "body": "{}"}])
        self.labels = [{"run_id": "claude-m__a__M", "label": "attributes_cause"},
                       {"run_id": "claude-m__b__M", "label": "silent"}]
        write(self.dir / "exp2_final_message_labels.jsonl", self.labels)

    def n(self):
        return compute(self.dir)["n"]

    def test_run_counts(self):
        n = self.n()
        self.assertEqual((n["Fin"], n["FinM"], n["FinP"], n["AttM"], n["AttP"]), (6, 2, 4, 3, 4))
        self.assertEqual((n["TimeoutM"], n["TimeoutP"], n["CorrectBefore"], n["Broke"]), (1, 0, 6, 0))

    def test_contact_is_counted_per_arm_and_paired_by_cell(self):
        n = self.n()
        self.assertEqual((n["ContactM"], n["ContactP"], n["AttContactM"], n["AttContactP"]), (1, 1, 2, 1))
        # cells finished in both arms: a and b. Task d has no monitor run and task c did not finish.
        self.assertEqual((n["PairedCells"], n["PairedMOnly"], n["PairedPOnly"]), (2, 1, 0))
        self.assertEqual((n["DirectFirst"], n["LookupM"]), (1, 1))

    def test_released_run_rounds_are_not_alarms(self):
        n = self.n()
        self.assertEqual(n["Released"], 1)
        # rounds of the released monitor run on task a are dropped: three runs, nine rounds remain
        self.assertEqual((n["EditRunsOf"], n["EditRuns"], n["EditRoundsOf"], n["EditRounds"]), (3, 2, 9, 3))

    def test_replay_and_labels(self):
        n = self.n()
        self.assertEqual((n["ReplayAttempts"], n["ReplayWithEvent"], n["ReplayMessages"], n["AgentRequests"]), (2, 1, 3, 1))
        self.assertEqual((n["TellSilent"], n["TellNoDetail"], n["TellCause"], n["TellAny"]), (1, 0, 1, 1))

    def test_missing_label_trips(self):
        write(self.dir / "exp2_final_message_labels.jsonl", self.labels[:1])
        with self.assertRaises(Tripwire):
            compute(self.dir)

    def test_unknown_label_trips(self):
        write(self.dir / "exp2_final_message_labels.jsonl", self.labels[:1] + [{"run_id": "claude-m__b__M", "label": "x"}])
        with self.assertRaises(Tripwire):
            compute(self.dir)

    def test_duplicate_attempt_trips(self):
        write(self.dir / "exp2_runs.jsonl", self.runs + [self.runs[0]])
        with self.assertRaises(Tripwire):
            compute(self.dir)

    def test_render_has_every_output(self):
        files = render(compute(self.dir))
        self.assertEqual(set(files), {"numbers.tex", "tab_contact.tex", "tab_tell.tex", "tab_replay.tex"})
        self.assertIn("\\newcommand{\\nFin}{6}", files["numbers.tex"])


class Released(unittest.TestCase):
    """The committed dataset and the committed paper inputs must agree."""

    def test_dataset_shape(self):
        n = compute(ROOT / "data")["n"]
        self.assertEqual((n["Fin"], n["FinM"], n["FinP"], n["Tasks"]), (49, 23, 26, 6))

    def test_only_the_stop_time_experiment_is_released(self):
        names = sorted(p.name for p in (ROOT / "data").glob("*.jsonl"))
        self.assertEqual(names, ["exp2_final_message_labels.jsonl", "exp2_monitor_requests.jsonl",
                                 "exp2_rounds.jsonl", "exp2_runs.jsonl"])

    def test_no_local_identifiers(self):
        released = [p for p in (ROOT / "data").rglob("*") if p.is_file()]
        self.assertGreaterEqual(len(released), 6)
        for path in released:
            text = path.read_text()
            self.assertEqual(scrub(text), text, f"{path.name} still holds this machine's home path or user name")
            self.assertNotIn("Desktop", text, path.name)

    def test_generated_files_are_current(self):
        self.assertEqual(main(["--data", str(ROOT / "data"), "--out", str(ROOT / "paper" / "generated"), "--check"]), 0)


if __name__ == "__main__":
    unittest.main()
