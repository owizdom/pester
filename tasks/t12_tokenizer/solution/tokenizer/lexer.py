"""Main lexer: turns source text into a list of Tokens."""

from tokenizer.tokens import Token, NUMBER, STRING, IDENT, OP, NEWLINE, EOF
from tokenizer.scanner import skip_whitespace, read_string, read_number, read_ident, read_operator

OPERATORS = set('+-*/=!<>(){}[];,.')


def tokenize(text):
    """Tokenize the input text and return a list of Token objects."""
    tokens = []
    pos = 0
    line = 1

    while pos < len(text):
        pos = skip_whitespace(text, pos)
        if pos >= len(text):
            break

        ch = text[pos]

        if ch == '\n':
            tokens.append(Token(NEWLINE, '\\n', line))
            line += 1
            pos += 1

        elif ch in ('"', "'"):
            val, pos, newlines = read_string(text, pos)
            tokens.append(Token(STRING, val, line))
            line += newlines

        elif ch.isdigit():
            val, pos = read_number(text, pos)
            tokens.append(Token(NUMBER, val, line))

        elif ch.isalpha() or ch == '_':
            val, pos = read_ident(text, pos)
            tokens.append(Token(IDENT, val, line))

        elif ch in OPERATORS:
            val, pos = read_operator(text, pos)
            tokens.append(Token(OP, val, line))

        else:
            pos += 1  # skip unknown characters

    tokens.append(Token(EOF, "", line))
    return tokens
