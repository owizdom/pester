You are working in a small Python package, `configparser_ext/`, in the current directory. Users filed these issues:

1. Section inheritance (`[child : parent]`) doesn't copy the parent's keys into the child section. Child sections should start with all of the parent's key-value pairs.
2. Variable interpolation `${key}` is not recursive. If `a = ${b}` and `b = hello`, then after interpolation `a` should be `"hello"`, not `"${b}"`.
3. Boolean parsing only handles `"true"` and `"false"`. It should also accept `"yes"`, `"no"`, `"1"`, `"0"`, `"on"`, and `"off"` (case-insensitive).
4. Multiline values (continuation lines starting with whitespace) are silently dropped. They should be appended to the previous key's value, joined by newlines with the leading whitespace stripped.
5. Inline comments (`#` or `;` after a value) are kept as part of the value. They should be stripped, unless the comment character is inside quotes.
6. New feature: `get_env(sections, section_name, key, env_var)` in `parser.py` that returns the key's value if present, otherwise falls back to `os.environ.get(env_var)`. Also support `${ENV:VAR_NAME}` syntax in interpolation to read environment variables.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
