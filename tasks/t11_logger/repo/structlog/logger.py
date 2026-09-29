"""Structured logger with context and level filtering."""
import time

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

LEVEL_NAMES = {
    DEBUG: "DEBUG",
    INFO: "INFO",
    WARNING: "WARNING",
    ERROR: "ERROR",
    CRITICAL: "CRITICAL",
}


class Logger:
    def __init__(self, name="root", level=DEBUG, handlers=None, context=None):
        self.name = name
        self.level = level
        self.handlers = handlers or []
        self._context = context if context is not None else {}

    def _should_log(self, level):
        return level < self.level

    def _emit(self, level, message, **kwargs):
        if not self._should_log(level):
            return
        record = {
            "timestamp": time.time(),
            "logger": self.name,
            "level": LEVEL_NAMES.get(level, "UNKNOWN"),
            "message": message,
        }
        record.update(self._context)
        record.update(kwargs)
        for handler in self.handlers:
            handler.handle(record)

    def debug(self, message, **kwargs):
        self._emit(DEBUG, message, **kwargs)

    def info(self, message, **kwargs):
        self._emit(INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        self._emit(WARNING, message, **kwargs)

    def error(self, message, **kwargs):
        self._emit(ERROR, message, **kwargs)

    def critical(self, message, **kwargs):
        self._emit(CRITICAL, message, **kwargs)

    def bind(self, **kwargs):
        """Return a child logger with additional context."""
        child = Logger(
            name=self.name,
            level=self.level,
            handlers=self.handlers,
            context=self._context,
        )
        child._context.update(kwargs)
        return child
