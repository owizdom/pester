"""Log handlers for writing records to destinations."""
import os


class ListHandler:
    """Accumulate records in a list (for testing)."""

    def __init__(self):
        self.records = []

    def handle(self, record):
        self.records.append(record)


class FileHandler:
    """Write formatted records to a file."""

    def __init__(self, path, formatter=None):
        self.path = path
        self.formatter = formatter
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._file = open(path, "a")

    def handle(self, record):
        text = self.formatter.format(record) if self.formatter else str(record)
        self._file.write(text + "\n")
        self._file.flush()

    def close(self):
        self._file.close()


class RotatingFileHandler:
    """Write to a file, rotating when it exceeds max_bytes."""

    def __init__(self, path, formatter=None, max_bytes=1_000_000):
        self.path = path
        self.formatter = formatter
        self.max_bytes = max_bytes
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._ensure_open()

    def _ensure_open(self):
        self._file = open(self.path, "a")

    def _rotate(self):
        self._file.close()
        backup = self.path + ".1"
        if os.path.exists(backup):
            os.remove(backup)
        os.rename(self.path, backup)
        self._ensure_open()

    def handle(self, record):
        text = self.formatter.format(record) if self.formatter else str(record)
        size = os.path.getsize(self.path)
        if size + len(text.encode()) + 1 > self.max_bytes:
            self._rotate()
        self._file.write(text + "\n")
        self._file.flush()

    def close(self):
        self._file.close()
