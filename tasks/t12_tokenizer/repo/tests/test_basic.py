import unittest

from tokenizer.lexer import tokenize
from tokenizer.tokens import NUMBER, IDENT, OP


class BasicTest(unittest.TestCase):
    def test_simple_expression(self):
        tokens = tokenize("x + 1")
        self.assertEqual(tokens[0].type, IDENT)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(tokens[1].type, OP)
        self.assertEqual(tokens[2].type, NUMBER)

    def test_number(self):
        tokens = tokenize("42")
        self.assertEqual(tokens[0].value, "42")
        self.assertEqual(tokens[0].type, NUMBER)


if __name__ == "__main__":
    unittest.main()
