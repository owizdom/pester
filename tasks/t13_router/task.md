You are working in a small Python package, `router/`, in the current directory. Users filed these issues:

1. Trailing slash mismatch: `/users/` does not match a route registered as `/users`, and vice versa. Routes should match regardless of a trailing slash.
2. Path parameter extraction fails when the value contains dots or hyphens. For example, `/user/john.doe` should match `/user/:name` and extract `name` as `"john.doe"`, but currently only alphanumeric characters are captured.
3. Wildcard routes (`/files/*`) do not match when the path after the prefix is empty. `/files/` or `/files` should match `/files/*` with the wildcard value being empty string.
4. Route priority is wrong: a static route like `/users/new` should always beat a dynamic route like `/users/:id`, but currently whichever was registered first wins.
5. Middleware chain does not pass modified request context forward. When one middleware adds a key to the context dict, the next middleware and the final handler should see it.

New feature: add `RouteGroup(prefix)` in `route.py` that lets you group routes under a shared prefix with shared middleware. It should have `add(path, handler)` and `use(middleware)` methods, and a `routes()` method that returns the expanded route list with the prefix prepended and middleware applied.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
