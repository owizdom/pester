#!/usr/bin/env python3
"""PostToolUse hook. Counts tool calls in <state>/hook.jsonl and injects inject()'s text."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from harness.inject import inject  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--state", required=True)
    a = ap.parse_args()
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        payload = {}
    state = Path(a.state)
    state.mkdir(parents=True, exist_ok=True)
    log = state / "hook.jsonl"
    i = 1 + (sum(1 for _ in log.open()) if log.exists() else 0)
    text = inject(a.condition, i, a.k)
    with log.open("a") as f:
        f.write(json.dumps({"i": i, "tool": payload.get("tool_name"), "text": text}) + "\n")
    if text is not None:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": text}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
