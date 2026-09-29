"""Inline formatting utilities."""
import re


def apply_inline(text):
    """Apply inline formatting: bold, links."""
    text = _render_bold(text)
    text = _render_links(text)
    return text


def _render_bold(text):
    """Convert **bold** to <strong>bold</strong>."""
    # Bug: only matches at line start
    m = re.match(r"^\*\*(.+?)\*\*", text)
    if m:
        return f"<strong>{m.group(1)}</strong>" + text[m.end():]
    return text


def _render_links(text):
    """Convert [text](url) to <a href='url'>text</a>."""
    # Bug: drops the href attribute
    def replace_link(m):
        label = m.group(1)
        return f"<a>{label}</a>"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
