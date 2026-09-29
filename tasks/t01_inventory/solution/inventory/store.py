from inventory.item import Item


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item):
        cur = self._items.get(item.sku)
        if cur is None:
            self._items[item.sku] = Item(item.sku, item.qty, item.price)
        else:
            cur.qty += item.qty
            cur.price = item.price

    def remove(self, sku, qty):
        if sku not in self._items:
            raise KeyError(sku)
        if qty <= 0 or qty > self._items[sku].qty:
            raise ValueError(f"cannot remove {qty} of {sku}")
        self._items[sku].qty -= qty

    def qty(self, sku):
        return self._items[sku].qty if sku in self._items else 0

    def total_value(self):
        return round(sum(i.qty * i.price for i in self._items.values()), 2)

    def skus(self):
        return list(self._items)

    def low_stock(self, threshold):
        return sorted(s for s, i in self._items.items() if i.qty < threshold)
