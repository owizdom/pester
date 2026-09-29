"""Middleware chain execution."""


def run_middleware(middleware_list, handler, context):
    """Run a list of middleware functions, then the handler.
    Each middleware is called as middleware(context, next_fn).
    BUG: each middleware gets the original context, not the
    one modified by previous middleware."""
    ctx = dict(context)

    def run(index):
        if index >= len(middleware_list):
            return handler(ctx)
        mw = middleware_list[index]
        # BUG: passes original ctx to each, not the evolving one
        original = dict(context)

        def next_fn(c):
            return run(index + 1)

        return mw(original, next_fn)

    return run(0)


def logging_middleware(context, next_fn):
    """Example middleware that adds a log entry to context."""
    context['logged'] = True
    return next_fn(context)


def auth_middleware(context, next_fn):
    """Example middleware that checks for an auth token."""
    if 'token' not in context:
        return {'error': 'unauthorized'}
    return next_fn(context)
