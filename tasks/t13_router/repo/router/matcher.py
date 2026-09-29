"""Path matching utilities."""


def normalize_path(path):
    """Normalize a URL path. Currently a no-op placeholder.
    BUG: does not strip trailing slashes."""
    if not path.startswith('/'):
        path = '/' + path
    return path


def split_path(path):
    """Split a path into its segments."""
    path = normalize_path(path)
    parts = path.strip('/').split('/')
    return [p for p in parts if p]


def paths_equal(a, b):
    """Check if two paths are equivalent.
    BUG: does not handle trailing slash equivalence."""
    return a == b


def extract_params(pattern_parts, path_parts):
    """Extract named parameters from path parts matching a pattern.
    BUG: rejects values with dots or hyphens."""
    params = {}
    for pp, pathp in zip(pattern_parts, path_parts):
        if pp.startswith(':'):
            if not pathp.replace('_', '').isalnum():
                return None
            params[pp[1:]] = pathp
    return params
