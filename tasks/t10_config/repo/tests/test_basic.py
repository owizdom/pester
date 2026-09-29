import unittest
from configparser_ext.parser import parse


class BasicTest(unittest.TestCase):
    def test_parse_simple(self):
        cfg = parse("[main]\nname = hello\ncount = 3\n")
        sec = cfg["main"]
        self.assertEqual(sec.get("name"), "hello")
        self.assertEqual(sec.getint("count"), 3)

    def test_boolean(self):
        cfg = parse("[flags]\nenabled = true\n")
        self.assertTrue(cfg["flags"].getboolean("enabled"))


if __name__ == "__main__":
    unittest.main()
