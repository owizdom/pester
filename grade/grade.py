"""Grade a workspace against a task's hidden tests, on a copy."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def grade(task_dir, workspace, timeout=120):
    task_dir, workspace = Path(task_dir), Path(workspace)
    with tempfile.TemporaryDirectory(prefix="pester-grade-") as d:
        tmp = Path(d) / "ws"
        shutil.copytree(workspace, tmp, ignore=shutil.ignore_patterns(".claude", "__pycache__"))
        hidden = tmp / "_hidden"
        shutil.copytree(task_dir / "hidden_tests", hidden)
        (hidden / "__init__.py").touch()
        try:
            p = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "_hidden", "-t", "."],
                               cwd=tmp, capture_output=True, text=True, timeout=timeout)
            out, ok = p.stdout + p.stderr, p.returncode == 0
        except subprocess.TimeoutExpired:
            out, ok = "grader timeout", False
        ok = ok and "Ran 0 tests" not in out and "skipped" not in out
        return {"pass": ok, "stdout": out[-4000:]}
