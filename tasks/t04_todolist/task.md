You are working in a small Python package, `todolist/`, in the current directory. Users filed these issues:

1. Priority sort is reversed: `get_sorted_by_priority()` returns low-priority items first. High priority (3) should come before medium (2) and low (1).
2. Marking a todo as done does not update the completion timestamp. `mark_done(todo_id)` should set `completed_at` to `datetime.now()` when marking an item complete.
3. Filter by tag is case-sensitive: `filter_by_tag("Work")` misses items tagged `"work"`. Tag filtering should be case-insensitive.
4. Overdue detection compares date strings instead of date objects. Items with `due_date` in the past should be detected as overdue regardless of string format.
5. `add_todo` allows an empty title (empty string or whitespace). It should raise `ValueError` if the title is empty or whitespace-only.
6. `delete` raises `RuntimeError` for a missing ID. It should raise `KeyError` instead.
7. New feature: add `search(keyword)` to the store module. It should return all todos whose title or description contains the keyword, case-insensitive, sorted by creation date (oldest first).

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
