"""Tokenize a math expression string into a list of tokens."""


def tokenize(expr):
    """Return a list of tokens: numbers (float), operators (+,-,*,/),
    and parentheses."""
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "+-*/()":
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == ".":
            start = i
            while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                i += 1
            tokens.append(float(expr[start:i]))
        else:
            raise ValueError(f"unexpected character: {ch!r}")
    return tokens
