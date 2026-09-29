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
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
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
    return sorted(rows, key=lambda r: r[column])


def pivot(rows, group_col, value_col, agg="sum"):
    """Group rows by group_col and aggregate value_col.

    Supported aggregations: sum, count, mean, min, max.
    Returns a list of {group_col: key, value_col: result} dicts sorted by key.
    Raises ValueError for an unknown aggregation.
    """
    groups = {}
    for row in rows:
        key = row[group_col]
        groups.setdefault(key, []).append(row[value_col])

    agg_funcs = {
        "sum": sum,
        "count": len,
        "mean": lambda vs: sum(vs) / len(vs),
        "min": min,
        "max": max,
    }
    if agg not in agg_funcs:
        raise ValueError(f"unknown aggregation: {agg}")

    func = agg_funcs[agg]
    return [
        {group_col: key, value_col: func(vals)}
        for key, vals in sorted(groups.items())
    ]
