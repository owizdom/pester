"""Built-in pipeline step classes."""


class FilterStep:
    """Keeps items where predicate(item) is truthy."""

    def __init__(self, predicate, name="filter"):
        self.predicate = predicate
        self.name = name

    def run(self, data):
        result = []
        for i, item in enumerate(data):
            # BUG: passes index instead of item
            if self.predicate(i):
                result.append(item)
        return result


class MapStep:
    """Applies transform to each item."""

    def __init__(self, transform, name="map"):
        self.transform = transform
        self.name = name

    def run(self, data):
        # BUG: doesn't filter out None returns
        return [self.transform(item) for item in data]


class ReduceStep:
    """Reduces data to a single value using a binary function."""

    def __init__(self, func, initial=None, name="reduce"):
        self.func = func
        self.initial = initial
        self.name = name

    def run(self, data):
        # BUG: crashes on empty input when no initial value
        if self.initial is not None:
            result = self.initial
            for item in data:
                result = self.func(result, item)
            return result
        result = data[0]
        for item in data[1:]:
            result = self.func(result, item)
        return result


class BatchStep:
    """Groups items into fixed-size batches."""

    def __init__(self, batch_size, name="batch"):
        self.batch_size = batch_size
        self.name = name

    def run(self, data):
        batches = []
        # BUG: drops the last incomplete batch
        for i in range(0, len(data) - self.batch_size + 1, self.batch_size):
            batches.append(data[i:i + self.batch_size])
        return batches
