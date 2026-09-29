"""Matrix operations: multiply, transpose, determinant, inverse."""

import cmath

from matrix.matrix import Matrix


def transpose(m):
    """Return the transpose of matrix m."""
    result = Matrix.zeros(m.cols, m.rows)
    for r in range(m.rows):
        for c in range(m.cols):
            result.set(c, r, m.get(r, c))
    return result


def multiply(a, b):
    """Return the product of matrices a and b."""
    if a.cols != b.rows:
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
    det = 0
    for c in range(n):
        sub = _minor(m, 0, c)
        sign = (-1) ** c
        det += sign * m.get(0, c) * determinant(sub)
    return det


def _minor(m, row, col):
    """Return the minor matrix with given row and column removed."""
    data = []
    for r in range(m.rows):
        if r == row:
            continue
        new_row = []
        for c in range(m.cols):
            if c == col:
                continue
            new_row.append(m.get(r, c))
        data.append(new_row)
    return Matrix(data)


def inverse(m):
    """Return the inverse of a 2x2 matrix."""
    if m.rows != 2 or m.cols != 2:
        raise ValueError("inverse only supports 2x2 matrices")
    det = determinant(m)
    if det == 0:
        raise ValueError("matrix is singular, cannot compute inverse")
    inv_det = 1.0 / det
    return Matrix([
        [m.get(1, 1) * inv_det, -m.get(0, 1) * inv_det],
        [-m.get(1, 0) * inv_det, m.get(0, 0) * inv_det],
    ])


def eigenvalues_2x2(m):
    """Compute eigenvalues of a 2x2 matrix using the quadratic formula.

    Returns a tuple of two values (possibly complex).
    """
    if m.rows != 2 or m.cols != 2:
        raise ValueError("eigenvalues_2x2 requires a 2x2 matrix")
    a = m.get(0, 0)
    b = m.get(0, 1)
    c = m.get(1, 0)
    d = m.get(1, 1)
    tr = a + d
    det = a * d - b * c
    disc = tr * tr - 4 * det
    sqrt_disc = cmath.sqrt(disc)
    e1 = (tr + sqrt_disc) / 2
    e2 = (tr - sqrt_disc) / 2
    if disc >= 0:
        return (e1.real, e2.real)
    return (e1, e2)
