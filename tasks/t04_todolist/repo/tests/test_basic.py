import unittest

from todolist.store import TodoStore
from todolist.formatting import format_todo


class BasicTest(unittest.TestCase):
    def test_add_and_get(self):
        store = TodoStore()
        todo = store.add_todo("Buy milk")
        self.assertEqual(store.get(todo.todo_id).title, "Buy milk")

    def test_format_todo(self):
        store = TodoStore()
        todo = store.add_todo("Read book", priority=2)
        text = format_todo(todo)
        self.assertIn("Read book", text)
        self.assertIn("MEDIUM", text)


if __name__ == "__main__":
    unittest.main()
