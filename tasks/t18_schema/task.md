You are working in a small Python package, `jsonschema/`, in the current directory. Users filed these issues:

1. Array items validation only checks the first element. If a schema says `{"type": "array", "items": {"type": "integer"}}`, only the first element is validated; the rest are skipped.
2. Enum comparison is type-strict: the value `1` (int) does not match the enum `[1.0]` (float). Numeric values that are equal should match regardless of int/float type.
3. Pattern matching does not anchor properly. A schema `{"type": "string", "pattern": "^abc$"}` incorrectly matches `"xabcx"` because `re.search` is used instead of `re.fullmatch` or equivalent anchoring.
4. Nested object validation is skipped entirely. When a schema has `"properties"` inside a nested object, those nested properties are never validated.
5. The `required` fields check does not descend into nested objects. If a nested object schema has its own `required` list, those required fields are not checked.
6. New feature: `format_validators` support. Users should be able to register custom format validation functions via `register_format(name, func)` and have them applied when a schema includes `{"format": "name"}`. The function receives the string value and should return `True` if valid, `False` otherwise. A `ValidationError` should be raised if the format check fails. Common formats like `"email"`, `"date"`, and `"uri"` are not built-in; they must be registered by the caller.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
