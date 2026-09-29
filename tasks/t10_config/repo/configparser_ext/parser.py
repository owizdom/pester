"""Parse INI-style configuration text."""
from configparser_ext.section import Section


def parse(text):
    """Parse INI text into a dict of section name -> Section."""
    sections = {}
    current = None

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
            sections[header] = current
            continue

        # Continuation lines (starting with whitespace) are skipped
        if line[0:1] in (" ", "\t"):
            continue

        # Key = value
        if "=" in stripped:
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip()
            if current is not None:
                current.set(key, value)

    return sections
