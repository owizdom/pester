You are working in a small Python package, `scheduler/`, in the current directory. Users filed these issues:

1. Overlapping events are silently allowed. `add_event` should raise `ValueError` when a new event overlaps an existing one on the same date.
2. Time parsing only handles the `"HH:MM"` format. Single-digit hours like `"9:30"` raise `ValueError` instead of being accepted.
3. Recurring events (daily and weekly) generate one event past the `end_date`. The last generated event should fall on or before `end_date`, never after it.
4. `delete_event` matches by title substring instead of exact match. Deleting `"Meeting"` also removes `"Team Meeting"`.
5. `events_on_date` does not handle events that span midnight. An event on `"2024-01-15"` from `"23:00"` to `"01:00"` should also appear when querying `"2024-01-16"`.
6. `display.format_day` sorts events by title alphabetically instead of by start time.
7. New feature: add `find_free_slot(date, duration_minutes)` to `Calendar`. It should return a `(start, end)` tuple of `"HH:MM"` strings for the earliest available slot of the requested duration on that date, or `None` if no slot fits within 24 hours.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
