import unittest

from router.route import Router


class BasicTest(unittest.TestCase):
    def test_static_route(self):
        r = Router()
        r.add("/hello", lambda ctx: "hi")
        handler, params, mw = r.match("/hello")
        self.assertEqual(handler({}), "hi")
        self.assertEqual(params, {})

    def test_param_route(self):
        r = Router()
        r.add("/user/:id", lambda ctx: ctx)
        handler, params, mw = r.match("/user/42")
        self.assertEqual(params, {"id": "42"})


if __name__ == "__main__":
    unittest.main()
