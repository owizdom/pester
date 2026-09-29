import unittest
import cmath

from matrix.matrix import Matrix
from matrix.operations import transpose, multiply, determinant, inverse, eigenvalues_2x2
from matrix.decompose import trace, gram


class TransposeHidden(unittest.TestCase):
    def test_nonsquare_transpose(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        t = transpose(m)
        self.assertEqual(t.shape(), (3, 2))
        self.assertEqual(t.get(0, 0), 1)
        self.assertEqual(t.get(0, 1), 4)
        self.assertEqual(t.get(2, 0), 3)
        self.assertEqual(t.get(2, 1), 6)

    def test_square_transpose(self):
        m = Matrix([[1, 2], [3, 4]])
        t = transpose(m)
        self.assertEqual(t.get(0, 1), 3)
        self.assertEqual(t.get(1, 0), 2)


class MultiplyHidden(unittest.TestCase):
    def test_valid_multiply(self):
        a = Matrix([[1, 2, 3], [4, 5, 6]])
        b = Matrix([[7, 8], [9, 10], [11, 12]])
        result = multiply(a, b)
        self.assertEqual(result.shape(), (2, 2))
        self.assertEqual(result.get(0, 0), 58)
        self.assertEqual(result.get(1, 1), 154)

    def test_incompatible_raises(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with self.assertRaises(ValueError):
            multiply(a, b)


class DeterminantHidden(unittest.TestCase):
    def test_3x3_determinant(self):
        m = Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
        self.assertEqual(determinant(m), 1)

    def test_3x3_identity(self):
        m = Matrix.identity(3)
        self.assertEqual(determinant(m), 1)

    def test_singular_3x3(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(determinant(m), 0)


class InverseHidden(unittest.TestCase):
    def test_singular_raises(self):
        m = Matrix([[1, 2], [2, 4]])
        with self.assertRaises(ValueError):
            inverse(m)

    def test_inverse_correct(self):
        m = Matrix([[4, 7], [2, 6]])
        inv = inverse(m)
        product = multiply(m, inv)
        identity = Matrix.identity(2)
        self.assertEqual(product, identity)


class EqualityHidden(unittest.TestCase):
    def test_float_tolerance(self):
        a = Matrix([[0.1 + 0.2, 0], [0, 1]])
        b = Matrix([[0.3, 0], [0, 1]])
        self.assertEqual(a, b)

    def test_different_values_not_equal(self):
        a = Matrix([[1, 0], [0, 1]])
        b = Matrix([[1, 0], [0, 2]])
        self.assertNotEqual(a, b)


class EigenvaluesHidden(unittest.TestCase):
    def test_real_eigenvalues(self):
        m = Matrix([[2, 1], [1, 2]])
        e1, e2 = eigenvalues_2x2(m)
        vals = sorted([e1, e2])
        self.assertAlmostEqual(vals[0], 1.0)
        self.assertAlmostEqual(vals[1], 3.0)

    def test_complex_eigenvalues(self):
        m = Matrix([[0, -1], [1, 0]])
        e1, e2 = eigenvalues_2x2(m)
        self.assertAlmostEqual(abs(e1.imag), 1.0)
        self.assertAlmostEqual(abs(e2.imag), 1.0)
        self.assertAlmostEqual(e1.real, 0.0)

    def test_diagonal_eigenvalues(self):
        m = Matrix([[5, 0], [0, 3]])
        e1, e2 = eigenvalues_2x2(m)
        vals = sorted([e1, e2])
        self.assertAlmostEqual(vals[0], 3.0)
        self.assertAlmostEqual(vals[1], 5.0)


class GramHidden(unittest.TestCase):
    def test_gram_nonsquare(self):
        m = Matrix([[1, 2], [3, 4], [5, 6]])
        g = gram(m)
        self.assertEqual(g.shape(), (2, 2))
        self.assertEqual(g.get(0, 0), 35)


if __name__ == "__main__":
    unittest.main()
