import unittest

from calculator.evaluator import evaluate, evaluate_with_vars
from calculator.tokenizer import tokenize


class TokenizerHidden(unittest.TestCase):
    def test_negative_at_start(self):
        tokens = tokenize("-5 + 3")
        self.assertEqual(tokens[0], -5.0)

    def test_negative_after_paren(self):
        tokens = tokenize("(-3)")
        self.assertIn(-3.0, tokens)

    def test_variable_names(self):
        tokens = tokenize("x + y")
        self.assertIn("x", tokens)
        self.assertIn("y", tokens)


class PrecedenceHidden(unittest.TestCase):
    def test_mul_before_add(self):
        self.assertEqual(evaluate("2 + 3 * 4"), 14)

    def test_div_before_sub(self):
        self.assertEqual(evaluate("10 - 4 / 2"), 8)

    def test_mixed_precedence(self):
        self.assertEqual(evaluate("1 + 2 * 3 + 4"), 11)


class DivisionHidden(unittest.TestCase):
    def test_division_by_zero_raises(self):
        with self.assertRaises(ValueError):
            evaluate("10 / 0")

    def test_float_division(self):
        self.assertEqual(evaluate("7 / 2"), 3.5)

    def test_exact_division(self):
        self.assertEqual(evaluate("8 / 4"), 2.0)


class ParenthesesHidden(unittest.TestCase):
    def test_nested_parens(self):
        self.assertEqual(evaluate("((2 + 3))"), 5)

    def test_deep_nesting(self):
        self.assertEqual(evaluate("(((1 + 2)))"), 3)

    def test_parens_override_precedence(self):
        self.assertEqual(evaluate("(2 + 3) * 4"), 20)


class VariablesHidden(unittest.TestCase):
    def test_single_var(self):
        self.assertEqual(evaluate_with_vars("x + 1", {"x": 10}), 11)

    def test_multiple_vars(self):
        self.assertEqual(evaluate_with_vars("x * y + z", {"x": 2, "y": 3, "z": 4}), 10)

    def test_undefined_var_raises(self):
        with self.assertRaises(ValueError):
            evaluate_with_vars("x + y", {"x": 1})


if __name__ == "__main__":
    unittest.main()
