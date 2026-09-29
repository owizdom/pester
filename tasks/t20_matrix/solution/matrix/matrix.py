"""Core Matrix class."""


class Matrix:
    """A 2D matrix of floats."""

    def __init__(self, data):
        """Create a matrix from a list of lists."""
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0]) if self.data else 0

    def get(self, r, c):
        return self.data[r][c]

    def set(self, r, c, val):
        self.data[r][c] = val

    def shape(self):
        return (self.rows, self.cols)

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape() != other.shape():
            return False
        for r in range(self.rows):
            for c in range(self.cols):
                if abs(self.data[r][c] - other.data[r][c]) > 1e-9:
                    return False
        return True

    def __repr__(self):
        return f"Matrix({self.data})"

    @classmethod
    def identity(cls, n):
        """Return an n x n identity matrix."""
        data = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return cls(data)

    @classmethod
    def zeros(cls, rows, cols):
        """Return a rows x cols zero matrix."""
        return cls([[0] * cols for _ in range(rows)])
