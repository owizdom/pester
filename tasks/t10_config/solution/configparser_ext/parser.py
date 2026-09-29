"""Parse INI-style configuration text."""
import os
from configparser_ext.section import Section


def _strip_inline_comment(value):
    """Remove inline comment (# or ;) that isn't inside quotes."""
    in_quote = False
    quote_char = None
    for i, ch in enumerate(value):
        if ch in ('"', "'") and not in_quote:
            in_quote = True
            quote_char = ch
        elif ch == quote_char and in_quote:
            in_quote = False
        elif ch in ("#", ";") and not in_quote:
            return value[:i].rstrip()
    return value


def parse(text):
    """Parse INI text into a dict of section name -> Section."""
    sections = {}
    current = None
    last_key = None

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped or stripped.startswith("#") or stripped.startswith(";"):
            continue

        # Section header
        if stripped.startswith("[") and stripped.endswith("]"):
            header = stripped[1:-1].strip()
            parent_name = None
            if ":" in header:
                child, parent = header.split(":", 1)
                header = child.strip()
                parent_name = parent.strip()
            current = Section(header)
            if parent_name and parent_name in sections:
                for k, v in sections[parent_name].items():
                    current.set(k, v)
            sections[header] = current
            last_key = None
            continue

        # Multiline continuation
        if line[0:1] in (" ", "\t") and current is not None and last_key is not None:
            old = current.get(last_key, "")
            current.set(last_key, old + "\n" + stripped)
            continue

        # Key = value
        if "=" in stripped:
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = _strip_inline_comment(value.strip())
            if current is not None:
                current.set(key, value)
                last_key = key

    return sections


def get_env(sections, section_name, key, env_var):
    """Get a key from a section, falling back to an environment variable."""
    sec = sections.get(section_name)
    if sec is not None:
        val = sec.get(key)
        if val is not None:
            return val
    return os.environ.get(env_var)
