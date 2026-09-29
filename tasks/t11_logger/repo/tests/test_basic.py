import unittest

from structlog.handlers import ListHandler
from structlog.formatters import TextFormatter


class BasicTest(unittest.TestCase):
    def test_list_handler(self):
        h = ListHandler()
        h.handle({"message": "hi"})
        self.assertEqual(len(h.records), 1)
        self.assertEqual(h.records[0]["message"], "hi")

    def test_text_formatter(self):
        fmt = TextFormatter()
        import time
        rec = {
            "timestamp": time.time(),
            "level": "INFO",
            "logger": "root",
            "message": "hello",
        }
        text = fmt.format(rec)
        self.assertIn("hello", text)
        self.assertIn("[INFO]", text)


if __name__ == "__main__":
    unittest.main()
