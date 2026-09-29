import unittest

from textdiff.lcs import lcs_length, lcs
from textdiff.diff import unified_diff

try:
    from textdiff.diff import word_diff
except ImportError:
    word_diff = None


class LcsHidden(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(lcs_length([], []), 0)
        self.assertEqual(lcs_length("abc", ""), 0)
        self.assertEqual(lcs_length("", "xyz"), 0)

    def test_lcs_subsequence(self):
        self.assertEqual(lcs("abcde", "ace"), ["a", "c", "e"])

    def test_lcs_length_normal(self):
        self.assertEqual(lcs_length("abcde", "ace"), 3)


class DiffHeaderHidden(unittest.TestCase):
    def test_header_present(self):
        result = unified_diff(["a"], ["b"], old_name="old.txt", new_name="new.txt")
        lines = result.split("\n")
        self.assertTrue(any(l.startswith("--- ") for l in lines))
        self.assertTrue(any(l.startswith("+++ ") for l in lines))
        self.assertIn("old.txt", result)
        self.assertIn("new.txt", result)


class LineNumbersHidden(unittest.TestCase):
    def test_one_indexed(self):
        old = ["alpha", "beta", "gamma"]
        new = ["alpha", "BETA", "gamma"]
        result = unified_diff(old, new)
        for line in result.split("\n"):
            if line.startswith("@@"):
                self.assertIn("-1,", line)
                self.assertIn("+1,", line)
                break
        else:
            self.fail("no @@ header found")


class SymbolsHidden(unittest.TestCase):
    def test_removed_line_has_minus(self):
        old = ["hello", "world"]
        new = ["hello"]
        result = unified_diff(old, new)
        data_lines = [l for l in result.split("\n")
                      if not l.startswith("@@") and not l.startswith("---") and not l.startswith("+++")]
        removed = [l for l in data_lines if l.startswith("-")]
        self.assertTrue(any("world" in l for l in removed),
                        f"expected '-world' in output, got: {result}")

    def test_added_line_has_plus(self):
        old = ["hello"]
        new = ["hello", "world"]
        result = unified_diff(old, new)
        data_lines = [l for l in result.split("\n")
                      if not l.startswith("@@") and not l.startswith("---") and not l.startswith("+++")]
        added = [l for l in data_lines if l.startswith("+")]
        self.assertTrue(any("world" in l for l in added),
                        f"expected '+world' in output, got: {result}")


class ContextOverlapHidden(unittest.TestCase):
    def test_close_changes_merged(self):
        old = ["a", "b", "c", "d", "e", "f"]
        new = ["a", "X", "c", "d", "Y", "f"]
        result = unified_diff(old, new)
        hunk_headers = [l for l in result.split("\n") if l.startswith("@@")]
        self.assertEqual(len(hunk_headers), 1,
                         f"expected 1 hunk, got {len(hunk_headers)}: {result}")


class IdenticalHidden(unittest.TestCase):
    def test_identical_returns_empty(self):
        result = unified_diff(["a", "b"], ["a", "b"])
        self.assertEqual(result, "")


class WordDiffHidden(unittest.TestCase):
    def test_basic(self):
        if word_diff is None:
            self.fail("word_diff not implemented")
        result = word_diff("the cat sat", "the dog sat")
        types = [t for t, _ in result]
        words = [w for _, w in result]
        self.assertIn("equal", types)
        self.assertIn("remove", types)
        self.assertIn("add", types)
        self.assertIn("the", words)
        self.assertIn("cat", words)
        self.assertIn("dog", words)

    def test_all_different(self):
        if word_diff is None:
            self.fail("word_diff not implemented")
        result = word_diff("a b", "x y")
        removes = [w for t, w in result if t == "remove"]
        adds = [w for t, w in result if t == "add"]
        self.assertEqual(set(removes), {"a", "b"})
        self.assertEqual(set(adds), {"x", "y"})

    def test_identical(self):
        if word_diff is None:
            self.fail("word_diff not implemented")
        result = word_diff("one two three", "one two three")
        self.assertTrue(all(t == "equal" for t, _ in result))
        self.assertEqual([w for _, w in result], ["one", "two", "three"])


if __name__ == "__main__":
    unittest.main()
