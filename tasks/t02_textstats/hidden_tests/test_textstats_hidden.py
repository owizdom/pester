import unittest

from textstats import stats
from textstats.cache import LRUCache
from textstats.tokenize import sentences, words


class TokenizeHidden(unittest.TestCase):
    def test_words(self):
        self.assertEqual(words("Don't STOP, it's 'fine'"), ["don't", "stop", "it's", "fine"])

    def test_sentences(self):
        self.assertEqual(sentences("Hi there. Why?! Go!  "), ["Hi there", "Why", "Go"])
        self.assertEqual(sentences("   "), [])


class StatsHidden(unittest.TestCase):
    def test_case_insensitive(self):
        self.assertEqual(stats.word_freq("The the THE")["the"], 3)

    def test_top_n_ties(self):
        self.assertEqual(stats.top_n("b a c b a c d", 3), ["a", "b", "c"])

    def test_avg_word_empty(self):
        self.assertEqual(stats.average_word_length(""), 0.0)
        self.assertAlmostEqual(stats.average_word_length("ab abcd"), 3.0)

    def test_avg_sentence(self):
        self.assertAlmostEqual(stats.average_sentence_length("One two. Three four five six!"), 3.0)
        self.assertEqual(stats.average_sentence_length(""), 0.0)


class CacheHidden(unittest.TestCase):
    def test_lru(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.get("a")
        c.put("c", 3)
        self.assertEqual(c.get("b"), None)
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(c.get("c"), 3)
        self.assertEqual(len(c), 2)

    def test_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)


if __name__ == "__main__":
    unittest.main()
