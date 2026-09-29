You are working in a small Python package, `structlog/`, in the current directory. Users filed these issues:

1. Log level filtering is inverted. Setting the level to `ERROR` should suppress `DEBUG` and `INFO` messages, but currently it lets them through and blocks `ERROR` messages instead.
2. `FileHandler` crashes when the log file's parent directory does not exist. It should create parent directories automatically.
3. `JsonFormatter` crashes with `TypeError` when a log record contains `datetime` objects. It should serialize them to ISO format strings.
4. Calling `bind()` to create a child logger with extra context fields mutates the parent logger's context. Child loggers should have independent context.
5. `RotatingFileHandler` compares the formatted message length against `max_bytes` instead of checking the actual file size on disk. Rotation should trigger based on the real file size.
6. New feature: `RateLimiter(logger, max_per_minute)` wrapper class that passes through log calls but suppresses duplicate messages (same message text) beyond the limit within a 60-second sliding window.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
