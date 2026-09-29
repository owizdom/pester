import unittest

from textdiff.lcs import lcs_length
from textdiff.display import colorize


class BasicTest(unittest.TestCase):
    def test_lcs_identical(self):
        self.assertEqual(lcs_length("abc", "abc"), 3)

    def test_colorize_smoke(self):
        result = colorize("+added line")
        self.assertIn("added line", result)


if __name__ == "__main__":
    unittest.main()
