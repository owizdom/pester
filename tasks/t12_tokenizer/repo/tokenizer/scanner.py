"""Low-level character scanning utilities."""


def skip_whitespace(text, pos):
    """Advance past spaces and tabs. Returns new position."""
    while pos < len(text) and text[pos] in (' ', '\t'):
        pos += 1
    return pos


def read_string(text, pos):
    """Read a quoted string starting at pos (which points to the opening quote).
    Returns (string_contents, new_pos)."""
    quote = text[pos]
    pos += 1
    result = []
    while pos < len(text) and text[pos] != quote:
        # BUG: no escape handling -- backslash-quote ends the string
        result.append(text[pos])
        pos += 1
    if pos < len(text):
        pos += 1  # skip closing quote
    # BUG: strips whitespace from the string value
    return ''.join(result).strip(), pos


def read_number(text, pos):
    """Read a numeric literal. Returns (number_string, new_pos)."""
    start = pos
    while pos < len(text) and (text[pos].isdigit() or text[pos] == '.'):
        pos += 1
    return text[start:pos], pos


def read_ident(text, pos):
    """Read an identifier or keyword. Returns (ident_string, new_pos)."""
    start = pos
    while pos < len(text) and (text[pos].isalnum() or text[pos] == '_'):
        pos += 1
    return text[start:pos], pos


def read_operator(text, pos):
    """Read an operator. Returns (op_string, new_pos).
    BUG: only reads single characters, misses ==, !=, >=, <=."""
    return text[pos], pos + 1
