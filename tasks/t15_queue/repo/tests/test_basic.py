import unittest

from taskqueue.task import Task
from taskqueue.queue import PriorityQueue


class BasicTest(unittest.TestCase):
    def test_add_and_get(self):
        q = PriorityQueue()
        t = Task("t1", 1, "do stuff")
        q.add(t)
        self.assertEqual(q.get("t1").payload, "do stuff")
        self.assertEqual(q.pending_count(), 1)

    def test_pop_single(self):
        q = PriorityQueue()
        q.add(Task("t1", 1, "work"))
        task = q.pop()
        self.assertEqual(task.task_id, "t1")
        self.assertEqual(task.status, "running")


if __name__ == "__main__":
    unittest.main()
