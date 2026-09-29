import unittest

from template.parser import parse
from template.renderer import render


class HTMLEscapeTests(unittest.TestCase):
    def test_angle_brackets_escaped(self):
        nodes = parse("{{ name }}")
        result = render(nodes, {"name": "<script>alert(1)</script>"})
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)

    def test_ampersand_escaped(self):
        nodes = parse("{{ val }}")
        result = render(nodes, {"val": "a & b"})
        self.assertIn("&amp;", result)

    def test_quote_escaped(self):
        nodes = parse('{{ val }}')
        result = render(nodes, {"val": 'say "hi"'})
        self.assertIn("&quot;", result)


class EmptyForLoopTests(unittest.TestCase):
    def test_empty_list_no_crash(self):
        tpl = "{% for x in items %}{{ x }}{% endfor %}"
        nodes = parse(tpl)
        result = render(nodes, {"items": []})
        self.assertEqual(result.strip(), "")

    def test_nonempty_list_still_works(self):
        tpl = "{% for x in items %}{{ x }} {% endfor %}"
        nodes = parse(tpl)
        result = render(nodes, {"items": ["a", "b"]})
        self.assertIn("a", result)
        self.assertIn("b", result)


class NestedIfTests(unittest.TestCase):
    def test_nested_if_else(self):
        tpl = (
            "{% if outer %}"
            "{% if inner %}INNER_TRUE{% else %}INNER_FALSE{% endif %}"
            "{% else %}"
            "OUTER_FALSE"
            "{% endif %}"
        )
        nodes = parse(tpl)

        result = render(nodes, {"outer": True, "inner": True})
        self.assertIn("INNER_TRUE", result)
        self.assertNotIn("OUTER_FALSE", result)

        result = render(nodes, {"outer": True, "inner": False})
        self.assertIn("INNER_FALSE", result)
        self.assertNotIn("OUTER_FALSE", result)

        result = render(nodes, {"outer": False})
        self.assertIn("OUTER_FALSE", result)
        self.assertNotIn("INNER", result)

    def test_simple_if_else(self):
        tpl = "{% if show %}YES{% else %}NO{% endif %}"
        nodes = parse(tpl)
        self.assertIn("YES", render(nodes, {"show": True}))
        self.assertIn("NO", render(nodes, {"show": False}))


class UndefinedVarTests(unittest.TestCase):
    def test_undefined_renders_empty(self):
        nodes = parse("Hello {{ missing }}!")
        result = render(nodes, {})
        self.assertEqual(result, "Hello !")

    def test_defined_still_works(self):
        nodes = parse("Hello {{ name }}!")
        result = render(nodes, {"name": "World"})
        self.assertIn("World", result)


class WhitespaceTests(unittest.TestCase):
    def test_no_extra_blank_lines(self):
        tpl = "A\n{% if show %}\nB\n{% endif %}\nC"
        nodes = parse(tpl)
        result = render(nodes, {"show": True})
        lines = [l for l in result.split('\n') if l.strip()]
        self.assertEqual(lines, ["A", "B", "C"])

    def test_inline_tags_no_extra_lines(self):
        tpl = "start\n{% for x in items %}\n{{ x }}\n{% endfor %}\nend"
        nodes = parse(tpl)
        result = render(nodes, {"items": ["a"]})
        lines = [l for l in result.split('\n') if l.strip()]
        self.assertEqual(lines, ["start", "a", "end"])


class FilterTests(unittest.TestCase):
    def test_upper(self):
        nodes = parse("{{ name | upper }}")
        result = render(nodes, {"name": "hello"})
        self.assertEqual(result, "HELLO")

    def test_lower(self):
        nodes = parse("{{ name | lower }}")
        result = render(nodes, {"name": "HELLO"})
        self.assertEqual(result, "hello")

    def test_default_on_missing(self):
        nodes = parse('{{ count | default:"0" }}')
        result = render(nodes, {})
        self.assertEqual(result, "0")

    def test_default_not_applied_when_set(self):
        nodes = parse('{{ count | default:"0" }}')
        result = render(nodes, {"count": "5"})
        self.assertEqual(result, "5")


if __name__ == "__main__":
    unittest.main()
