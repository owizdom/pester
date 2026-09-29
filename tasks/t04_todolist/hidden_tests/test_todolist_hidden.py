import unittest
import time
from datetime import date, timedelta

from todolist.store import TodoStore
from todolist.filters import filter_by_tag, filter_overdue


class PrioritySortHidden(unittest.TestCase):
    def test_high_first(self):
        store = TodoStore()
        store.add_todo("Low task", priority=1)
        store.add_todo("High task", priority=3)
        store.add_todo("Medium task", priority=2)
        result = store.get_sorted_by_priority()
        priorities = [t.priority for t in result]
        self.assertEqual(priorities, [3, 2, 1])


class MarkDoneHidden(unittest.TestCase):
    def test_completed_at_set(self):
        store = TodoStore()
        todo = store.add_todo("Test task")
        self.assertIsNone(todo.completed_at)
        store.mark_done(todo.todo_id)
        self.assertIsNotNone(todo.completed_at)
        self.assertTrue(todo.done)


class TagFilterHidden(unittest.TestCase):
    def test_case_insensitive(self):
        store = TodoStore()
        store.add_todo("Task A", tags=["Work"])
        store.add_todo("Task B", tags=["work"])
        store.add_todo("Task C", tags=["personal"])
        result = filter_by_tag(store.all_todos(), "WORK")
        self.assertEqual(len(result), 2)

    def test_no_match(self):
        store = TodoStore()
        store.add_todo("Task A", tags=["home"])
        result = filter_by_tag(store.all_todos(), "work")
        self.assertEqual(len(result), 0)


class OverdueHidden(unittest.TestCase):
    def test_overdue_uses_date_comparison(self):
        store = TodoStore()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        store.add_todo("Past", due_date=yesterday)
        store.add_todo("Future", due_date=tomorrow)
        overdue = filter_overdue(store.all_todos())
        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0].title, "Past")

    def test_done_not_overdue(self):
        store = TodoStore()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        todo = store.add_todo("Done past", due_date=yesterday)
        store.mark_done(todo.todo_id)
        overdue = filter_overdue(store.all_todos())
        self.assertEqual(len(overdue), 0)


class EmptyTitleHidden(unittest.TestCase):
    def test_empty_string_raises(self):
        store = TodoStore()
        with self.assertRaises(ValueError):
            store.add_todo("")

    def test_whitespace_only_raises(self):
        store = TodoStore()
        with self.assertRaises(ValueError):
            store.add_todo("   ")


class DeleteHidden(unittest.TestCase):
    def test_missing_raises_key_error(self):
        store = TodoStore()
        with self.assertRaises(KeyError):
            store.delete(999)

    def test_delete_works(self):
        store = TodoStore()
        todo = store.add_todo("To remove")
        store.delete(todo.todo_id)
        with self.assertRaises(KeyError):
            store.get(todo.todo_id)


class SearchHidden(unittest.TestCase):
    def test_search_title(self):
        store = TodoStore()
        store.add_todo("Buy groceries")
        store.add_todo("Read a book")
        result = store.search("buy")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Buy groceries")

    def test_search_description(self):
        store = TodoStore()
        store.add_todo("Task", description="needs groceries from store")
        result = store.search("GROCERIES")
        self.assertEqual(len(result), 1)

    def test_search_sorted_by_created(self):
        store = TodoStore()
        store.add_todo("Alpha report")
        time.sleep(0.01)
        store.add_todo("Beta report")
        result = store.search("report")
        self.assertEqual(result[0].title, "Alpha report")
        self.assertEqual(result[1].title, "Beta report")


if __name__ == "__main__":
    unittest.main()
