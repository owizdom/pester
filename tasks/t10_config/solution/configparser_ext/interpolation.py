"""Variable interpolation for config values."""
import os
import re


def interpolate(value, section, _depth=0):
    """Replace ${key} and ${ENV:VAR} references with resolved values."""
    if _depth > 10:
        return value

    def replacer(match):
        ref_key = match.group(1)
        if ref_key.startswith("ENV:"):
            env_name = ref_key[4:]
            return os.environ.get(env_name, match.group(0))
        result = section.get(ref_key)
        if result is None:
            return match.group(0)
        return result

    resolved = re.sub(r"\$\{([^}]+)\}", replacer, value)
    if resolved != value and "${" in resolved:
        return interpolate(resolved, section, _depth + 1)
    return resolved


def interpolate_section(section):
    """Interpolate all values in a section in place."""
    for key in section.keys():
        val = section.get(key)
        if val and "${" in val:
            section.set(key, interpolate(val, section))
