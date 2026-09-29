"""Render classified lines into HTML."""
import re
from mdrender.utils import apply_inline


def render(tokens):
    """Convert a list of (type, content) tokens into an HTML string."""
    html_parts = []
    i = 0
    while i < len(tokens):
        kind, content = tokens[i]
        if kind == "blank":
            i += 1
            continue
        if kind == "header":
            level, text = content
            html_parts.append(f"<h{level}>{apply_inline(text)}</h{level}>")
            i += 1
        elif kind == "ul":
            # Bug: flattens all list items, ignoring indentation
            html_parts.append("<ul>")
            while i < len(tokens) and tokens[i][0] == "ul":
                _, (indent, text) = tokens[i]
                html_parts.append(f"<li>{apply_inline(text)}</li>")
                i += 1
            html_parts.append("</ul>")
        else:
            html_parts.append(f"<p>{apply_inline(content)}</p>")
            i += 1
    return "\n".join(html_parts)
