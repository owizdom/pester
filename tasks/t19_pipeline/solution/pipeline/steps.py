"""Built-in pipeline step classes."""


class FilterStep:
    """Keeps items where predicate(item) is truthy."""

    def __init__(self, predicate, name="filter"):
        self.predicate = predicate
        self.name = name

    def run(self, data):
        result = []
        for item in data:
            if self.predicate(item):
                result.append(item)
        return result


class MapStep:
    """Applies transform to each item. Skips None results."""

    def __init__(self, transform, name="map"):
        self.transform = transform
        self.name = name

    def run(self, data):
        result = []
        for item in data:
            mapped = self.transform(item)
            if mapped is not None:
                result.append(mapped)
        return result


class ReduceStep:
    """Reduces data to a single value using a binary function."""

    def __init__(self, func, initial=None, name="reduce"):
        self.func = func
        self.initial = initial
        self.name = name

    def run(self, data):
        if self.initial is not None:
            result = self.initial
            for item in data:
                result = self.func(result, item)
            return result
        if not data:
            return None
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
        for i in range(0, len(data), self.batch_size):
            batches.append(data[i:i + self.batch_size])
        return batches
