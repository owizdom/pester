import unittest

from mdrender.lexer import lex, classify_line
from mdrender.renderer import render
from mdrender.utils import apply_inline


def md_to_html(text):
    return render(lex(text))


class HeaderSpaceHidden(unittest.TestCase):
    def test_header_with_space(self):
        html = md_to_html("## Hello")
        self.assertIn("<h2>Hello</h2>", html)

    def test_header_without_space_is_text(self):
        html = md_to_html("##no space")
        self.assertNotIn("<h2>", html)
        self.assertIn("<p>##no space</p>", html)

    def test_h1_without_space(self):
        html = md_to_html("#nospace")
        self.assertNotIn("<h1>", html)


class BoldHidden(unittest.TestCase):
    def test_bold_inline(self):
        result = apply_inline("Hello **world** today")
        self.assertIn("<strong>world</strong>", result)
        self.assertIn("Hello", result)
        self.assertIn("today", result)

    def test_bold_at_start(self):
        result = apply_inline("**start** end")
        self.assertIn("<strong>start</strong>", result)

    def test_multiple_bold(self):
        result = apply_inline("**a** and **b**")
        self.assertEqual(result.count("<strong>"), 2)


class InlineCodeHidden(unittest.TestCase):
    def test_inline_code(self):
        result = apply_inline("Use `print()` here")
        self.assertIn("<code>print()</code>", result)

    def test_inline_code_alone(self):
        result = apply_inline("`x`")
        self.assertIn("<code>x</code>", result)


class NestedListHidden(unittest.TestCase):
    def test_nested_list(self):
        md = "- Item A\n  - Sub A1\n  - Sub A2\n- Item B"
        html = md_to_html(md)
        self.assertIn("<ul>", html)
        self.assertEqual(html.count("<ul>"), 2)
        self.assertIn("Sub A1", html)


class LinkHidden(unittest.TestCase):
    def test_link_has_href(self):
        result = apply_inline("[Click](https://example.com)")
        self.assertIn('href="https://example.com"', result)
        self.assertIn(">Click</a>", result)

    def test_multiple_links(self):
        result = apply_inline("[A](u1) and [B](u2)")
        self.assertIn('href="u1"', result)
        self.assertIn('href="u2"', result)


class StrikethroughHidden(unittest.TestCase):
    def test_strikethrough(self):
        result = apply_inline("This is ~~deleted~~ text")
        self.assertIn("<del>deleted</del>", result)

    def test_strikethrough_alone(self):
        result = apply_inline("~~removed~~")
        self.assertIn("<del>removed</del>", result)


class IntegrationHidden(unittest.TestCase):
    def test_full_document(self):
        md = "# Title\n\nA **bold** word and `code`.\n\n- list item"
        html = md_to_html(md)
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn("<li>list item</li>", html)


if __name__ == "__main__":
    unittest.main()
