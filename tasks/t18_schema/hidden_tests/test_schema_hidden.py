import unittest

from jsonschema.validator import validate, register_format
from jsonschema.errors import ValidationError
from jsonschema.types import types_equal


class ArrayItemsHidden(unittest.TestCase):
    def test_all_elements_validated(self):
        schema = {"type": "array", "items": {"type": "integer"}}
        validate([1, 2, 3], schema)
        with self.assertRaises(ValidationError):
            validate([1, "bad", 3], schema)

    def test_second_element_invalid(self):
        schema = {"type": "array", "items": {"type": "string"}}
        with self.assertRaises(ValidationError):
            validate(["ok", 99], schema)

    def test_last_element_invalid(self):
        schema = {"type": "array", "items": {"type": "integer"}}
        with self.assertRaises(ValidationError):
            validate([1, 2, 3, "oops"], schema)


class EnumHidden(unittest.TestCase):
    def test_int_matches_float_enum(self):
        schema = {"enum": [1.0, 2.0, 3.0]}
        validate(1, schema)

    def test_float_matches_int_enum(self):
        schema = {"enum": [1, 2, 3]}
        validate(2.0, schema)

    def test_enum_still_rejects_wrong_value(self):
        schema = {"enum": [1, 2, 3]}
        with self.assertRaises(ValidationError):
            validate(4, schema)

    def test_types_equal_numeric(self):
        self.assertTrue(types_equal(1, 1.0))
        self.assertTrue(types_equal(0, 0.0))
        self.assertFalse(types_equal(True, 1))


class PatternHidden(unittest.TestCase):
    def test_anchored_pattern_rejects_substring(self):
        schema = {"type": "string", "pattern": "^abc$"}
        validate("abc", schema)
        with self.assertRaises(ValidationError):
            validate("xabcx", schema)

    def test_partial_pattern_match(self):
        schema = {"type": "string", "pattern": "^[0-9]+$"}
        validate("123", schema)
        with self.assertRaises(ValidationError):
            validate("12x3", schema)


class NestedObjectHidden(unittest.TestCase):
    def test_nested_properties_validated(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
        }
        validate({"name": "Alice", "age": 30}, schema)
        with self.assertRaises(ValidationError):
            validate({"name": "Alice", "age": "thirty"}, schema)

    def test_deeply_nested_properties(self):
        schema = {
            "type": "object",
            "properties": {
                "address": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "zip": {"type": "string"},
                    },
                }
            },
        }
        validate({"address": {"city": "NY", "zip": "10001"}}, schema)
        with self.assertRaises(ValidationError):
            validate({"address": {"city": "NY", "zip": 10001}}, schema)

    def test_nested_required(self):
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "required": ["email"],
                    "properties": {
                        "email": {"type": "string"},
                    },
                }
            },
        }
        validate({"user": {"email": "a@b.c"}}, schema)
        with self.assertRaises(ValidationError):
            validate({"user": {}}, schema)


class FormatValidatorsHidden(unittest.TestCase):
    def test_register_and_use_format(self):
        register_format("test_email", lambda s: "@" in s)
        schema = {"type": "string", "format": "test_email"}
        validate("user@example.com", schema)
        with self.assertRaises(ValidationError):
            validate("not-an-email", schema)

    def test_unknown_format_passes(self):
        schema = {"type": "string", "format": "unknown_format_xyz"}
        validate("anything", schema)

    def test_custom_date_format(self):
        import re
        register_format("test_date", lambda s: bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", s)))
        schema = {"type": "string", "format": "test_date"}
        validate("2024-01-15", schema)
        with self.assertRaises(ValidationError):
            validate("not-a-date", schema)


if __name__ == "__main__":
    unittest.main()
