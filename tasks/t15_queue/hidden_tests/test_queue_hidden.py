import unittest
import time

from taskqueue.task import Task
from taskqueue.queue import PriorityQueue
from taskqueue.executor import Executor


class PriorityOrderHidden(unittest.TestCase):
    def test_lower_number_pops_first(self):
        q = PriorityQueue()
        q.add(Task("low", 5, "low priority"))
        q.add(Task("high", 1, "high priority"))
        q.add(Task("mid", 3, "medium priority"))
        first = q.pop()
        self.assertEqual(first.task_id, "high")
        second = q.pop()
        self.assertEqual(second.task_id, "mid")
        third = q.pop()
        self.assertEqual(third.task_id, "low")


class DuplicateHidden(unittest.TestCase):
    def test_duplicate_id_raises(self):
        q = PriorityQueue()
        q.add(Task("t1", 1, "first"))
        with self.assertRaises(ValueError):
            q.add(Task("t1", 2, "second"))


class CancelHidden(unittest.TestCase):
    def test_cancelled_task_not_popped(self):
        q = PriorityQueue()
        q.add(Task("t1", 1, "work"))
        q.cancel("t1")
        task = q.pop()
        self.assertIsNone(task)

    def test_cancel_returns_next(self):
        q = PriorityQueue()
        q.add(Task("t1", 1, "first"))
        q.add(Task("t2", 1, "second"))
        q.cancel("t1")
        task = q.pop()
        self.assertEqual(task.task_id, "t2")

    def test_cancel_unknown_raises(self):
        q = PriorityQueue()
        with self.assertRaises(KeyError):
            q.cancel("nonexistent")


class RetryHidden(unittest.TestCase):
    def test_retry_decrements(self):
        q = PriorityQueue()
        t = Task("t1", 1, "work", retries=2)
        q.add(t)
        ex = Executor(q)
        task = q.pop()
        ex.run_task(task, lambda t: 1 / 0)
        self.assertEqual(task.retries, 1)

    def test_retries_exhausted_marks_failed(self):
        q = PriorityQueue()
        t = Task("t1", 1, "work", retries=1)
        q.add(t)
        ex = Executor(q)
        task = q.pop()
        ex.run_task(task, lambda t: 1 / 0)
        self.assertEqual(task.status, "failed")

    def test_retry_requeues(self):
        q = PriorityQueue()
        t = Task("t1", 1, "work", retries=3)
        q.add(t)
        ex = Executor(q)
        task = q.pop()
        ex.run_task(task, lambda t: 1 / 0)
        self.assertEqual(task.status, "pending")
        again = q.pop()
        self.assertIs(again, task)


class TimeoutHidden(unittest.TestCase):
    def test_timeout_marks_failed(self):
        q = PriorityQueue()
        t = Task("t1", 1, "work", timeout=0.01)
        q.add(t)
        ex = Executor(q)
        task = q.pop()

        def slow(t):
            time.sleep(0.05)
            return "late"

        ex.run_task(task, slow)
        self.assertEqual(task.status, "failed")
        self.assertEqual(ex.results["t1"], "timeout")


class DependencyHidden(unittest.TestCase):
    def test_dependency_blocks_pop(self):
        q = PriorityQueue()
        q.add(Task("a", 2, "first"))
        q.add(Task("b", 1, "second"))
        q.add_dependency("b", "a")
        first = q.pop()
        self.assertEqual(first.task_id, "a")

    def test_dependency_unblocks_after_done(self):
        q = PriorityQueue()
        q.add(Task("a", 2, "first"))
        q.add(Task("b", 1, "second"))
        q.add_dependency("b", "a")
        a = q.pop()
        a.status = "done"
        b = q.pop()
        self.assertIsNotNone(b)
        self.assertEqual(b.task_id, "b")

    def test_dependency_unknown_raises(self):
        q = PriorityQueue()
        q.add(Task("a", 1, "work"))
        with self.assertRaises(KeyError):
            q.add_dependency("a", "ghost")
        with self.assertRaises(KeyError):
            q.add_dependency("ghost", "a")


class RunNextHidden(unittest.TestCase):
    def test_run_next_success(self):
        q = PriorityQueue()
        q.add(Task("t1", 1, "work"))
        ex = Executor(q)
        ok = ex.run_next(lambda t: "done")
        self.assertTrue(ok)
        self.assertEqual(q.get("t1").status, "done")

    def test_run_next_empty(self):
        q = PriorityQueue()
        ex = Executor(q)
        self.assertIsNone(ex.run_next(lambda t: "x"))


if __name__ == "__main__":
    unittest.main()
