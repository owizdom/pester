You are working in a small Python package, `pipeline/`, in the current directory. Users filed these issues:

1. `FilterStep` passes the wrong value to the predicate function. It passes the index of the item instead of the item itself, so filtering produces wrong results.
2. `MapStep` does not handle `None` return values from the transform function. When the transform returns `None` for an item, that `None` should be skipped (not included in the output).
3. `ReduceStep` without an initial value crashes with an error on empty input. It should return `None` when the input list is empty and no initial value is provided.
4. `BatchStep` drops the last batch if it is smaller than `batch_size`. For example, batching `[1,2,3,4,5]` with size 2 gives `[[1,2],[3,4]]` and drops `[5]`.
5. `Pipeline.run` silently swallows exceptions from individual steps. It catches all exceptions and continues, so errors are never reported to the caller. Exceptions from steps should propagate.
6. New feature: `Pipeline.parallel(steps)` that takes a list of independent steps, runs them concurrently using `concurrent.futures.ThreadPoolExecutor`, collects the results from each step, and returns a list of the individual step results (one result list per step, in the same order as the input steps).

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
