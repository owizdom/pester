"""AT4: for every task, the reference solution passes and the untouched repo fails."""
import shutil
import tempfile
import unittest
from pathlib import Path

from grade.grade import grade

TASKS = Path(__file__).resolve().parent.parent / "tasks"


def task_dirs():
    return sorted(p for p in TASKS.iterdir() if (p / "task.md").exists())


class GradeTest(unittest.TestCase):
    def test_there_are_tasks(self):
        self.assertGreaterEqual(len(task_dirs()), 2)

    def test_each_task_layout(self):
        for t in task_dirs():
            for part in ("repo", "hidden_tests", "solution"):
                self.assertTrue((t / part).is_dir(), (t.name, part))
            self.assertFalse(any((t / "repo").rglob("test_hidden*")), t.name)

    def test_untouched_fails_solution_passes(self):
        for t in task_dirs():
            with tempfile.TemporaryDirectory() as d:
                ws = Path(d) / "ws"
                shutil.copytree(t / "repo", ws)
                self.assertFalse(grade(t, ws)["pass"], f"{t.name}: untouched repo passed")
                shutil.copytree(t / "solution", ws, dirs_exist_ok=True)
                r = grade(t, ws)
                self.assertTrue(r["pass"], f"{t.name}: solution failed\n{r['stdout']}")

    def test_grade_leaves_workspace_unchanged(self):
        t = task_dirs()[0]
        with tempfile.TemporaryDirectory() as d:
            ws = Path(d) / "ws"
            shutil.copytree(t / "repo", ws)
            before = sorted(str(p.relative_to(ws)) for p in ws.rglob("*"))
            grade(t, ws)
            after = sorted(str(p.relative_to(ws)) for p in ws.rglob("*"))
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
