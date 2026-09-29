"""Calendar for managing events.

Provides the central Calendar class that stores events, checks
for conflicts, and supports querying by date.
"""
from datetime import datetime, timedelta

from scheduler.event import Event, minutes_to_time


class Calendar:
    """Manages a collection of non-overlapping events."""

    def __init__(self):
        self._events = []

    def add_event(self, title, date, start, end):
        """Add an event, raising ValueError on overlap."""
        ev = Event(title, date, start, end)
        for existing in self._events:
            if ev.overlaps(existing):
                raise ValueError(
                    f"'{title}' overlaps with '{existing.title}'")
        self._events.append(ev)
        return ev

    def delete_event(self, title):
        """Remove the event whose title matches exactly."""
        self._events = [e for e in self._events if e.title != title]

    def events_on_date(self, date):
        """Return all events occurring on the given date.

        Includes events from the previous day that span midnight.
        """
        result = []
        for e in self._events:
            if e.date == date:
                result.append(e)
            elif e.end_minutes <= e.start_minutes:
                ev_date = datetime.strptime(e.date, "%Y-%m-%d").date()
                query_date = datetime.strptime(date, "%Y-%m-%d").date()
                if query_date == ev_date + timedelta(days=1):
                    result.append(e)
        return result

    def all_events(self):
        """Return a copy of the full event list."""
        return list(self._events)

    def event_count(self):
        """Return the total number of stored events."""
        return len(self._events)

    def find_free_slot(self, date, duration_minutes):
        """Find the earliest available slot of the given duration on date.

        Returns a (start, end) tuple of 'HH:MM' strings, or None.
        """
        events = self.events_on_date(date)
        occupied = []
        for e in events:
            if e.date == date:
                occupied.append((e.start_minutes, e.end_minutes))
            else:
                occupied.append((0, e.end_minutes))
        occupied.sort()

        current = 0
        for occ_start, occ_end in occupied:
            if occ_start - current >= duration_minutes:
                return (minutes_to_time(current),
                        minutes_to_time(current + duration_minutes))
            current = max(current, occ_end)

        if 24 * 60 - current >= duration_minutes:
            return (minutes_to_time(current),
                    minutes_to_time(current + duration_minutes))
        return None
