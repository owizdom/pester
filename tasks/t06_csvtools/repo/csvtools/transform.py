"""Data transformation utilities for CSV rows.

Provides type inference, sorting, and aggregation helpers
that operate on lists of row dicts.
"""


def infer_type(value):
    """Convert a string value to int, float, or leave as string.

    Attempts integer first, then float. Returns the original
    string if neither conversion succeeds.
    """
    s = value.strip()
    if s.isdigit():
        return int(s)
    if "." in s and s.replace(".", "", 1).isdigit():
        return float(s)
    return s


def typed_rows(rows):
    """Apply type inference to every string value in each row.

    Returns a new list of dicts with values converted where possible.
    Non-string values are left unchanged.
    """
    return [
        {k: infer_type(v) if isinstance(v, str) else v for k, v in row.items()}
        for row in rows
    ]


def sort_by(rows, column):
    """Sort rows by a given column.

    Returns a new sorted list; the original is not modified.
    """
    return sorted(rows, key=lambda r: str(r[column]))
