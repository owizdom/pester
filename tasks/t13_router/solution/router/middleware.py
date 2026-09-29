"""Middleware chain execution."""


def run_middleware(middleware_list, handler, context):
    """Run a list of middleware functions, then the handler.
    Each middleware is called as middleware(context, next_fn).
    The context modifications from each middleware carry forward."""
    ctx = dict(context)

    def run(index):
        if index >= len(middleware_list):
            return handler(ctx)
        mw = middleware_list[index]

        def next_fn(c):
            ctx.update(c)
            return run(index + 1)

        return mw(ctx, next_fn)

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
