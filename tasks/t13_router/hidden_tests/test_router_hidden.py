import unittest

from router.route import Router, RouteGroup
from router.matcher import normalize_path, paths_equal, extract_params
from router.middleware import run_middleware


class TrailingSlashTests(unittest.TestCase):
    def test_slash_matches_no_slash(self):
        r = Router()
        r.add("/users", lambda ctx: "ok")
        result = r.match("/users/")
        self.assertIsNotNone(result)
        self.assertEqual(result[0]({}), "ok")

    def test_no_slash_matches_slash(self):
        r = Router()
        r.add("/users/", lambda ctx: "ok")
        result = r.match("/users")
        self.assertIsNotNone(result)

    def test_paths_equal_trailing(self):
        self.assertTrue(paths_equal("/users", "/users/"))
        self.assertTrue(paths_equal("/a/b/", "/a/b"))


class ParamDotsHyphensTests(unittest.TestCase):
    def test_dot_in_param(self):
        r = Router()
        r.add("/user/:name", lambda ctx: ctx)
        result = r.match("/user/john.doe")
        self.assertIsNotNone(result)
        self.assertEqual(result[1]["name"], "john.doe")

    def test_hyphen_in_param(self):
        r = Router()
        r.add("/item/:slug", lambda ctx: ctx)
        result = r.match("/item/my-item")
        self.assertIsNotNone(result)
        self.assertEqual(result[1]["slug"], "my-item")

    def test_extract_params_dots(self):
        params = extract_params([":file"], ["report.pdf"])
        self.assertIsNotNone(params)
        self.assertEqual(params["file"], "report.pdf")


class WildcardTests(unittest.TestCase):
    def test_wildcard_with_path(self):
        r = Router()
        r.add("/files/*", lambda ctx: ctx)
        result = r.match("/files/a/b")
        self.assertIsNotNone(result)
        self.assertEqual(result[1]["*"], "a/b")

    def test_wildcard_empty_path(self):
        r = Router()
        r.add("/files/*", lambda ctx: "found")
        result = r.match("/files/")
        self.assertIsNotNone(result)
        self.assertEqual(result[1]["*"], "")

    def test_wildcard_exact_prefix(self):
        r = Router()
        r.add("/files/*", lambda ctx: "found")
        result = r.match("/files")
        self.assertIsNotNone(result)


class PriorityTests(unittest.TestCase):
    def test_static_beats_dynamic(self):
        r = Router()
        r.add("/users/:id", lambda ctx: "dynamic")
        r.add("/users/new", lambda ctx: "static")
        result = r.match("/users/new")
        self.assertIsNotNone(result)
        self.assertEqual(result[0]({}), "static")

    def test_dynamic_beats_wildcard(self):
        r = Router()
        r.add("/files/*", lambda ctx: "wild")
        r.add("/files/:name", lambda ctx: "dynamic")
        result = r.match("/files/readme")
        self.assertEqual(result[0]({}), "dynamic")


class MiddlewareTests(unittest.TestCase):
    def test_context_passes_through_chain(self):
        def mw1(ctx, next_fn):
            ctx['step1'] = True
            ctx['value'] = 'from_mw1'
            return next_fn(ctx)

        def mw2(ctx, next_fn):
            ctx['step2'] = True
            ctx['saw_value'] = ctx.get('value')
            return next_fn(ctx)

        def handler(ctx):
            return ctx

        result = run_middleware([mw1, mw2], handler, {})
        self.assertTrue(result.get('step1'))
        self.assertTrue(result.get('step2'))
        self.assertEqual(result['saw_value'], 'from_mw1')


class RouteGroupTests(unittest.TestCase):
    def test_group_prefix(self):
        g = RouteGroup("/api")
        g.add("/users", lambda ctx: "users")
        g.add("/items", lambda ctx: "items")
        routes = g.routes()
        self.assertEqual(len(routes), 2)
        patterns = [r.pattern for r in routes]
        self.assertIn("/api/users", patterns)
        self.assertIn("/api/items", patterns)

    def test_group_middleware(self):
        def auth(ctx, next_fn):
            ctx['authed'] = True
            return next_fn(ctx)

        g = RouteGroup("/api")
        g.use(auth)
        g.add("/data", lambda ctx: ctx)
        routes = g.routes()
        self.assertEqual(len(routes[0].middleware), 1)

    def test_group_in_router(self):
        r = Router()
        g = RouteGroup("/api")
        g.add("/hello", lambda ctx: "hi")
        for route in g.routes():
            r.add(route.pattern, route.handler, route.middleware)
        result = r.match("/api/hello")
        self.assertIsNotNone(result)
        self.assertEqual(result[0]({}), "hi")


if __name__ == "__main__":
    unittest.main()
