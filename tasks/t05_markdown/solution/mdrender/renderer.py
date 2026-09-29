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
            html_parts.append(_render_list(tokens, i, 0))
            while i < len(tokens) and tokens[i][0] == "ul":
                i += 1
        else:
            html_parts.append(f"<p>{apply_inline(content)}</p>")
            i += 1
    return "\n".join(html_parts)


def _render_list(tokens, start, base_indent):
    """Recursively render a list with nested indentation."""
    parts = ["<ul>"]
    i = start
    while i < len(tokens) and tokens[i][0] == "ul":
        indent, text = tokens[i][1]
        if indent < base_indent:
            break
        if indent > base_indent:
            # Nested list: find extent and recurse
            nested = _render_list(tokens, i, indent)
            # Attach to previous li
            if parts and parts[-1].endswith("</li>"):
                parts[-1] = parts[-1][:-5] + "\n" + nested + "</li>"
            else:
                parts.append(f"<li>{nested}</li>")
            while i < len(tokens) and tokens[i][0] == "ul" and tokens[i][1][0] >= indent:
                i += 1
        else:
            parts.append(f"<li>{apply_inline(text)}</li>")
            i += 1
    parts.append("</ul>")
    return "\n".join(parts)
