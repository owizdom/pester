"""Parse inventory CSV text: one `sku,qty,price` record per line."""
from inventory.item import Item


def parse_line(line):
    sku, qty, price = line.split(",")
    return Item(sku=sku, qty=int(qty), price=int(price))


def parse(text):
    return [parse_line(line) for line in text.splitlines()]
