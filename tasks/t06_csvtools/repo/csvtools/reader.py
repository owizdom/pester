"""CSV reader utilities.

Provides functions for parsing CSV-formatted text into Python data
structures. The first row of the input is always treated as headers.
"""


def parse_row(line):
    """Split a CSV line into a list of field strings.

    Does not handle quoting -- fields are split on every comma.
    """
    return line.split(",")


def read_csv(text):
    """Parse CSV text into a list of row dicts.

    The first line is the header row; remaining lines are data.
    Each data line becomes a dict mapping header names to values.
    All values are returned as strings.
    """
    lines = text.strip().splitlines()
    headers = parse_row(lines[0])
    rows = []
    for line in lines[1:]:
        values = parse_row(line)
        row = {}
        for i, h in enumerate(headers):
            row[h] = values[i]
        rows.append(row)
    return rows


def column_values(rows, column):
    """Return a list of all values for a given column across rows."""
    return [row[column] for row in rows if column in row]
