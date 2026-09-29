import os
import unittest

from configparser_ext.parser import parse
from configparser_ext.interpolation import interpolate, interpolate_section
from configparser_ext.section import Section


class InheritanceHidden(unittest.TestCase):
    def test_child_inherits_parent_keys(self):
        cfg = parse("[base]\ncolor = red\nsize = 10\n\n[child : base]\nsize = 20\n")
        child = cfg["child"]
        self.assertEqual(child.get("color"), "red")
        self.assertEqual(child.get("size"), "20")

    def test_parent_unchanged_after_inheritance(self):
        cfg = parse("[base]\na = 1\n\n[child : base]\na = 2\nb = 3\n")
        self.assertEqual(cfg["base"].get("a"), "1")
        self.assertIsNone(cfg["base"].get("b"))

    def test_missing_parent_no_crash(self):
        cfg = parse("[child : ghost]\nkey = val\n")
        self.assertEqual(cfg["child"].get("key"), "val")


class InterpolationHidden(unittest.TestCase):
    def test_recursive_interpolation(self):
        sec = Section("s", {"a": "${b}", "b": "${c}", "c": "done"})
        interpolate_section(sec)
        self.assertEqual(sec.get("a"), "done")

    def test_env_var_interpolation(self):
        os.environ["_CFGTEST_VAR"] = "from_env"
        try:
            sec = Section("s", {"x": "${ENV:_CFGTEST_VAR}"})
            interpolate_section(sec)
            self.assertEqual(sec.get("x"), "from_env")
        finally:
            del os.environ["_CFGTEST_VAR"]

    def test_unknown_ref_kept(self):
        sec = Section("s", {"a": "${missing}"})
        interpolate_section(sec)
        self.assertEqual(sec.get("a"), "${missing}")


class BooleanHidden(unittest.TestCase):
    def test_truthy_variants(self):
        cfg = parse("[f]\na = yes\nb = on\nc = 1\nd = TRUE\n")
        for k in "abcd":
            self.assertTrue(cfg["f"].getboolean(k), f"key {k} should be True")

    def test_falsy_variants(self):
        cfg = parse("[f]\na = no\nb = off\nc = 0\nd = FALSE\n")
        for k in "abcd":
            self.assertFalse(cfg["f"].getboolean(k), f"key {k} should be False")

    def test_invalid_raises(self):
        cfg = parse("[f]\na = maybe\n")
        with self.assertRaises(ValueError):
            cfg["f"].getboolean("a")


class MultilineHidden(unittest.TestCase):
    def test_continuation_joined(self):
        text = "[s]\ngreeting = hello\n  world\n  again\n"
        cfg = parse(text)
        self.assertEqual(cfg["s"].get("greeting"), "hello\nworld\nagain")
        text2 = "[s]\nval = line1\n\tline2\n"
        cfg2 = parse(text2)
        self.assertEqual(cfg2["s"].get("val"), "line1\nline2")


class InlineCommentHidden(unittest.TestCase):
    def test_comment_stripped(self):
        cfg = parse("[s]\nname = alice # the user\nport = 8080 ; default\n")
        self.assertEqual(cfg["s"].get("name"), "alice")
        self.assertEqual(cfg["s"].get("port"), "8080")

    def test_quoted_hash_kept(self):
        cfg = parse('[s]\ncolor = "red # not a comment"\n')
        self.assertEqual(cfg["s"].get("color"), '"red # not a comment"')


class GetEnvHidden(unittest.TestCase):
    def test_key_present(self):
        from configparser_ext.parser import get_env
        cfg = parse("[db]\nhost = localhost\n")
        self.assertEqual(get_env(cfg, "db", "host", "DB_HOST"), "localhost")

    def test_falls_back_to_env(self):
        from configparser_ext.parser import get_env
        os.environ["_CFGTEST_FALLBACK"] = "envval"
        try:
            cfg = parse("[db]\nhost = localhost\n")
            self.assertEqual(get_env(cfg, "db", "port", "_CFGTEST_FALLBACK"), "envval")
        finally:
            del os.environ["_CFGTEST_FALLBACK"]

    def test_missing_both_returns_none(self):
        from configparser_ext.parser import get_env
        cfg = parse("[db]\nhost = localhost\n")
        self.assertIsNone(get_env(cfg, "db", "missing_key", "_CFGTEST_NOEXIST"))


if __name__ == "__main__":
    unittest.main()
