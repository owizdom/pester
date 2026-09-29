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

    groups = [[change_indices[0]]]
    for idx in change_indices[1:]:
        if idx - groups[-1][-1] <= 2 * context:
            groups[-1].append(idx)
        else:
            groups.append([idx])

    lines = []
    lines.append(f"--- {old_name}")
    lines.append(f"+++ {new_name}")

    for group in groups:
        start = max(0, group[0] - context)
        end = min(len(ops), group[-1] + context + 1)

        old_start = sum(1 for t, _ in ops[:start] if t in (" ", "-")) + 1
        new_start = sum(1 for t, _ in ops[:start] if t in (" ", "+")) + 1
        old_count = sum(1 for t, _ in ops[start:end] if t in (" ", "-"))
        new_count = sum(1 for t, _ in ops[start:end] if t in (" ", "+"))

        lines.append(f"@@ -{old_start},{old_count} +{new_start},{new_count} @@")
        for t, line in ops[start:end]:
            lines.append(f"{t}{line}")

    return "\n".join(lines)


def word_diff(line_a, line_b):
    """Return word-level changes between *line_a* and *line_b*.

    Each element is a (type, word) tuple where type is
    ``"equal"``, ``"add"``, or ``"remove"``.
    """
    words_a = line_a.split()
    words_b = line_b.split()
    common = lcs(words_a, words_b)

    result = []
    ai, bi, ci = 0, 0, 0
    while ci < len(common):
        while ai < len(words_a) and words_a[ai] != common[ci]:
            result.append(("remove", words_a[ai]))
            ai += 1
        while bi < len(words_b) and words_b[bi] != common[ci]:
            result.append(("add", words_b[bi]))
            bi += 1
        result.append(("equal", common[ci]))
        ai += 1
        bi += 1
        ci += 1
    while ai < len(words_a):
        result.append(("remove", words_a[ai]))
        ai += 1
    while bi < len(words_b):
        result.append(("add", words_b[bi]))
        bi += 1
    return result
