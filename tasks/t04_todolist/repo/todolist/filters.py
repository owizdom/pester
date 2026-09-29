"""Filtering utilities for todo items."""
from datetime import datetime


def filter_by_tag(todos, tag):
    """Return todos that have the given tag. Should be case-insensitive."""
    # Bug: case-sensitive comparison
    return [t for t in todos if tag in t.tags]


def filter_overdue(todos):
    """Return todos that are past their due date and not done."""
    now = datetime.now().strftime("%Y-%m-%d")
    # Bug: compares date strings instead of date objects
    return [t for t in todos if not t.done and t.due_date and t.due_date < now]
