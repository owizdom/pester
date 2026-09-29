"""Pipeline orchestrator."""

from concurrent.futures import ThreadPoolExecutor

from pipeline.errors import StepError


class Pipeline:
    """Runs a sequence of steps on data."""

    def __init__(self, steps=None):
        self.steps = list(steps or [])

    def add(self, step):
        """Append a step to the pipeline."""
        self.steps.append(step)
        return self

    def run(self, data):
        """Execute all steps in order. Returns the final result."""
        result = data
        for step in self.steps:
            result = step.run(result)
        return result

    def parallel(self, steps, data):
        """Run independent steps concurrently on the same data.

        Returns a list of results, one per step, in the same order.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(step.run, list(data)) for step in steps]
            return [f.result() for f in futures]

    def __len__(self):
        return len(self.steps)

    def __repr__(self):
        names = [s.name for s in self.steps]
        return f"Pipeline({names})"
