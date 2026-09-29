You are working in a small Python package, `textstats/`, in the current directory. Users filed these issues:

1. `words()` splits contractions: "don't" becomes "don" and "t". Words must be lowercase, and an apostrophe between letters stays inside the word ("Don't" gives "don't").
2. `sentences()` only splits on periods and returns empty strings. It should split on `.`, `!` and `?` (runs like `?!` count once), strip whitespace, and drop empty pieces.
3. `word_freq` counts "The" and "the" separately. It should be case-insensitive.
4. `top_n` breaks ties arbitrarily. Ties must be broken alphabetically.
5. `average_word_length("")` crashes. It should return `0.0` for text without words.
6. `LRUCache` evicts the wrong entry, and `get` does not count as a use. It must evict the least recently used key, a `get` hit must mark the key as recently used, and a capacity below 1 must raise `ValueError`.
7. New feature: `stats.average_sentence_length(text)` returns the mean number of words per sentence, or `0.0` when there are no sentences.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
