"""macOS sandbox profile that limits an agent to its workspace and the clean Claude config."""
from pathlib import Path

HOME = Path.home()
ALLOW = [HOME / ".pester" / "claude-clean", HOME / ".local", HOME / "Library" / "Caches",
         HOME / "Library" / "Keychains", HOME / "Library" / "Preferences"]


def profile(ws):
    allow = " ".join(f'(subpath "{p}")' for p in [Path(ws).resolve(), *ALLOW])
    return ("(version 1)\n(allow default)\n"
            f'(deny file-read-data file-write* (subpath "{HOME}"))\n'
            f"(allow file-read-data file-write* {allow})\n")


def wrap(cmd, ws):
    return ["sandbox-exec", "-p", profile(ws), *cmd]
