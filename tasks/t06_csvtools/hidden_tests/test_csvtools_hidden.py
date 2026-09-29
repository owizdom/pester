import unittest

from csvtools.reader import read_csv, parse_row
from csvtools.writer import write_csv
from csvtools.transform import infer_type, typed_rows, sort_by


class TestParseRow(unittest.TestCase):
    def test_quoted_field_with_comma(self):
        fields = parse_row('Alice,"New York, NY",30')
        self.assertEqual(fields, ["Alice", "New York, NY", "30"])

    def test_simple_row(self):
        fields = parse_row("a,b,c")
        self.assertEqual(fields, ["a", "b", "c"])


class TestReadCsv(unittest.TestCase):
    def test_header_whitespace_stripped(self):
        rows = read_csv(" Name , Age \nAlice,30\n")
        self.assertIn("Name", rows[0])
        self.assertIn("Age", rows[0])

    def test_empty_rows_skipped(self):
        rows = read_csv("Name,Age\nAlice,30\n\nBob,25\n")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["Name"], "Bob")

    def test_quoted_commas_preserved(self):
        data = 'City,State\n"San Jose",CA\n"Portland, OR",OR\n'
        rows = read_csv(data)
        self.assertEqual(rows[1]["City"], "Portland, OR")


class TestInferType(unittest.TestCase):
    def test_negative_integer(self):
        self.assertEqual(infer_type("-5"), -5)
        self.assertIsInstance(infer_type("-5"), int)

    def test_negative_float(self):
        self.assertAlmostEqual(infer_type("-3.14"), -3.14)
        self.assertIsInstance(infer_type("-3.14"), float)

    def test_positive_int_and_float(self):
        self.assertEqual(infer_type("42"), 42)
        self.assertAlmostEqual(infer_type("3.14"), 3.14)


class TestSortBy(unittest.TestCase):
    def test_numeric_sort(self):
        rows = [{"n": "A", "v": 10}, {"n": "B", "v": 2}, {"n": "C", "v": 20}]
        result = sort_by(rows, "v")
        self.assertEqual([r["v"] for r in result], [2, 10, 20])


class TestPivot(unittest.TestCase):
    def test_sum(self):
        from csvtools.transform import pivot
        rows = [
            {"dept": "eng", "salary": 100},
            {"dept": "eng", "salary": 200},
            {"dept": "sales", "salary": 150},
        ]
        result = pivot(rows, "dept", "salary", agg="sum")
        by_dept = {r["dept"]: r["salary"] for r in result}
        self.assertEqual(by_dept["eng"], 300)
        self.assertEqual(by_dept["sales"], 150)

    def test_count(self):
        from csvtools.transform import pivot
        rows = [
            {"dept": "eng", "salary": 100},
            {"dept": "eng", "salary": 200},
            {"dept": "sales", "salary": 150},
        ]
        result = pivot(rows, "dept", "salary", agg="count")
        by_dept = {r["dept"]: r["salary"] for r in result}
        self.assertEqual(by_dept["eng"], 2)
        self.assertEqual(by_dept["sales"], 1)

    def test_mean(self):
        from csvtools.transform import pivot
        rows = [
            {"dept": "eng", "salary": 100},
            {"dept": "eng", "salary": 200},
        ]
        result = pivot(rows, "dept", "salary", agg="mean")
        self.assertAlmostEqual(result[0]["salary"], 150.0)

    def test_unknown_agg_raises(self):
        from csvtools.transform import pivot
        with self.assertRaises(ValueError):
            pivot([{"a": 1, "b": 2}], "a", "b", agg="median")


if __name__ == "__main__":
    unittest.main()
