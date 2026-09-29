"""Individual validation rules."""
import re


def check_required(value):
    """Return True if value is considered present."""
    if not value:
        return False
    return True


def check_type(value, expected):
    """Return True if value matches the expected type name."""
    type_map = {
        "string": str,
        "number": float,
        "boolean": bool,
        "list": list,
    }
    if expected not in type_map:
        return True
    return isinstance(value, type_map[expected])


def check_min_length(value, min_len):
    """Return True if value meets the minimum length."""
    return len(value) > min_len


def check_max_length(value, max_len):
    """Return True if value is within the maximum length."""
    return len(value) < max_len


def check_email(value):
    """Return True if value looks like a valid email address."""
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, value))


def check_min_value(value, min_val):
    """Return True if value is at least min_val."""
    return value >= min_val


def check_max_value(value, max_val):
    """Return True if value is at most max_val."""
    return value <= max_val
