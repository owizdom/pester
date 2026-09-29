You are working in a small Python package, `inventory/`, in the current directory. Users filed these issues:

1. Parsing fails on input with blank lines or `# comment` lines, on decimal prices like `2.50`, and on fields with spaces around the commas (`A1 , 3 , 2.50`). A line without exactly three fields should raise `ValueError`.
2. Adding the same SKU twice replaces its stock instead of adding to it. The quantities should add up, and the newest price should win.
3. `Inventory.remove` lets stock go negative. It should raise `KeyError` for an unknown SKU, and `ValueError` for a non-positive quantity or for removing more than is in stock.
4. The report lists SKUs in reverse order. They must be ascending, and the TOTAL line must always show two decimals (`TOTAL: 7.60`). `total_value()` should be rounded to two decimals.
5. New feature: `Inventory.low_stock(threshold)` returns a sorted list of the SKUs whose quantity is below `threshold`.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
