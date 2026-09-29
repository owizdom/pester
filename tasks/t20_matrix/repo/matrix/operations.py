"""Matrix operations: multiply, transpose, determinant, inverse."""

from matrix.matrix import Matrix


def transpose(m):
    """Return the transpose of matrix m."""
    # BUG: wrong for non-square matrices (uses m.rows x m.rows instead of m.cols x m.rows)
    result = Matrix.zeros(m.rows, m.cols)
    for r in range(m.rows):
        for c in range(m.cols):
            result.set(r, c, m.get(c, r))
    return result


def multiply(a, b):
    """Return the product of matrices a and b."""
    # BUG: checks rows == rows instead of a.cols == b.rows
    if a.rows != b.rows:
        raise ValueError(
            f"incompatible dimensions: {a.shape()} and {b.shape()}"
        )
    result = Matrix.zeros(a.rows, b.cols)
    for r in range(a.rows):
        for c in range(b.cols):
            s = 0
            for k in range(a.cols):
                s += a.get(r, k) * b.get(k, c)
            result.set(r, c, s)
    return result


def determinant(m):
    """Return the determinant of a square matrix."""
    if m.rows != m.cols:
        raise ValueError("determinant requires a square matrix")
    n = m.rows
    if n == 1:
        return m.get(0, 0)
    if n == 2:
        return m.get(0, 0) * m.get(1, 1) - m.get(0, 1) * m.get(1, 0)
    # BUG: returns 0 for 3x3+
    return 0


def inverse(m):
    """Return the inverse of a 2x2 matrix."""
    if m.rows != 2 or m.cols != 2:
        raise ValueError("inverse only supports 2x2 matrices")
    det = determinant(m)
    # BUG: no check for singular matrix (det == 0)
    inv_det = 1.0 / det
    return Matrix([
        [m.get(1, 1) * inv_det, -m.get(0, 1) * inv_det],
        [-m.get(1, 0) * inv_det, m.get(0, 0) * inv_det],
    ])


def eigenvalues_2x2(m):
    """Compute eigenvalues of a 2x2 matrix. Not yet implemented."""
    raise NotImplementedError("eigenvalues_2x2 is not implemented")
