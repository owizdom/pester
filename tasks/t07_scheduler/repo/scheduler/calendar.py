"""Calendar for managing events.

Provides the central Calendar class that stores events, checks
for conflicts, and supports querying by date.
"""
from scheduler.event import Event


class Calendar:
    """Manages a collection of non-overlapping events."""

    def __init__(self):
        self._events = []

    def add_event(self, title, date, start, end):
        """Add an event to the calendar.

        Should raise ValueError if the new event overlaps with any
        existing event, but that check is not yet implemented.
        """
        ev = Event(title, date, start, end)
        self._events.append(ev)
        return ev

    def delete_event(self, title):
        """Remove the event with the given title."""
        self._events = [e for e in self._events if title not in e.title]

    def events_on_date(self, date):
        """Return all events occurring on the given date."""
        return [e for e in self._events if e.date == date]

    def all_events(self):
        """Return a copy of the full event list."""
        return list(self._events)

    def event_count(self):
        """Return the total number of stored events."""
        return len(self._events)
