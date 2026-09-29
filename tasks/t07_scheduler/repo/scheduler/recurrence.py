"""Recurring event generation."""
from datetime import datetime, timedelta

from scheduler.event import Event


def daily_events(title, start_date, end_date, start_time, end_time):
    """Generate daily recurring events from start_date through end_date."""
    events = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    while current <= end + timedelta(days=1):
        events.append(Event(title, current.strftime("%Y-%m-%d"),
                            start_time, end_time))
        current += timedelta(days=1)
    return events


def weekly_events(title, start_date, end_date, start_time, end_time, weekday):
    """Generate weekly events on a given weekday (0=Mon through 6=Sun)."""
    events = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    while current.weekday() != weekday:
        current += timedelta(days=1)
    while current <= end + timedelta(days=1):
        events.append(Event(title, current.strftime("%Y-%m-%d"),
                            start_time, end_time))
        current += timedelta(days=7)
    return events
