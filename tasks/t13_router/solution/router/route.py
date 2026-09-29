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
        """Find the best matching route for a path.
        Static routes beat dynamic routes. Returns (handler, params, mw) or None."""
        path = _normalize(path)
        best = None
        best_priority = -1
        for route in self._routes:
            params = _match_route(route, path)
            if params is not None:
                p = _priority(route)
                if p > best_priority:
                    best = (route.handler, params, route.middleware)
                    best_priority = p
        return best


class RouteGroup:
    """Group routes under a shared prefix with shared middleware."""

    def __init__(self, prefix):
        self.prefix = prefix.rstrip('/')
        self._routes = []
        self._middleware = []

    def add(self, path, handler):
        self._routes.append((path, handler))

    def use(self, middleware):
        self._middleware.append(middleware)

    def routes(self):
        result = []
        for path, handler in self._routes:
            full = self.prefix + ('/' + path.strip('/') if path.strip('/') else '')
            result.append(Route(full, handler, list(self._middleware)))
        return result


def _normalize(path):
    """Strip trailing slash for matching (but keep root as /)."""
    if path != '/' and path.endswith('/'):
        path = path.rstrip('/')
    return path


def _priority(route):
    """Higher number means higher priority. Static > dynamic > wildcard."""
    if route.is_wildcard:
        return 0
    if route.is_dynamic:
        return 1
    return 2


def _match_route(route, path):
    """Match a route against a normalized path. Returns params dict or None."""
    path = _normalize(path)
    path_parts = path.strip('/').split('/') if path != '/' else ['']

    norm_pattern = _normalize(route.pattern)
    route_parts = norm_pattern.strip('/').split('/') if norm_pattern != '/' else ['']

    if route.is_wildcard:
        prefix = route_parts[:-1]  # everything before *
        if len(path_parts) < len(prefix):
            return None
        for rp, pp in zip(prefix, path_parts):
            if rp.startswith(':'):
                pass
            elif rp != pp:
                return None
        if len(path_parts) < len(prefix):
            return None
        wildcard_val = '/'.join(path_parts[len(prefix):]) if len(path_parts) > len(prefix) else ''
        return {'*': wildcard_val}

    if len(route_parts) != len(path_parts):
        return None

    params = {}
    for rpart, ppart in zip(route_parts, path_parts):
        if rpart.startswith(':'):
            if not ppart:
                return None
            params[rpart[1:]] = ppart
        elif rpart != ppart:
            return None

    return params
