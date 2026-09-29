"""Pipeline orchestrator."""

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
            try:
                result = step.run(result)
            except Exception:
                # BUG: silently swallows all exceptions
                pass
        return result

    def __len__(self):
        return len(self.steps)

    def __repr__(self):
        names = [s.name for s in self.steps]
        return f"Pipeline({names})"
