"""Todo item data model."""
from datetime import datetime


class Todo:
    def __init__(self, todo_id, title, description="", priority=1,
                 tags=None, due_date=None):
        self.todo_id = todo_id
        self.title = title
        self.description = description
        self.priority = priority  # 1=low, 2=medium, 3=high
        self.tags = tags or []
        self.due_date = due_date  # expects a date string "YYYY-MM-DD"
        self.done = False
        self.completed_at = None
        self.created_at = datetime.now()

    def mark_done(self):
        self.done = True
        self.completed_at = datetime.now()

    def __repr__(self):
        status = "done" if self.done else "pending"
        return f"Todo({self.todo_id!r}, {self.title!r}, {status})"
