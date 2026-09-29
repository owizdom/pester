import unittest

from scheduler.calendar import Calendar


class BasicTest(unittest.TestCase):
    def test_add_event(self):
        cal = Calendar()
        ev = cal.add_event("Meeting", "2024-01-15", "10:00", "11:00")
        self.assertEqual(ev.title, "Meeting")

    def test_events_on_date(self):
        cal = Calendar()
        cal.add_event("Meeting", "2024-01-15", "10:00", "11:00")
        events = cal.events_on_date("2024-01-15")
        self.assertEqual(len(events), 1)


if __name__ == "__main__":
    unittest.main()
