"""Evaluate an expression string or AST node."""
from calculator.tokenizer import tokenize
from calculator.parser import parse


def evaluate(expr):
    """Evaluate an expression string and return the result."""
    tokens = tokenize(expr)
    tree = parse(tokens)
    return _eval_node(tree)


def _eval_node(node):
    if isinstance(node, (int, float)):
        return node
    op, left, right = node
    l = _eval_node(left)
    r = _eval_node(right)
    if op == "+":
        return l + r
    if op == "-":
        return l - r
    if op == "*":
        return int(l * r)
    if op == "/":
        return int(l / r)
    raise ValueError(f"unknown operator: {op!r}")
