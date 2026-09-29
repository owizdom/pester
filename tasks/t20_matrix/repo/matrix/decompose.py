"""Matrix decomposition utilities."""

from matrix.matrix import Matrix
from matrix.operations import transpose, multiply


def trace(m):
    """Return the trace (sum of diagonal) of a square matrix."""
    if m.rows != m.cols:
        raise ValueError("trace requires a square matrix")
    return sum(m.get(i, i) for i in range(m.rows))


def is_symmetric(m):
    """Check if a matrix is symmetric."""
    if m.rows != m.cols:
        return False
    for r in range(m.rows):
        for c in range(r + 1, m.cols):
            if abs(m.get(r, c) - m.get(c, r)) > 1e-9:
                return False
    return True


def gram(m):
    """Return M^T * M (the Gram matrix)."""
    mt = transpose(m)
    return multiply(mt, m)


def frobenius_norm(m):
    """Return the Frobenius norm: sqrt of sum of squared elements."""
    total = 0
    for r in range(m.rows):
        for c in range(m.cols):
            total += m.get(r, c) ** 2
    return total ** 0.5
