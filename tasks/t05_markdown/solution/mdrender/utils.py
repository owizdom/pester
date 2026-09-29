"""Inline formatting utilities."""
import re


def apply_inline(text):
    """Apply inline formatting: bold, inline code, strikethrough, links."""
    text = _render_code(text)
    text = _render_bold(text)
    text = _render_strikethrough(text)
    text = _render_links(text)
    return text


def _render_bold(text):
    """Convert **bold** to <strong>bold</strong> anywhere in text."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def _render_code(text):
    """Convert `code` to <code>code</code>."""
    return re.sub(r"`(.+?)`", r"<code>\1</code>", text)


def _render_strikethrough(text):
    """Convert ~~text~~ to <del>text</del>."""
    return re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)


def _render_links(text):
    """Convert [text](url) to <a href='url'>text</a>."""
    def replace_link(m):
        label = m.group(1)
        url = m.group(2)
        return f"<a href=\"{url}\">{label}</a>"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
