You are working in a small Python package, `csvtools/`, in the current directory. Users filed these issues:

1. Quoted fields containing commas are split incorrectly. A field like `"Portland, OR"` should stay as one value, but the parser splits on every comma regardless of quoting.
2. Header row whitespace is not stripped. Headers like `" Name , Age "` end up with leading/trailing spaces in the dict keys.
3. Empty rows in the middle of the CSV cause an `IndexError` instead of being skipped.
4. Type inference treats negative numbers as strings. `infer_type("-5")` should return the integer `-5`, and `infer_type("-3.14")` should return the float `-3.14`.
5. `sort_by` does string comparison instead of using the actual values. Sorting a numeric column puts `10` before `2` because `"10" < "2"` lexicographically.
6. New feature: add `pivot(rows, group_col, value_col, agg='sum')` to `transform.py`. It should group rows by `group_col`, aggregate `value_col` using the given function (`sum`, `count`, `mean`, `min`, `max`), and return a sorted list of `{group_col: key, value_col: aggregated}` dicts. Raise `ValueError` for an unknown aggregation.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
