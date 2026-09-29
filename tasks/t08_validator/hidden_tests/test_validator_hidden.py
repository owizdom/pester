import unittest

from validator.rules import (
    check_email, check_min_length, check_max_length,
    check_type, check_required,
)
from validator.schema import validate, validate_or_raise
from validator.errors import ValidationError


class TestEmail(unittest.TestCase):
    def test_plus_alias_accepted(self):
        self.assertTrue(check_email("user+tag@domain.com"))

    def test_normal_email_accepted(self):
        self.assertTrue(check_email("alice@example.org"))

    def test_invalid_rejected(self):
        self.assertFalse(check_email("not-an-email"))


class TestLength(unittest.TestCase):
    def test_min_length_boundary(self):
        self.assertTrue(check_min_length("abc", 3))

    def test_max_length_boundary(self):
        self.assertTrue(check_max_length("hello", 5))

    def test_below_min(self):
        self.assertFalse(check_min_length("ab", 3))

    def test_above_max(self):
        self.assertFalse(check_max_length("toolong", 5))


class TestRequired(unittest.TestCase):
    def test_false_is_present(self):
        self.assertTrue(check_required(False))

    def test_zero_is_present(self):
        self.assertTrue(check_required(0))

    def test_none_is_missing(self):
        self.assertFalse(check_required(None))


class TestTypeCheck(unittest.TestCase):
    def test_number_accepts_int(self):
        self.assertTrue(check_type(5, "number"))

    def test_number_accepts_float(self):
        self.assertTrue(check_type(3.14, "number"))

    def test_number_rejects_bool(self):
        self.assertFalse(check_type(True, "number"))


class TestNestedValidation(unittest.TestCase):
    def test_nested_required(self):
        schema = {
            "address": {
                "properties": {
                    "city": {"required": True, "type": "string"},
                }
            }
        }
        errors = validate({"address": {}}, schema)
        fields = [e["field"] for e in errors]
        self.assertIn("address.city", fields)

    def test_nested_passes(self):
        schema = {
            "address": {
                "properties": {
                    "city": {"required": True, "type": "string"},
                }
            }
        }
        errors = validate({"address": {"city": "Portland"}}, schema)
        self.assertEqual(errors, [])


class TestWhen(unittest.TestCase):
    def test_condition_met(self):
        from validator.schema import when
        schema = {"role": {"required": True, "type": "string"}}
        conds = [when("role", "admin",
                       {"admin_code": {"required": True, "type": "string"}})]
        errors = validate({"role": "admin"}, schema, conditions=conds)
        fields = [e["field"] for e in errors]
        self.assertIn("admin_code", fields)

    def test_condition_not_met(self):
        from validator.schema import when
        schema = {"role": {"required": True, "type": "string"}}
        conds = [when("role", "admin",
                       {"admin_code": {"required": True}})]
        errors = validate({"role": "viewer"}, schema, conditions=conds)
        self.assertEqual(errors, [])


class TestValidateOrRaise(unittest.TestCase):
    def test_raises_on_errors(self):
        schema = {"name": {"required": True}}
        with self.assertRaises(ValidationError):
            validate_or_raise({}, schema)


if __name__ == "__main__":
    unittest.main()
