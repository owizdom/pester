import unittest

from pipeline.steps import FilterStep, MapStep, ReduceStep, BatchStep
from pipeline.pipeline import Pipeline


class FilterStepHidden(unittest.TestCase):
    def test_filter_uses_item_not_index(self):
        step = FilterStep(lambda x: x > 3)
        result = step.run([1, 5, 2, 8, 3])
        self.assertEqual(result, [5, 8])

    def test_filter_strings(self):
        step = FilterStep(lambda s: len(s) > 3)
        result = step.run(["hi", "hello", "ok", "world"])
        self.assertEqual(result, ["hello", "world"])


class MapStepHidden(unittest.TestCase):
    def test_map_skips_none(self):
        step = MapStep(lambda x: x * 2 if x > 0 else None)
        result = step.run([1, -1, 3, 0, 5])
        self.assertEqual(result, [2, 6, 10])

    def test_map_all_none(self):
        step = MapStep(lambda x: None)
        result = step.run([1, 2, 3])
        self.assertEqual(result, [])


class ReduceStepHidden(unittest.TestCase):
    def test_reduce_empty_no_initial(self):
        step = ReduceStep(lambda a, b: a + b)
        result = step.run([])
        self.assertIsNone(result)

    def test_reduce_with_initial(self):
        step = ReduceStep(lambda a, b: a + b, initial=10)
        result = step.run([1, 2, 3])
        self.assertEqual(result, 16)

    def test_reduce_single_element(self):
        step = ReduceStep(lambda a, b: a + b)
        result = step.run([42])
        self.assertEqual(result, 42)


class BatchStepHidden(unittest.TestCase):
    def test_last_incomplete_batch_included(self):
        step = BatchStep(2)
        result = step.run([1, 2, 3, 4, 5])
        self.assertEqual(result, [[1, 2], [3, 4], [5]])

    def test_single_item_batch(self):
        step = BatchStep(3)
        result = step.run([1])
        self.assertEqual(result, [[1]])

    def test_exact_batch(self):
        step = BatchStep(2)
        result = step.run([1, 2, 3, 4])
        self.assertEqual(result, [[1, 2], [3, 4]])


class PipelineRunHidden(unittest.TestCase):
    def test_exception_propagates(self):
        def bad_transform(x):
            raise ValueError("oops")
        p = Pipeline([MapStep(bad_transform)])
        with self.assertRaises(ValueError):
            p.run([1, 2])

    def test_chained_steps(self):
        p = Pipeline([
            FilterStep(lambda x: x > 0),
            MapStep(lambda x: x * 10),
        ])
        result = p.run([-1, 2, -3, 4])
        self.assertEqual(result, [20, 40])


class PipelineParallelHidden(unittest.TestCase):
    def test_parallel_runs_steps(self):
        p = Pipeline()
        s1 = MapStep(lambda x: x * 2)
        s2 = FilterStep(lambda x: x > 2)
        results = p.parallel([s1, s2], [1, 2, 3])
        self.assertEqual(results[0], [2, 4, 6])
        self.assertEqual(results[1], [3])

    def test_parallel_preserves_order(self):
        import time
        p = Pipeline()
        slow = MapStep(lambda x: (time.sleep(0.01), x)[1], name="slow")
        fast = MapStep(lambda x: x + 1, name="fast")
        results = p.parallel([slow, fast], [1, 2])
        self.assertEqual(results[0], [1, 2])
        self.assertEqual(results[1], [2, 3])


if __name__ == "__main__":
    unittest.main()
