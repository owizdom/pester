"""Validation error types for the JSON schema validator."""


class ValidationError(Exception):
    """Raised when a value does not conform to a schema."""

    def __init__(self, message, path=None):
        self.message = message
        self.path = path or []
        super().__init__(self.message)

    def __str__(self):
        loc = ".".join(str(p) for p in self.path) if self.path else "<root>"
        return f"{loc}: {self.message}"

    def absolute_path(self):
        """Return the full dotted path to the failing element."""
        return ".".join(str(p) for p in self.path)


class SchemaError(Exception):
    """Raised when the schema itself is malformed."""

    def __init__(self, message, keyword=None):
        self.message = message
        self.keyword = keyword
        super().__init__(self.message)

    def __str__(self):
        if self.keyword:
            return f"schema error in {self.keyword!r}: {self.message}"
        return f"schema error: {self.message}"
