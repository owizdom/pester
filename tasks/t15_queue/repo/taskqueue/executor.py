"""Execute tasks pulled from a PriorityQueue."""

import time
from taskqueue.queue import PriorityQueue
from taskqueue.task import Task


class Executor:
    def __init__(self, queue):
        self.queue = queue
        self.results = {}

    def run_task(self, task, func):
        """Run *func(task)* and handle success, failure, and timeout.

        Returns True on success, False on failure or timeout.
        """
        try:
            if task.timeout is not None:
                start = time.monotonic()
                result = func(task)
                elapsed = time.monotonic() - start
                if elapsed > task.timeout:
                    self.results[task.task_id] = "timeout"
                    return False
            else:
                result = func(task)
            task.status = "done"
            self.results[task.task_id] = result
            return True
        except Exception:
            if task.retries > 0:
                task.status = "pending"
                self.queue._requeue(task)
                return False
            task.status = "failed"
            return False

    def run_next(self, func):
        """Pop the next task and execute it.  Returns None if queue is empty."""
        task = self.queue.pop()
        if task is None:
            return None
        return self.run_task(task, func)
