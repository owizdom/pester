import unittest

from validator.schema import validate


class BasicTest(unittest.TestCase):
    def test_valid_data(self):
        schema = {"name": {"required": True, "type": "string"}}
        errors = validate({"name": "Alice"}, schema)
        self.assertEqual(errors, [])

    def test_missing_required(self):
        schema = {"name": {"required": True}}
        errors = validate({}, schema)
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
