from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._d = OrderedDict()

    def get(self, key, default=None):
        if key in self._d:
            self._d.move_to_end(key)
            return self._d[key]
        return default

    def put(self, key, value):
        self._d[key] = value
        self._d.move_to_end(key)
        if len(self._d) > self.capacity:
            self._d.popitem(last=False)

    def __len__(self):
        return len(self._d)
