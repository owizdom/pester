"""Core JSON schema validator."""
import re

from jsonschema.errors import ValidationError
from jsonschema.types import check_type, types_equal

_format_validators = {}


def register_format(name, func):
    """Register a custom format validation function."""
    _format_validators[name] = func


def validate(instance, schema, path=None):
    """Validate instance against schema. Raises ValidationError on failure."""
    if path is None:
        path = []

    if "type" in schema:
        if not check_type(instance, schema["type"]):
            raise ValidationError(
                f"expected {schema['type']}, got {type(instance).__name__}", path=path)

    if "enum" in schema:
        if not any(types_equal(instance, v) for v in schema["enum"]):
            raise ValidationError(f"{instance!r} not in enum", path=path)

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            raise ValidationError("string too short", path=path)
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            raise ValidationError("string too long", path=path)
        if "pattern" in schema:
            # BUG: uses re.search instead of re.fullmatch
            if not re.search(schema["pattern"], instance):
                raise ValidationError(f"no match for {schema['pattern']!r}", path=path)

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise ValidationError(f"below minimum {schema['minimum']}", path=path)
        if "maximum" in schema and instance > schema["maximum"]:
            raise ValidationError(f"above maximum {schema['maximum']}", path=path)

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            raise ValidationError("array too short", path=path)
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise ValidationError("array too long", path=path)
        if "items" in schema:
            # BUG: only validates first element
            for i, item in enumerate(instance):
                validate(item, schema["items"], path=path + [i])
                break

    if isinstance(instance, dict):
        if "required" in schema:
            for field in schema["required"]:
                if field not in instance:
                    raise ValidationError(f"missing required field {field!r}", path=path)
        # BUG: nested properties validation is skipped
        if "properties" in schema and False:
            for prop, prop_schema in schema["properties"].items():
                if prop in instance:
                    validate(instance[prop], prop_schema, path=path + [prop])

    return True
