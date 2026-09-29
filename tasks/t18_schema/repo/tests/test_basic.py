import unittest

from jsonschema.validator import validate
from jsonschema.errors import ValidationError


class BasicTest(unittest.TestCase):
    def test_type_check_string(self):
        validate("hello", {"type": "string"})
        with self.assertRaises(ValidationError):
            validate(123, {"type": "string"})

    def test_simple_object_required(self):
        schema = {"type": "object", "required": ["name"]}
        validate({"name": "Alice"}, schema)
        with self.assertRaises(ValidationError):
            validate({}, schema)


if __name__ == "__main__":
    unittest.main()
