You are working in a small Python package, `textdiff/`, in the current directory. Users filed these issues:

1. `lcs_length` returns 1 instead of 0 when either input is empty.
2. When two changes are close together, the unified diff emits separate hunks whose context lines overlap. Close changes should be merged into a single hunk.
3. The unified diff output is missing the file-header lines (`--- old_name` and `+++ new_name`).
4. Line numbers in the `@@ -a,b +c,d @@` hunk headers are 0-indexed. They should be 1-indexed.
5. The `+` and `-` prefixes on changed lines are swapped: removed lines show `+` and added lines show `-`.
6. New feature: `word_diff(line_a, line_b)` returns a list of `(type, word)` tuples showing word-level changes between two lines, where `type` is `"equal"`, `"add"`, or `"remove"`. Words are defined by `str.split()`.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
