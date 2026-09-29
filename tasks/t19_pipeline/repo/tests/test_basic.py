import unittest

from pipeline.steps import MapStep
from pipeline.pipeline import Pipeline


class BasicTest(unittest.TestCase):
    def test_map_doubles(self):
        step = MapStep(lambda x: x * 2)
        result = step.run([1, 2, 3])
        self.assertEqual(result, [2, 4, 6])

    def test_pipeline_single_step(self):
        p = Pipeline([MapStep(lambda x: x + 1)])
        result = p.run([10, 20])
        self.assertEqual(result, [11, 21])


if __name__ == "__main__":
    unittest.main()
