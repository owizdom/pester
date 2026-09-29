"""Adjacency-list graph supporting directed and undirected modes."""


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self._adj = {}

    def add_node(self, node):
        """Ensure *node* exists in the graph."""
        if node not in self._adj:
            self._adj[node] = []

    def add_edge(self, u, v):
        """Add an edge from *u* to *v* (and v to u when undirected)."""
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append(v)
        if not self.directed:
            self._adj[v].append(u)

    def remove_node(self, node):
        """Remove *node* and all its edges from the graph."""
        if node not in self._adj:
            raise KeyError(node)
        del self._adj[node]
        for adj_list in self._adj.values():
            while node in adj_list:
                adj_list.remove(node)

    def neighbors(self, node):
        """Return the list of neighbors of *node*."""
        return list(self._adj.get(node, []))

    def nodes(self):
        """Return all nodes in the graph."""
        return list(self._adj.keys())

    def has_edge(self, u, v):
        """Return True if there is an edge from *u* to *v*."""
        return v in self._adj.get(u, [])
