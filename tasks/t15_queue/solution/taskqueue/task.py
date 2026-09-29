from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """A unit of work with a priority and optional retry/timeout settings."""

    task_id: str
    priority: int
    payload: str
    status: str = "pending"
    retries: int = 3
    timeout: Optional[float] = None

    def __repr__(self):
        return (
            f"Task(id={self.task_id!r}, pri={self.priority}, "
            f"status={self.status!r}, retries={self.retries})"
        )
