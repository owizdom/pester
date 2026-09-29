"""The only source of reminder text. Spec 0001 section 3."""
from pathlib import Path

CONDITIONS = ("C0", "C1", "C2", "C3", "C4")
PARAPHRASES = [l for l in (Path(__file__).parent / "reminders.txt").read_text().splitlines() if l.strip()]
REMINDER = PARAPHRASES[0]
NEUTRAL = "Note: tool call logged."


def inject(condition, action_index, k, rng=None):
    """Text to show after tool call number action_index (1-based), or None."""
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition {condition!r}")
    if condition == "C0" or action_index < k:
        return None
    if condition == "C1":
        return REMINDER if action_index == k else None
    if condition == "C2":
        return REMINDER
    if condition == "C3":
        return PARAPHRASES[(action_index - k) % len(PARAPHRASES)]
    return NEUTRAL
