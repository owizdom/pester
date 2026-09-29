"""Parse inventory CSV text: one `sku,qty,price` record per line."""
from inventory.item import Item


def parse_line(line):
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"bad record: {line!r}")
    sku, qty, price = parts
    return Item(sku=sku, qty=int(qty), price=float(price))


def parse(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(parse_line(s))
    return out
