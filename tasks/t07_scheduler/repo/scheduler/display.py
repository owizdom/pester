"""Display formatting for calendar events.

Provides human-readable text output for calendar views
including single-day and full-week summaries.
"""
from datetime import datetime, timedelta


def format_day(events):
    """Format a list of events for one day.

    Events are displayed one per line as 'START-END TITLE'.
    The list should be sorted by start time, but currently
    sorts by title instead.
    """
    sorted_events = sorted(events, key=lambda e: e.title)
    lines = []
    for e in sorted_events:
        lines.append(f"{e.start}-{e.end} {e.title}")
    return "\n".join(lines)


def format_week(calendar, start_date):
    """Format a full week of events starting from start_date.

    Days with no events are omitted. Each day with events gets
    a header line followed by the formatted day output.
    Returns a single string with newline separators.
    """
    lines = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    for _ in range(7):
        date_str = current.strftime("%Y-%m-%d")
        day_events = calendar.events_on_date(date_str)
        if day_events:
            lines.append(f"--- {date_str} ---")
            lines.append(format_day(day_events))
        current += timedelta(days=1)
    return "\n".join(lines)
