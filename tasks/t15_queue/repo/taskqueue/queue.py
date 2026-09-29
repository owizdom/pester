"""Priority queue that schedules Task objects by priority number."""

import heapq
from taskqueue.task import Task


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._tasks = {}
        self._counter = 0

    # ---- mutators ----

    def add(self, task):
        """Insert a task into the queue."""
        self._tasks[task.task_id] = task
        self._counter += 1
        heapq.heappush(
            self._heap, (-task.priority, self._counter, task.task_id)
        )

    def _requeue(self, task):
        """Re-insert a task that is being retried."""
        self._counter += 1
        heapq.heappush(
            self._heap, (-task.priority, self._counter, task.task_id)
        )

    def pop(self):
        """Remove and return the highest-priority pending task, or None."""
        if not self._heap:
            return None
        _, _, task_id = heapq.heappop(self._heap)
        task = self._tasks[task_id]
        task.status = "running"
        return task

    def cancel(self, task_id):
        """Mark a task as cancelled so it will not be executed."""
        if task_id not in self._tasks:
            raise KeyError(task_id)
        self._tasks[task_id].status = "cancelled"

    # ---- queries ----

    def get(self, task_id):
        """Return the task object for *task_id*, or raise KeyError."""
        if task_id not in self._tasks:
            raise KeyError(task_id)
        return self._tasks[task_id]

    def pending_count(self):
        """Return the number of tasks still in pending status."""
        return sum(1 for t in self._tasks.values() if t.status == "pending")
