import json
import os
import shutil
import tempfile
import time
import unittest
from datetime import datetime

from structlog.logger import Logger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from structlog.handlers import ListHandler, FileHandler, RotatingFileHandler
from structlog.formatters import JsonFormatter, TextFormatter


class LevelFilterHidden(unittest.TestCase):
    def test_error_level_blocks_debug(self):
        h = ListHandler()
        log = Logger(handlers=[h], level=ERROR)
        log.debug("nope")
        log.info("nope")
        self.assertEqual(len(h.records), 0)

    def test_error_level_passes_error(self):
        h = ListHandler()
        log = Logger(handlers=[h], level=ERROR)
        log.error("yes")
        log.critical("also yes")
        self.assertEqual(len(h.records), 2)

    def test_debug_level_passes_all(self):
        h = ListHandler()
        log = Logger(handlers=[h], level=DEBUG)
        log.debug("d")
        log.info("i")
        log.warning("w")
        log.error("e")
        log.critical("c")
        self.assertEqual(len(h.records), 5)

    def test_warning_level_boundary(self):
        h = ListHandler()
        log = Logger(handlers=[h], level=WARNING)
        log.debug("no")
        log.info("no")
        log.warning("yes")
        self.assertEqual(len(h.records), 1)
        self.assertEqual(h.records[0]["level"], "WARNING")


class BindContextHidden(unittest.TestCase):
    def test_child_does_not_mutate_parent(self):
        h = ListHandler()
        parent = Logger(handlers=[h], level=DEBUG)
        child = parent.bind(request_id="abc")
        parent.info("from parent")
        self.assertNotIn("request_id", parent._context)

    def test_child_has_own_context(self):
        h = ListHandler()
        parent = Logger(handlers=[h], level=DEBUG)
        child = parent.bind(user="alice")
        child.info("hello")
        self.assertEqual(h.records[0].get("user"), "alice")

    def test_nested_bind_independence(self):
        h = ListHandler()
        root = Logger(handlers=[h], level=DEBUG)
        c1 = root.bind(a=1)
        c2 = c1.bind(b=2)
        self.assertNotIn("b", c1._context)
        self.assertNotIn("a", root._context)


class FileHandlerHidden(unittest.TestCase):
    def test_creates_parent_dirs(self):
        d = tempfile.mkdtemp()
        try:
            path = os.path.join(d, "sub", "deep", "app.log")
            fh = FileHandler(path)
            fh.handle({"message": "test"})
            fh.close()
            self.assertTrue(os.path.exists(path))
            with open(path) as f:
                self.assertIn("test", f.read())
        finally:
            shutil.rmtree(d)


class JsonFormatterHidden(unittest.TestCase):
    def test_datetime_serialization(self):
        fmt = JsonFormatter()
        record = {
            "timestamp": time.time(),
            "logger": "root",
            "level": "INFO",
            "message": "hi",
            "created_at": datetime(2024, 1, 15, 10, 30, 0),
        }
        text = fmt.format(record)
        data = json.loads(text)
        self.assertEqual(data["created_at"], "2024-01-15T10:30:00")

    def test_plain_record_still_works(self):
        fmt = JsonFormatter()
        record = {
            "timestamp": 1000000.0,
            "level": "DEBUG",
            "message": "ok",
            "logger": "test",
        }
        text = fmt.format(record)
        data = json.loads(text)
        self.assertEqual(data["message"], "ok")


class RotatingHandlerHidden(unittest.TestCase):
    def test_rotates_by_file_size(self):
        d = tempfile.mkdtemp()
        try:
            path = os.path.join(d, "app.log")
            rh = RotatingFileHandler(path, max_bytes=100)
            for i in range(20):
                rh.handle({"message": f"line {i:04d} padding"})
            rh.close()
            self.assertTrue(os.path.exists(path + ".1"))
            main_size = os.path.getsize(path)
            self.assertLessEqual(main_size, 200)
        finally:
            shutil.rmtree(d)


class RateLimiterHidden(unittest.TestCase):
    def test_suppresses_beyond_limit(self):
        from structlog.logger import RateLimiter

        h = ListHandler()
        log = Logger(handlers=[h], level=DEBUG)
        rl = RateLimiter(log, max_per_minute=3)
        for _ in range(10):
            rl.info("spam")
        self.assertEqual(len(h.records), 3)

    def test_different_messages_independent(self):
        from structlog.logger import RateLimiter

        h = ListHandler()
        log = Logger(handlers=[h], level=DEBUG)
        rl = RateLimiter(log, max_per_minute=2)
        for _ in range(5):
            rl.info("aaa")
            rl.info("bbb")
        self.assertEqual(len(h.records), 4)

    def test_rate_limiter_all_levels(self):
        from structlog.logger import RateLimiter

        h = ListHandler()
        log = Logger(handlers=[h], level=DEBUG)
        rl = RateLimiter(log, max_per_minute=1)
        rl.debug("x")
        rl.debug("x")
        rl.warning("y")
        rl.warning("y")
        rl.error("z")
        rl.error("z")
        self.assertEqual(len(h.records), 3)


if __name__ == "__main__":
    unittest.main()
