import unittest

from tokenizer.tokens import Token, NUMBER, STRING, IDENT, OP, NEWLINE, EOF
from tokenizer.lexer import tokenize
from tokenizer.scanner import block_comments


class EscapeTests(unittest.TestCase):
    def test_escape_sequences(self):
        tokens = tokenize(r'"hello \"world\""')
        strings = [t for t in tokens if t.type == STRING]
        self.assertEqual(len(strings), 1)
        self.assertEqual(strings[0].value, 'hello "world"')
        tokens2 = tokenize(r'"a\\b"')
        strings2 = [t for t in tokens2 if t.type == STRING]
        self.assertEqual(strings2[0].value, 'a\\b')


class MultiCharOperatorTests(unittest.TestCase):
    def test_equals_equals(self):
        tokens = tokenize("a == b")
        ops = [t for t in tokens if t.type == OP]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0].value, "==")

    def test_not_equals(self):
        tokens = tokenize("a != b")
        ops = [t for t in tokens if t.type == OP]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0].value, "!=")

    def test_gte_lte(self):
        tokens = tokenize("x >= 1")
        ops = [t for t in tokens if t.type == OP]
        self.assertEqual(ops[0].value, ">=")

        tokens = tokenize("x <= 1")
        ops = [t for t in tokens if t.type == OP]
        self.assertEqual(ops[0].value, "<=")

    def test_single_equals_still_works(self):
        tokens = tokenize("x = 1")
        ops = [t for t in tokens if t.type == OP]
        self.assertEqual(ops[0].value, "=")


class StringWhitespaceTests(unittest.TestCase):
    def test_whitespace_preserved_in_strings(self):
        tokens = tokenize('"hello   world"')
        strings = [t for t in tokens if t.type == STRING]
        self.assertEqual(strings[0].value, "hello   world")
        tokens2 = tokenize('"a\tb"')
        strings2 = [t for t in tokens2 if t.type == STRING]
        self.assertIn('\t', strings2[0].value)


class LineNumberTests(unittest.TestCase):
    def test_line_after_multiline_string(self):
        src = '"line1\nline2"\nx'
        tokens = tokenize(src)
        ident = [t for t in tokens if t.type == IDENT]
        self.assertEqual(ident[0].value, "x")
        self.assertEqual(ident[0].line, 3)

    def test_simple_newline_tracking(self):
        tokens = tokenize("a\nb")
        idents = [t for t in tokens if t.type == IDENT]
        self.assertEqual(idents[0].line, 1)
        self.assertEqual(idents[1].line, 2)


class EOFTests(unittest.TestCase):
    def test_eof_emitted(self):
        tokens = tokenize("x")
        self.assertEqual(tokens[-1].type, EOF)
        self.assertEqual(tokens[-1].value, "")

    def test_eof_on_empty(self):
        tokens = tokenize("")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, EOF)

    def test_eof_line_number(self):
        tokens = tokenize("a\nb\n")
        self.assertEqual(tokens[-1].type, EOF)
        self.assertEqual(tokens[-1].line, 3)


class BlockCommentTests(unittest.TestCase):
    def test_simple_block_comment(self):
        self.assertEqual(block_comments("a /* comment */ b"), "a  b")

    def test_nested_block_comment(self):
        self.assertEqual(
            block_comments("a /* outer /* inner */ still */ b"),
            "a  b",
        )

    def test_no_comment(self):
        self.assertEqual(block_comments("hello world"), "hello world")

    def test_comment_at_edges(self):
        self.assertEqual(block_comments("/* start */middle/* end */"), "middle")


if __name__ == "__main__":
    unittest.main()
