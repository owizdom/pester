"""Display helpers for diffs: ANSI coloring and side-by-side view."""

RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def colorize(diff_text):
    """Add ANSI color codes to unified-diff text."""
    out = []
    for line in diff_text.split("\n"):
        if line.startswith("---") or line.startswith("+++"):
            out.append(f"{CYAN}{line}{RESET}")
        elif line.startswith("-"):
            out.append(f"{RED}{line}{RESET}")
        elif line.startswith("+"):
            out.append(f"{GREEN}{line}{RESET}")
        elif line.startswith("@@"):
            out.append(f"{CYAN}{line}{RESET}")
        else:
            out.append(line)
    return "\n".join(out)


def side_by_side(old_lines, new_lines, width=40):
    """Format *old_lines* and *new_lines* in two columns."""
    length = max(len(old_lines), len(new_lines))
    out = []
    for i in range(length):
        left = old_lines[i] if i < len(old_lines) else ""
        right = new_lines[i] if i < len(new_lines) else ""
        out.append(f"{left:<{width}} | {right}")
    return "\n".join(out)
