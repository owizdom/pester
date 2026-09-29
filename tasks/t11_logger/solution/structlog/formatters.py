"""Format log records into strings."""
import json
import time
from datetime import datetime, date


class TextFormatter:
    """Simple text formatter."""

    def __init__(self, fmt=None):
        self.fmt = fmt or "{timestamp} [{level}] {message}"

    def format(self, record):
        ts = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(record["timestamp"])
        )
        return self.fmt.format(
            timestamp=ts,
            level=record["level"],
            logger=record["logger"],
            message=record["message"],
        )


def _json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(
        f"Object of type {type(obj).__name__} is not JSON serializable"
    )


class JsonFormatter:
    """JSON formatter for structured logging."""

    def format(self, record):
        return json.dumps(record, default=_json_default)
