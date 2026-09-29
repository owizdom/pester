"""Tokenize a math expression string into a list of tokens."""


def tokenize(expr):
    """Return a list of tokens: numbers (float), operators (+,-,*,/),
    parentheses, and variable names (str starting with alpha)."""
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "-":
            # Negative number: at start or after open paren
            if not tokens or tokens[-1] == "(":
                i += 1
                if i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                    start = i
                    while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                        i += 1
                    tokens.append(-float(expr[start:i]))
                else:
                    raise ValueError("expected number after unary minus")
            else:
                tokens.append("-")
                i += 1
        elif ch in "+*/()":
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == ".":
            start = i
            while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                i += 1
            tokens.append(float(expr[start:i]))
        elif ch.isalpha() or ch == "_":
            start = i
            while i < len(expr) and (expr[i].isalnum() or expr[i] == "_"):
                i += 1
            tokens.append(expr[start:i])
        else:
            raise ValueError(f"unexpected character: {ch!r}")
    return tokens
