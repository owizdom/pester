You are working in a small Python package, `contacts/`, in the current directory. Users filed these issues:

1. Adding a contact with name "Alice" and then another with name "alice" creates two entries. Duplicate detection should be case-insensitive.
2. Phone normalization is stripping the country code. `"+1-555-1234"` should normalize to `"15551234"`, not `"5551234"`.
3. Searching by name only returns exact matches. `search_by_name` should support partial/substring matching (case-insensitive).
4. CSV export doesn't handle commas inside field values. A name like `"Doe, Jane"` corrupts the CSV output.
5. CSV import skips the last record in the file. All records should be imported.
6. New feature: `ContactBook.merge_duplicates()` should combine contacts with the same name (case-insensitive), merging their phone numbers and emails. Keep the first occurrence's name casing.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
