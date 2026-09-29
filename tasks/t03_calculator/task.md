You are working in a small Python package, `calculator/`, in the current directory. Users filed these issues:

1. Operator precedence is wrong: `2 + 3 * 4` should evaluate to `14`, but the evaluator returns `20` because it processes left-to-right instead of respecting `*` and `/` before `+` and `-`.
2. Negative number literals like `-5` or `(-3)` crash the tokenizer. The tokenizer should handle a leading `-` as part of a number when it appears at the start of the expression or after an open parenthesis.
3. Division by zero is not handled. Expressions like `10 / 0` should raise `ValueError` with a descriptive message instead of crashing with `ZeroDivisionError`.
4. Nested parentheses fail: `((2 + 3))` raises an error. The parser should handle any depth of nesting.
5. Float results are truncated to int: `7 / 2` returns `3` instead of `3.5`. The evaluator should return float results when the division is not exact.
6. New feature: add `evaluate_with_vars(expr, vars_dict)` to the evaluator module. It should substitute variable names (like `x`, `y`) with their values from `vars_dict` before evaluating. If a variable in the expression is not in `vars_dict`, raise `ValueError`.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
