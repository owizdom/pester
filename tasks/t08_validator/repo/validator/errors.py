"""Validation error types.

Provides the ValidationError exception class and a helper for
formatting error lists into human-readable output.
"""


class ValidationError(Exception):
    """Raised when validation fails, carrying a list of error dicts.

    Each error dict has at least 'field' and 'message' keys.
    """

    def __init__(self, errors):
        self.errors = errors
        super().__init__(str(errors))

    @property
    def fields(self):
        """Return the list of field names that have errors."""
        return [e.get("field", "unknown") for e in self.errors]

    @property
    def count(self):
        """Return the number of validation errors."""
        return len(self.errors)


def format_errors(errors):
    """Format a list of error dicts into readable lines.

    Each error becomes a line like 'field: message'.
    """
    lines = []
    for err in errors:
        field = err.get("field", "unknown")
        message = err.get("message", "invalid")
        lines.append(f"{field}: {message}")
    return "\n".join(lines)
