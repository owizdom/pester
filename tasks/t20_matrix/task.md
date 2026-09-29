You are working in a small Python package, `matrix/`, in the current directory. Users filed these issues:

1. Transpose is wrong for non-square matrices. A 2x3 matrix transposed should be 3x2, but the current implementation swaps indices incorrectly and crashes or produces wrong dimensions.
2. Matrix multiply has a backwards dimension check. It checks `rows == rows` instead of `cols of A == rows of B`, so valid multiplications are rejected and invalid ones are allowed.
3. Determinant only works for 2x2 matrices. For 3x3 and larger matrices it returns 0 instead of computing the correct value via cofactor expansion.
4. Inverse does not check for singular matrices. When the determinant is zero, it attempts division by zero instead of raising a `ValueError`.
5. Matrix equality check uses `==` on floats, which fails for values that differ by floating-point rounding. It should use approximate comparison with a small tolerance.
6. New feature: `eigenvalues_2x2(matrix)` that computes the eigenvalues of a 2x2 matrix using the quadratic formula on the characteristic polynomial. Returns a tuple of two values. If the discriminant is negative, the values should be complex numbers.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
