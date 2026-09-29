import unittest

from graph.graph import Graph
from graph.traversal import bfs, dfs
from graph.algorithms import shortest_path, has_cycle

try:
    from graph.algorithms import topological_sort
except ImportError:
    topological_sort = None


class BfsHidden(unittest.TestCase):
    def test_no_duplicates(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        result = bfs(g, "A")
        self.assertEqual(len(result), len(set(result)))
        self.assertEqual(set(result), {"A", "B", "C"})

    def test_bfs_order(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        result = bfs(g, "A")
        self.assertEqual(result[0], "A")
        self.assertLess(result.index("B"), result.index("D"))
        self.assertLess(result.index("C"), result.index("D"))


class ShortestPathHidden(unittest.TestCase):
    def test_adjacent(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        self.assertEqual(shortest_path(g, "A", "B"), 1)

    def test_two_hops(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        self.assertEqual(shortest_path(g, "A", "C"), 2)

    def test_same_node(self):
        g = Graph(directed=True)
        g.add_node("A")
        self.assertEqual(shortest_path(g, "A", "A"), 0)

    def test_no_path(self):
        g = Graph(directed=True)
        g.add_node("A")
        g.add_node("B")
        self.assertEqual(shortest_path(g, "A", "B"), -1)


class CycleHidden(unittest.TestCase):
    def test_dag_no_false_positive(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        self.assertFalse(has_cycle(g))

    def test_real_cycle(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "A")
        self.assertTrue(has_cycle(g))


class UndirectedEdgeHidden(unittest.TestCase):
    def test_both_directions(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        self.assertIn("B", g.neighbors("A"))
        self.assertIn("A", g.neighbors("B"))


class RemoveNodeHidden(unittest.TestCase):
    def test_removes_dangling_refs(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("C", "B")
        g.remove_node("B")
        self.assertNotIn("B", g.neighbors("A"))
        self.assertNotIn("B", g.neighbors("C"))
        self.assertNotIn("B", g.nodes())


class TopSortHidden(unittest.TestCase):
    def test_basic_order(self):
        if topological_sort is None:
            self.fail("topological_sort not implemented")
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        order = topological_sort(g)
        self.assertLess(order.index("A"), order.index("B"))
        self.assertLess(order.index("B"), order.index("C"))

    def test_diamond(self):
        if topological_sort is None:
            self.fail("topological_sort not implemented")
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        g.add_edge("C", "D")
        order = topological_sort(g)
        self.assertLess(order.index("A"), order.index("B"))
        self.assertLess(order.index("A"), order.index("C"))
        self.assertLess(order.index("B"), order.index("D"))
        self.assertLess(order.index("C"), order.index("D"))

    def test_cycle_raises(self):
        if topological_sort is None:
            self.fail("topological_sort not implemented")
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "A")
        with self.assertRaises(ValueError):
            topological_sort(g)

    def test_undirected_raises(self):
        if topological_sort is None:
            self.fail("topological_sort not implemented")
        g = Graph(directed=False)
        g.add_edge("A", "B")
        with self.assertRaises(ValueError):
            topological_sort(g)


if __name__ == "__main__":
    unittest.main()
