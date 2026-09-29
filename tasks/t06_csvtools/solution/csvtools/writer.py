"""CSV writer utilities."""


def quote_field(value):
    """Quote a field if it contains commas or double-quotes."""
    s = str(value)
    if "," in s or '"' in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def write_csv(rows, columns=None):
    """Write a list of dicts to CSV text.

    If columns is None, uses keys from the first row.
    """
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    lines = [",".join(columns)]
    for row in rows:
        line = ",".join(quote_field(row.get(c, "")) for c in columns)
        lines.append(line)
    return "\n".join(lines) + "\n"
