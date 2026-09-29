"""Format todo items for display."""

PRIORITY_LABELS = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}


def format_todo(todo):
    """Format a single todo as a display string."""
    status = "[x]" if todo.done else "[ ]"
    prio = PRIORITY_LABELS.get(todo.priority, "?")
    tags = ", ".join(todo.tags) if todo.tags else "none"
    line = f"{status} #{todo.todo_id} [{prio}] {todo.title}"
    if todo.description:
        line += f" - {todo.description}"
    line += f" (tags: {tags})"
    if todo.due_date:
        line += f" due:{todo.due_date}"
    return line


def format_list(todos):
    """Format a list of todos, one per line."""
    if not todos:
        return "(no items)"
    return "\n".join(format_todo(t) for t in todos)
