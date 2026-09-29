"""Evaluate an expression string or AST node."""
from calculator.tokenizer import tokenize
from calculator.parser import parse


def evaluate(expr):
    """Evaluate an expression string and return the result."""
    tokens = tokenize(expr)
    tree = parse(tokens)
    return _eval_node(tree)


def evaluate_with_vars(expr, vars_dict):
    """Evaluate an expression with variable substitution."""
    tokens = tokenize(expr)
    tree = parse(tokens)
    return _eval_node(tree, vars_dict)


def _eval_node(node, variables=None):
    if isinstance(node, (int, float)):
        return node
    if isinstance(node, tuple) and node[0] == "var":
        name = node[1]
        if variables is None or name not in variables:
            raise ValueError(f"undefined variable: {name!r}")
        return variables[name]
    op, left, right = node
    l = _eval_node(left, variables)
    r = _eval_node(right, variables)
    if op == "+":
        return l + r
    if op == "-":
        return l - r
    if op == "*":
        return l * r
    if op == "/":
        if r == 0:
            raise ValueError("division by zero")
        return l / r
    raise ValueError(f"unknown operator: {op!r}")
