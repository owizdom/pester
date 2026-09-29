"""Lexer: classify each line of Markdown by type."""
import re


def classify_line(line):
    """Return (type, content) for a single line.

    Types: 'header', 'ul', 'blank', 'text'
    """
    stripped = line.rstrip()
    if not stripped:
        return ("blank", "")
    # Bug: does not require space after # characters
    m = re.match(r"^(#{1,6})(.*)", stripped)
    if m:
        level = len(m.group(1))
        text = m.group(2).strip()
        return ("header", (level, text))
    if stripped.lstrip().startswith("- "):
        indent = len(line) - len(line.lstrip())
        text = stripped.lstrip()[2:]
        return ("ul", (indent, text))
    return ("text", stripped)


def lex(markdown):
    """Return a list of (type, content) tuples for the full document."""
    return [classify_line(line) for line in markdown.split("\n")]
