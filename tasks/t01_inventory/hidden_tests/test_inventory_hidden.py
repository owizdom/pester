import unittest

from inventory.item import Item
from inventory.parser import parse, parse_line
from inventory.report import format_report
from inventory.store import Inventory

DATA = """# stock file
A1 , 3 , 2.50

B2,1,0.10
"""


def inv_from(text):
    inv = Inventory()
    for it in parse(text):
        inv.add(it)
    return inv


class ParseHidden(unittest.TestCase):
    def test_blank_comment_space_decimal(self):
        items = parse(DATA)
        self.assertEqual([(i.sku, i.qty) for i in items], [("A1", 3), ("B2", 1)])
        self.assertAlmostEqual(items[0].price, 2.5)

    def test_bad_field_count(self):
        with self.assertRaises(ValueError):
            parse_line("A1,3")
        with self.assertRaises(ValueError):
            parse_line("A1,3,2,9")


class StoreHidden(unittest.TestCase):
    def test_add_accumulates_newest_price(self):
        inv = Inventory()
        inv.add(Item("A1", 2, 1.0))
        inv.add(Item("A1", 3, 2.0))
        self.assertEqual(inv.qty("A1"), 5)
        self.assertAlmostEqual(inv.total_value(), 10.0)

    def test_remove_rules(self):
        inv = inv_from(DATA)
        with self.assertRaises(KeyError):
            inv.remove("ZZ", 1)
        with self.assertRaises(ValueError):
            inv.remove("A1", 4)
        with self.assertRaises(ValueError):
            inv.remove("A1", 0)
        with self.assertRaises(ValueError):
            inv.remove("A1", -1)
        inv.remove("A1", 2)
        self.assertEqual(inv.qty("A1"), 1)

    def test_total_rounded(self):
        self.assertEqual(inv_from(DATA).total_value(), 7.6)

    def test_low_stock(self):
        inv = inv_from("C3,5,1\nA1,1,1\nB2,2,1\n")
        self.assertEqual(inv.low_stock(3), ["A1", "B2"])
        self.assertEqual(inv.low_stock(1), [])


class ReportHidden(unittest.TestCase):
    def test_report(self):
        self.assertEqual(format_report(inv_from("B2,1,0.10\nA1,3,2.50\n")), "A1: 3\nB2: 1\nTOTAL: 7.60")


if __name__ == "__main__":
    unittest.main()
