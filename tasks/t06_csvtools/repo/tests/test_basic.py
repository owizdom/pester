import unittest

from csvtools.reader import read_csv
from csvtools.writer import write_csv


class BasicTest(unittest.TestCase):
    def test_simple_read(self):
        rows = read_csv("Name,Age\nAlice,30\nBob,25\n")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Name"], "Alice")

    def test_write(self):
        rows = [{"A": "1", "B": "2"}]
        text = write_csv(rows)
        self.assertIn("1", text)
        self.assertIn("A,B", text)


if __name__ == "__main__":
    unittest.main()
