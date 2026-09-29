import unittest

from mdrender.lexer import lex
from mdrender.renderer import render


class BasicTest(unittest.TestCase):
    def test_simple_header(self):
        tokens = lex("# Hello")
        html = render(tokens)
        self.assertIn("<h1>Hello</h1>", html)

    def test_paragraph(self):
        tokens = lex("Just some text")
        html = render(tokens)
        self.assertIn("<p>Just some text</p>", html)


if __name__ == "__main__":
    unittest.main()
