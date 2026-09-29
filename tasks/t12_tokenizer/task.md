You are working in a small Python package, `tokenizer/`, in the current directory. Users filed these issues:

1. String escape sequences are not handled. A string like `"hello \"world\""` gets split into multiple tokens instead of a single STRING token containing `hello "world"`.
2. Multi-character operators (`==`, `!=`, `>=`, `<=`) are parsed as two separate single-character tokens instead of one operator token.
3. Whitespace inside quoted strings is being stripped. The string `"hello world"` loses its internal spaces.
4. Line numbers are wrong after multiline strings. The line counter does not increment when `\n` appears inside a quoted string.
5. No EOF token is emitted at the end of the token stream. The last token should always be `Token("EOF", "", line)`.

New feature: add a function `block_comments(text)` in `scanner.py` that strips `/* ... */` style comments from input text before tokenizing, including handling nested block comments like `/* outer /* inner */ still comment */`.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
