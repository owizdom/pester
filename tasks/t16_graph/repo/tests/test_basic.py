import unittest

from graph.graph import Graph
from graph.traversal import dfs


class BasicTest(unittest.TestCase):
    def test_add_edge_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        self.assertIn("B", g.neighbors("A"))

    def test_dfs_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        result = dfs(g, "A")
        self.assertEqual(set(result), {"A", "B", "C"})


if __name__ == "__main__":
    unittest.main()
