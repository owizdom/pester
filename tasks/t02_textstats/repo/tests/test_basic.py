import unittest

from textstats.cache import LRUCache
from textstats.stats import word_freq


class BasicTest(unittest.TestCase):
    def test_freq(self):
        self.assertEqual(word_freq("a b a")["a"], 2)

    def test_cache_put_get(self):
        c = LRUCache(2)
        c.put("x", 1)
        self.assertEqual(c.get("x"), 1)


if __name__ == "__main__":
    unittest.main()
