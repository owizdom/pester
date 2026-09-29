"""Priority queue that schedules Task objects by priority number."""

import heapq
from taskqueue.task import Task


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._tasks = {}
        self._counter = 0
        self._dependencies = {}

    # ---- mutators ----

    def add(self, task):
        """Insert a task into the queue.  Raises ValueError on duplicate ID."""
        if task.task_id in self._tasks:
            raise ValueError(f"duplicate task ID: {task.task_id}")
        self._tasks[task.task_id] = task
        self._counter += 1
        heapq.heappush(
            self._heap, (task.priority, self._counter, task.task_id)
        )

    def _requeue(self, task):
        """Re-insert a task that is being retried."""
        self._counter += 1
        heapq.heappush(
            self._heap, (task.priority, self._counter, task.task_id)
        )

    def pop(self):
        """Remove and return the highest-priority pending task, or None."""
        skipped = []
        result = None
        while self._heap:
            entry = heapq.heappop(self._heap)
            _, _, task_id = entry
            if task_id not in self._tasks:
                continue
            task = self._tasks[task_id]
            if task.status != "pending":
                continue
            deps = self._dependencies.get(task_id, set())
            unmet = any(
                self._tasks.get(d) is None or self._tasks[d].status != "done"
                for d in deps
            )
            if unmet:
                skipped.append(entry)
                continue
            task.status = "running"
            result = task
            break
        for entry in skipped:
            heapq.heappush(self._heap, entry)
        return result

    def cancel(self, task_id):
        """Mark a task as cancelled so it will not be executed."""
        if task_id not in self._tasks:
            raise KeyError(task_id)
        self._tasks[task_id].status = "cancelled"

    def add_dependency(self, task_id, depends_on_id):
        """Declare that *task_id* cannot run until *depends_on_id* is done."""
        if task_id not in self._tasks:
            raise KeyError(task_id)
        if depends_on_id not in self._tasks:
            raise KeyError(depends_on_id)
        self._dependencies.setdefault(task_id, set()).add(depends_on_id)

    # ---- queries ----

    def get(self, task_id):
        """Return the task object for *task_id*, or raise KeyError."""
        if task_id not in self._tasks:
            raise KeyError(task_id)
        return self._tasks[task_id]

    def pending_count(self):
        """Return the number of tasks still in pending status."""
        return sum(1 for t in self._tasks.values() if t.status == "pending")
