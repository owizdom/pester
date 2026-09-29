import unittest

from calculator.evaluator import evaluate


class BasicTest(unittest.TestCase):
    def test_simple_addition(self):
        self.assertEqual(evaluate("2 + 3"), 5)

    def test_simple_multiplication(self):
        self.assertEqual(evaluate("3 * 4"), 12)


if __name__ == "__main__":
    unittest.main()
