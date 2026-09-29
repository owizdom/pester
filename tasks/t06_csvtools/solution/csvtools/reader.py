"""CSV reader utilities.

Provides functions for parsing CSV-formatted text into Python data
structures. The first row of the input is always treated as headers.
"""


def parse_row(line):
    """Split a CSV line into a list of field strings.

    Respects double-quoted fields: commas inside quotes are kept
    as part of the field value, and the quotes are removed.
    """
    fields = []
    current = []
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == "," and not in_quotes:
            fields.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    fields.append("".join(current).strip())
    return fields


def read_csv(text):
    """Parse CSV text into a list of row dicts.

    The first line is the header row; remaining lines are data.
    Each data line becomes a dict mapping header names to values.
    All values are returned as strings.
    """
    lines = text.strip().splitlines()
    headers = [h.strip() for h in parse_row(lines[0])]
    rows = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = parse_row(line)
        row = {}
        for i, h in enumerate(headers):
            row[h] = values[i] if i < len(values) else ""
        rows.append(row)
    return rows


def column_values(rows, column):
    """Return a list of all values for a given column across rows."""
    return [row[column] for row in rows if column in row]
