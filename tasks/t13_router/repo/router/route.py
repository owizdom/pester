"""Route definition and registration."""


class Route:
    """A single route with a pattern, handler, and optional middleware."""

    def __init__(self, pattern, handler, middleware=None):
        self.pattern = pattern
        self.handler = handler
        self.middleware = middleware or []
        self.parts = pattern.strip('/').split('/') if pattern != '/' else ['']
        self.is_dynamic = any(p.startswith(':') for p in self.parts)
        self.is_wildcard = pattern.endswith('/*')


class Router:
    """Collects routes and dispatches paths to handlers."""

    def __init__(self):
        self._routes = []

    def add(self, pattern, handler, middleware=None):
        self._routes.append(Route(pattern, handler, middleware))

    def match(self, path):
        """Find the first matching route for a path.
        Returns (handler, params, middleware) or None.
        BUG: no priority sorting -- first registered wins."""
        for route in self._routes:
            params = _match_route(route, path)
            if params is not None:
                return route.handler, params, route.middleware
        return None


def _match_route(route, path):
    """Try to match a route against a path. Returns params dict or None.
    BUG: trailing slash not normalized.
    BUG: param values only match [a-zA-Z0-9_]."""
    # BUG: no trailing slash normalization
    path_parts = path.strip('/').split('/') if path != '/' else ['']

    if route.is_wildcard:
        prefix = route.parts[:-1]  # everything before *
        if len(path_parts) < len(prefix):
            return None
        for rp, pp in zip(prefix, path_parts):
            if rp.startswith(':'):
                pass
            elif rp != pp:
                return None
        # BUG: doesn't match when path_parts == prefix (empty wildcard)
        if len(path_parts) == len(prefix):
            return None
        wildcard_val = '/'.join(path_parts[len(prefix):])
        return {'*': wildcard_val}

    if len(route.parts) != len(path_parts):
        return None

    params = {}
    for rpart, ppart in zip(route.parts, path_parts):
        if rpart.startswith(':'):
            # BUG: only allows alphanumeric + underscore
            if not ppart.replace('_', '').isalnum():
                return None
            params[rpart[1:]] = ppart
        elif rpart != ppart:
            return None

    return params
