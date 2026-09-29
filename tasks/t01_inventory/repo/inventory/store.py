from inventory.item import Item


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item):
        self._items[item.sku] = item

    def remove(self, sku, qty):
        self._items[sku].qty -= qty

    def qty(self, sku):
        return self._items[sku].qty if sku in self._items else 0

    def total_value(self):
        return sum(i.qty * i.price for i in self._items.values())

    def skus(self):
        return list(self._items)
