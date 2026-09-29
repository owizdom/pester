"""Schema-based data validation."""
from validator.rules import (
    check_required, check_type, check_email,
    check_min_length, check_max_length,
    check_min_value, check_max_value,
)
from validator.errors import ValidationError


def validate(data, schema, conditions=None):
    """Validate data against a schema.

    Returns a list of error dicts with 'field' and 'message' keys.
    """
    errors = []

    for field, rules in schema.items():
        value = data.get(field)

        if rules.get("required") and not check_required(value):
            errors.append({"field": field, "message": "is required"})
            continue

        if value is None:
            continue

        if "type" in rules:
            if not check_type(value, rules["type"]):
                errors.append({"field": field,
                               "message": f"must be {rules['type']}"})
                continue

        if isinstance(value, str):
            if "min_length" in rules:
                if not check_min_length(value, rules["min_length"]):
                    errors.append({"field": field,
                                   "message": f"too short"})
            if "max_length" in rules:
                if not check_max_length(value, rules["max_length"]):
                    errors.append({"field": field,
                                   "message": f"too long"})
            if rules.get("email") and not check_email(value):
                errors.append({"field": field,
                               "message": "invalid email"})

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "min_value" in rules:
                if not check_min_value(value, rules["min_value"]):
                    errors.append({"field": field,
                                   "message": f"too small"})
            if "max_value" in rules:
                if not check_max_value(value, rules["max_value"]):
                    errors.append({"field": field,
                                   "message": f"too large"})

    return errors


def validate_or_raise(data, schema, conditions=None):
    """Validate and raise ValidationError if any errors are found."""
    errors = validate(data, schema, conditions=conditions)
    if errors:
        raise ValidationError(errors)
