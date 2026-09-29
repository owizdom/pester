You are working in a small Python package, `template/`, in the current directory. Users filed these issues:

1. HTML escaping is not applied to variable output. `{{ name }}` should escape `<`, `>`, `&`, and `"` to their HTML entities (`&lt;`, `&gt;`, `&amp;`, `&quot;`), but currently outputs raw text.
2. `{% for x in items %}` crashes with an IndexError on empty lists instead of producing no output for the loop body.
3. Nested `{% if %}`/`{% else %}`/`{% endif %}` is broken. When an inner if/else appears inside an outer if block, the inner else gets confused with the outer else, producing wrong output.
4. Undefined variables crash with a KeyError instead of rendering as an empty string.
5. Extra blank lines appear around block tags. Lines that contain only a `{% ... %}` tag should not produce a blank line in the output.

New feature: add filter support with pipe syntax. `{{ name | upper }}` applies the `upper` filter, `{{ name | lower }}` applies `lower`, and `{{ count | default:"0" }}` uses the default value when the variable is undefined or empty. Filters are defined in `filters.py`.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
