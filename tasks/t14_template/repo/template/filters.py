"""Template filters (placeholder -- not yet wired up to renderer)."""


BUILTIN_FILTERS = {}


def register(name):
    """Decorator to register a filter function by name."""
    def wrapper(fn):
        BUILTIN_FILTERS[name] = fn
        return fn
    return wrapper


@register('upper')
def filter_upper(value, arg=None):
    """Convert value to uppercase."""
    return str(value).upper()


@register('lower')
def filter_lower(value, arg=None):
    """Convert value to lowercase."""
    return str(value).lower()


def apply_filter(value, filter_name, arg=None):
    """Apply a named filter to a value. Currently unused by renderer."""
    fn = BUILTIN_FILTERS.get(filter_name)
    if fn is not None:
        return fn(value, arg)
    return value


def parse_filter_expr(expr):
    """Parse a filter expression like 'name | upper' into (varname, filters).
    Not currently called from anywhere."""
    parts = expr.split('|')
    var_name = parts[0].strip()
    filters = []
    for p in parts[1:]:
        p = p.strip()
        if ':' in p:
            fname, farg = p.split(':', 1)
            filters.append((fname.strip(), farg.strip().strip('"').strip("'")))
        else:
            filters.append((p, None))
    return var_name, filters
