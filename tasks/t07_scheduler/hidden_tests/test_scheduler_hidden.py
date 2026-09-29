import unittest

from scheduler.event import Event, parse_time
from scheduler.calendar import Calendar
from scheduler.recurrence import daily_events, weekly_events
from scheduler.display import format_day


class TestParseTime(unittest.TestCase):
    def test_single_digit_hour(self):
        h, m = parse_time("9:30")
        self.assertEqual((h, m), (9, 30))

    def test_standard_format(self):
        h, m = parse_time("14:05")
        self.assertEqual((h, m), (14, 5))


class TestOverlap(unittest.TestCase):
    def test_overlap_raises(self):
        cal = Calendar()
        cal.add_event("A", "2024-01-15", "10:00", "11:00")
        with self.assertRaises(ValueError):
            cal.add_event("B", "2024-01-15", "10:30", "11:30")

    def test_adjacent_events_ok(self):
        cal = Calendar()
        cal.add_event("A", "2024-01-15", "10:00", "11:00")
        cal.add_event("B", "2024-01-15", "11:00", "12:00")
        self.assertEqual(len(cal.all_events()), 2)


class TestDeleteEvent(unittest.TestCase):
    def test_exact_match_only(self):
        cal = Calendar()
        cal.add_event("Team Meeting", "2024-01-15", "10:00", "11:00")
        cal.add_event("Meeting", "2024-01-16", "14:00", "15:00")
        cal.delete_event("Meeting")
        titles = [e.title for e in cal.all_events()]
        self.assertIn("Team Meeting", titles)
        self.assertNotIn("Meeting", titles)


class TestEventsOnDate(unittest.TestCase):
    def test_midnight_spanning(self):
        cal = Calendar()
        cal.add_event("Night Shift", "2024-01-15", "23:00", "01:00")
        events = cal.events_on_date("2024-01-16")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "Night Shift")


class TestRecurrence(unittest.TestCase):
    def test_daily_respects_end_date(self):
        events = daily_events("Standup", "2024-01-15", "2024-01-17",
                              "09:00", "09:15")
        dates = [e.date for e in events]
        self.assertEqual(dates, ["2024-01-15", "2024-01-16", "2024-01-17"])

    def test_weekly_respects_end_date(self):
        events = weekly_events("Weekly", "2024-01-15", "2024-01-28",
                               "10:00", "11:00", 0)
        dates = [e.date for e in events]
        self.assertEqual(dates, ["2024-01-15", "2024-01-22"])


class TestFormatDay(unittest.TestCase):
    def test_sorted_by_start_time(self):
        e1 = Event("Alpha", "2024-01-15", "14:00", "15:00")
        e2 = Event("Bravo", "2024-01-15", "09:00", "10:00")
        result = format_day([e1, e2])
        lines = result.split("\n")
        self.assertTrue(lines[0].startswith("09:00"))
        self.assertTrue(lines[1].startswith("14:00"))


class TestFindFreeSlot(unittest.TestCase):
    def test_empty_day(self):
        cal = Calendar()
        slot = cal.find_free_slot("2024-01-15", 60)
        self.assertIsNotNone(slot)
        self.assertEqual(slot, ("00:00", "01:00"))

    def test_finds_gap_between_events(self):
        cal = Calendar()
        cal.add_event("A", "2024-01-15", "00:00", "09:00")
        cal.add_event("B", "2024-01-15", "10:00", "11:00")
        slot = cal.find_free_slot("2024-01-15", 60)
        self.assertIsNotNone(slot)
        self.assertEqual(slot, ("09:00", "10:00"))

    def test_no_room(self):
        cal = Calendar()
        cal.add_event("All Day", "2024-01-15", "00:00", "23:59")
        slot = cal.find_free_slot("2024-01-15", 120)
        self.assertIsNone(slot)


if __name__ == "__main__":
    unittest.main()
