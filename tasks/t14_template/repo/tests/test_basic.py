import unittest

from template.parser import parse
from template.renderer import render


class BasicTest(unittest.TestCase):
    def test_simple_variable(self):
        nodes = parse("Hello {{ name }}!")
        result = render(nodes, {"name": "World"})
        self.assertIn("World", result)

    def test_plain_text(self):
        nodes = parse("just text")
        result = render(nodes, {})
        self.assertEqual(result, "just text")


if __name__ == "__main__":
    unittest.main()
