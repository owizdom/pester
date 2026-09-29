"""In-memory todo storage with add, delete, and retrieval."""
from todolist.models import Todo


class TodoStore:
    def __init__(self):
        self._todos = {}
        self._next_id = 1

    def add_todo(self, title, description="", priority=1, tags=None,
                 due_date=None):
        if not title or not title.strip():
            raise ValueError("title must not be empty")
        todo = Todo(self._next_id, title, description, priority, tags,
                    due_date)
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id):
        if todo_id not in self._todos:
            raise KeyError(f"no todo with id {todo_id}")
        return self._todos[todo_id]

    def delete(self, todo_id):
        if todo_id not in self._todos:
            raise KeyError(f"no todo with id {todo_id}")
        del self._todos[todo_id]

    def mark_done(self, todo_id):
        self.get(todo_id).mark_done()

    def all_todos(self):
        return list(self._todos.values())

    def get_sorted_by_priority(self):
        return sorted(self._todos.values(), key=lambda t: t.priority,
                      reverse=True)

    def search(self, keyword):
        """Return todos matching keyword in title or description,
        case-insensitive, sorted by creation date (oldest first)."""
        kw = keyword.lower()
        matches = [t for t in self._todos.values()
                   if kw in t.title.lower() or kw in t.description.lower()]
        return sorted(matches, key=lambda t: t.created_at)
