"""Config section with typed getters."""


_BOOL_TRUE = frozenset({"true", "yes", "1", "on"})
_BOOL_FALSE = frozenset({"false", "no", "0", "off"})


class Section:
    def __init__(self, name, data=None):
        self.name = name
        self._data = dict(data) if data else {}

    def get(self, key, fallback=None):
        return self._data.get(key, fallback)

    def set(self, key, value):
        self._data[key] = value

    def getint(self, key, fallback=0):
        val = self.get(key)
        return int(val) if val is not None else fallback

    def getfloat(self, key, fallback=0.0):
        val = self.get(key)
        return float(val) if val is not None else fallback

    def getboolean(self, key, fallback=False):
        val = self.get(key)
        if val is None:
            return fallback
        low = val.lower()
        if low in _BOOL_TRUE:
            return True
        if low in _BOOL_FALSE:
            return False
        raise ValueError(f"Not a boolean: {val!r}")

    def keys(self):
        return list(self._data.keys())

    def items(self):
        return list(self._data.items())

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return f"Section({self.name!r}, {self._data})"
