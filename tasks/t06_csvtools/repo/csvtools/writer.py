"""CSV writer utilities.

Converts lists of dicts back into CSV text, handling quoting
for fields that contain commas or double-quote characters.
"""


def quote_field(value):
    """Quote a field value if it contains commas or double-quotes.

    Uses RFC 4180 style: wrap in double-quotes and double any
    internal double-quote characters.
    """
    s = str(value)
    if "," in s or '"' in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def write_csv(rows, columns=None):
    """Write a list of dicts to CSV text.

    If columns is None, uses keys from the first row.
    Returns a string with a trailing newline.
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
