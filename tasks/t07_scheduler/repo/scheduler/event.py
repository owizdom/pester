"""Event data model."""


def parse_time(s):
    """Parse a time string like '14:00' or '9:30' into (hour, minute)."""
    if len(s) != 5 or s[2] != ":":
        raise ValueError(f"invalid time format: {s}")
    return int(s[:2]), int(s[3:])


def time_to_minutes(s):
    """Convert a time string to minutes since midnight."""
    h, m = parse_time(s)
    return h * 60 + m


def minutes_to_time(mins):
    """Convert minutes since midnight to 'HH:MM' string."""
    return f"{mins // 60:02d}:{mins % 60:02d}"


class Event:
    """A calendar event on a single date."""

    def __init__(self, title, date, start, end):
        self.title = title
        self.date = date
        self.start = start
        self.end = end
        self.start_minutes = time_to_minutes(start)
        self.end_minutes = time_to_minutes(end)

    def overlaps(self, other):
        """Return True if this event overlaps with another on the same date."""
        if self.date != other.date:
            return False
        return (self.start_minutes < other.end_minutes
                and other.start_minutes < self.end_minutes)

    def __repr__(self):
        return f"Event({self.title!r}, {self.date}, {self.start}-{self.end})"
