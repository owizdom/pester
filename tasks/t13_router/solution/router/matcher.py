"""Path matching utilities."""


def normalize_path(path):
    """Normalize a URL path by stripping trailing slashes."""
    if not path.startswith('/'):
        path = '/' + path
    if path != '/' and path.endswith('/'):
        path = path.rstrip('/')
    return path


def split_path(path):
    """Split a path into its segments."""
    path = normalize_path(path)
    parts = path.strip('/').split('/')
    return [p for p in parts if p]


def paths_equal(a, b):
    """Check if two paths are equivalent, ignoring trailing slashes."""
    return normalize_path(a) == normalize_path(b)


def extract_params(pattern_parts, path_parts):
    """Extract named parameters from path parts matching a pattern.
    Accepts any non-empty value for parameter segments."""
    params = {}
    for pp, pathp in zip(pattern_parts, path_parts):
        if pp.startswith(':'):
            if not pathp:
                return None
            params[pp[1:]] = pathp
    return params
