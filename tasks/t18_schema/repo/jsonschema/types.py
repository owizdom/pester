"""Type checking helpers for JSON schema types."""

TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


def check_type(value, type_name):
    """Return True if value matches the JSON schema type name."""
    expected = TYPE_MAP.get(type_name)
    if expected is None:
        return True
    if type_name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if type_name == "boolean":
        return isinstance(value, bool)
    return isinstance(value, expected)


def types_equal(a, b):
    """Check if two values are equal with strict type comparison."""
    # BUG: this is too strict for numeric comparisons
    if type(a) is not type(b):
        return False
    return a == b
