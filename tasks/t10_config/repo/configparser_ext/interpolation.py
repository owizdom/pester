"""Variable interpolation for config values."""
import re


def interpolate(value, section):
    """Replace ${key} references with values from the section."""
    def replacer(match):
        ref_key = match.group(1)
        result = section.get(ref_key)
        if result is None:
            return match.group(0)
        return result

    return re.sub(r"\$\{([^}]+)\}", replacer, value)


def interpolate_section(section):
    """Interpolate all values in a section in place."""
    for key in section.keys():
        val = section.get(key)
        if val and "${" in val:
            section.set(key, interpolate(val, section))
