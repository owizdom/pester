"""Low-level character scanning utilities."""


def skip_whitespace(text, pos):
    """Advance past spaces and tabs. Returns new position."""
    while pos < len(text) and text[pos] in (' ', '\t'):
        pos += 1
    return pos


def read_string(text, pos):
    """Read a quoted string starting at pos (which points to the opening quote).
    Returns (string_contents, new_pos, newline_count)."""
    quote = text[pos]
    pos += 1
    result = []
    newlines = 0
    while pos < len(text) and text[pos] != quote:
        if text[pos] == '\\' and pos + 1 < len(text):
            next_ch = text[pos + 1]
            if next_ch == quote:
                result.append(quote)
                pos += 2
                continue
            elif next_ch == 'n':
                result.append('\n')
                pos += 2
                continue
            elif next_ch == 't':
                result.append('\t')
                pos += 2
                continue
            elif next_ch == '\\':
                result.append('\\')
                pos += 2
                continue
        if text[pos] == '\n':
            newlines += 1
        result.append(text[pos])
        pos += 1
    if pos < len(text):
        pos += 1  # skip closing quote
    return ''.join(result), pos, newlines


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
    """Read an operator, including two-character operators."""
    ch = text[pos]
    if pos + 1 < len(text):
        two = text[pos:pos + 2]
        if two in ('==', '!=', '>=', '<='):
            return two, pos + 2
    return ch, pos + 1


def block_comments(text):
    """Strip /* ... */ block comments from text, including nested ones."""
    result = []
    pos = 0
    while pos < len(text):
        if pos + 1 < len(text) and text[pos] == '/' and text[pos + 1] == '*':
            depth = 1
            pos += 2
            while pos < len(text) and depth > 0:
                if pos + 1 < len(text) and text[pos] == '/' and text[pos + 1] == '*':
                    depth += 1
                    pos += 2
                elif pos + 1 < len(text) and text[pos] == '*' and text[pos + 1] == '/':
                    depth -= 1
                    pos += 2
                else:
                    pos += 1
        else:
            result.append(text[pos])
            pos += 1
    return ''.join(result)
