You are working in a small Python package, `validator/`, in the current directory. Users filed these issues:

1. Email validation rejects valid `+` aliases. Addresses like `user+tag@domain.com` are valid but the regex does not allow the `+` character in the local part.
2. `min_length` and `max_length` checks are off by one. `min_length=3` rejects `"abc"` (length 3) and `max_length=5` rejects `"hello"` (length 5). Both boundary values should be accepted.
3. Nested object validation is skipped entirely. When a field's rules include `"properties"`, the nested object should be validated recursively and errors should be prefixed with the parent field name (e.g. `"address.city"`).
4. The required-field check treats `False` and `0` as missing. Only `None` should count as absent.
5. The type check for `"number"` rejects integers and only accepts `float`. Both `int` and `float` should be accepted (but not `bool`).
6. New feature: add `when(field, value, then_rules)` to `schema.py`. It returns a condition dict. `validate` should accept an optional `conditions` list; for each condition where `data[field] == value`, `then_rules` are applied as an additional schema on the same data.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
