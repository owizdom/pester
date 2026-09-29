import unittest

from matrix.matrix import Matrix
from matrix.operations import determinant


class BasicTest(unittest.TestCase):
    def test_create_and_shape(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.shape(), (2, 2))
        self.assertEqual(m.get(0, 1), 2)

    def test_determinant_2x2(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(determinant(m), -2)


if __name__ == "__main__":
    unittest.main()
