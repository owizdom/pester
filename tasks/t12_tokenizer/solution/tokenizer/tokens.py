"""Token types and the Token data class."""


class Token:
    """A single token with a type, value, and source line number."""

    def __init__(self, type, value, line=1):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r}, line={self.line})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (self.type, self.value, self.line) == (other.type, other.value, other.line)

    def __hash__(self):
        return hash((self.type, self.value, self.line))

    def is_eof(self):
        """Return True if this is an EOF token."""
        return self.type == "EOF"


# Token type constants
NUMBER = "NUMBER"
STRING = "STRING"
IDENT = "IDENT"
OP = "OP"
NEWLINE = "NEWLINE"
EOF = "EOF"
