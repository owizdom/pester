import unittest

from inventory.parser import parse
from inventory.store import Inventory


class BasicTest(unittest.TestCase):
    def test_parse_one(self):
        items = parse("A1,3,2")
        self.assertEqual(items[0].sku, "A1")
        self.assertEqual(items[0].qty, 3)

    def test_add_and_qty(self):
        inv = Inventory()
        for it in parse("A1,3,2"):
            inv.add(it)
        self.assertEqual(inv.qty("A1"), 3)


if __name__ == "__main__":
    unittest.main()
