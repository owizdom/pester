"""Pipeline error types."""


class StepError(Exception):
    """Raised when a pipeline step fails during execution."""

    def __init__(self, step_name, original):
        self.step_name = step_name
        self.original = original
        super().__init__(f"step {step_name!r} failed: {original}")

    def unwrap(self):
        """Return the original exception that caused the step to fail."""
        return self.original


class PipelineError(Exception):
    """Raised when the pipeline itself encounters a structural problem."""

    def __init__(self, message, step_index=None):
        self.message = message
        self.step_index = step_index
        super().__init__(message)


class EmptyPipelineError(PipelineError):
    """Raised when attempting to run a pipeline with no steps."""

    def __init__(self):
        super().__init__("cannot run an empty pipeline", step_index=None)
