from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._d = OrderedDict()

    def get(self, key, default=None):
        if key in self._d:
            return self._d[key]
        return default

    def put(self, key, value):
        self._d[key] = value
        self._d.move_to_end(key)
        if len(self._d) > self.capacity:
            self._d.popitem(last=True)

    def __len__(self):
        return len(self._d)
