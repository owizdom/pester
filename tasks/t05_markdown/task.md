You are working in a small Python package, `mdrender/`, in the current directory. Users filed these issues:

1. Headers without a space after `#` are still converted: `##no space` becomes `<h2>no space</h2>`, but the Markdown spec requires a space after the `#` characters. Lines like `##no space` should be left as plain text.
2. Bold markup `**text**` only works when it appears at the start of a line. Inline bold like `Hello **world** today` does not get converted. Bold should work anywhere in the line.
3. Inline code with backticks is not handled at all. Text like `` `code` `` should be rendered as `<code>code</code>`.
4. Unordered lists do not handle nested items. Lines indented with 2 or more spaces followed by `- ` should produce nested `<ul><li>` structures.
5. Links `[text](url)` are rendered without the `href` attribute: the output is `<a>text</a>` instead of `<a href="url">text</a>`.
6. New feature: add strikethrough support. Text wrapped in `~~` like `~~deleted~~` should be rendered as `<del>deleted</del>`. This should work anywhere in a line, just like bold.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
