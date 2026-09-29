"""Filtering utilities for todo items."""
from datetime import datetime, date


def filter_by_tag(todos, tag):
    """Return todos that have the given tag, case-insensitive."""
    tag_lower = tag.lower()
    return [t for t in todos
            if any(tg.lower() == tag_lower for tg in t.tags)]


def filter_overdue(todos):
    """Return todos that are past their due date and not done."""
    today = date.today()
    results = []
    for t in todos:
        if t.done or not t.due_date:
            continue
        if isinstance(t.due_date, str):
            due = date.fromisoformat(t.due_date)
        else:
            due = t.due_date
        if due < today:
            results.append(t)
    return results
