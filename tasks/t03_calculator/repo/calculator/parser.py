"""Parse a token list into an AST (nested tuples).

Grammar (simplified, NO precedence — all left-to-right):
    expr   = primary (OP primary)*
    primary = NUMBER | '(' expr ')'
"""


def parse(tokens):
    pos, node = _parse_expr(tokens, 0)
    if pos != len(tokens):
        raise ValueError(f"unexpected token at position {pos}")
    return node


def _parse_expr(tokens, pos):
    pos, left = _parse_primary(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ("+", "-", "*", "/"):
        op = tokens[pos]
        pos += 1
        pos, right = _parse_primary(tokens, pos)
        left = (op, left, right)
    return pos, left


def _parse_primary(tokens, pos):
    if pos >= len(tokens):
        raise ValueError("unexpected end of expression")
    tok = tokens[pos]
    if isinstance(tok, (int, float)):
        return pos + 1, tok
    if tok == "(":
        pos, node = _parse_expr(tokens, pos + 1)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("missing closing parenthesis")
        return pos + 1, node
    raise ValueError(f"unexpected token: {tok!r}")
