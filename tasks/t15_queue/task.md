You are working in a small Python package, `taskqueue/`, in the current directory. Users filed these issues:

1. Priority order is wrong. Lower priority numbers should mean higher priority (priority 1 runs before priority 5), but the queue pops tasks with the highest priority number first.
2. Adding a task whose ID already exists silently overwrites the old task. It should raise `ValueError`.
3. Cancelling a task does not actually prevent it from being popped. The cancelled task still comes out of the queue and gets executed.
4. When a task fails and is retried, the retry count never goes down. This causes infinite retries instead of eventually marking the task as failed.
5. When a task times out, its status stays `"running"` instead of being set to `"failed"`.
6. New feature: `PriorityQueue.add_dependency(task_id, depends_on_id)` marks that `task_id` cannot run until `depends_on_id` has completed (status `"done"`). `pop()` should skip tasks whose dependencies are not yet met, putting them back for later. Raise `KeyError` if either ID is unknown.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
