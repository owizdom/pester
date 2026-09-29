"""Unified diff generation from two lists of lines."""

from textdiff.lcs import lcs


def unified_diff(old_lines, new_lines, old_name="a", new_name="b", context=3):
    """Return a unified-diff string comparing *old_lines* to *new_lines*."""
    common = lcs(old_lines, new_lines)

    ops = []
    oi, ni, ci = 0, 0, 0
    while ci < len(common):
        while oi < len(old_lines) and old_lines[oi] != common[ci]:
            ops.append(("-", old_lines[oi]))
            oi += 1
        while ni < len(new_lines) and new_lines[ni] != common[ci]:
            ops.append(("+", new_lines[ni]))
            ni += 1
        ops.append((" ", common[ci]))
        oi += 1
        ni += 1
        ci += 1
    while oi < len(old_lines):
        ops.append(("-", old_lines[oi]))
        oi += 1
    while ni < len(new_lines):
        ops.append(("+", new_lines[ni]))
        ni += 1

    return _format_hunks(ops, old_name, new_name, context)


def _format_hunks(ops, old_name, new_name, context):
    """Build the textual unified-diff output from a list of ops."""
    if not any(t != " " for t, _ in ops):
        return ""

    change_indices = [i for i, (t, _) in enumerate(ops) if t != " "]
    if not change_indices:
        return ""

    lines = []

    for idx in change_indices:
        start = max(0, idx - context)
        end = min(len(ops), idx + context + 1)

        old_start = sum(1 for t, _ in ops[:start] if t in (" ", "-"))
        new_start = sum(1 for t, _ in ops[:start] if t in (" ", "+"))
        old_count = sum(1 for t, _ in ops[start:end] if t in (" ", "-"))
        new_count = sum(1 for t, _ in ops[start:end] if t in (" ", "+"))

        lines.append(f"@@ -{old_start},{old_count} +{new_start},{new_count} @@")
        for t, line in ops[start:end]:
            if t == "-":
                lines.append(f"+{line}")
            elif t == "+":
                lines.append(f"-{line}")
            else:
                lines.append(f" {line}")

    return "\n".join(lines)
