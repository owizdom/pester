"""Graph algorithms: shortest path, cycle detection, topological sort."""

from collections import deque


def shortest_path(graph, start, end):
    """Return the shortest-path distance (edge count) from *start* to *end*.

    Returns -1 when no path exists.
    """
    if start == end:
        return 0
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        for neighbor in graph.neighbors(node):
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1


def has_cycle(graph):
    """Return True if the graph contains at least one cycle."""
    visited = set()
    rec_stack = set()

    def _dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                if _dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    for node in graph.nodes():
        if node not in visited:
            if _dfs(node):
                return True
    return False


def topological_sort(graph):
    """Return nodes in topological order.

    Raises ValueError for undirected graphs or graphs with cycles.
    """
    if not graph.directed:
        raise ValueError("topological sort requires a directed graph")
    if has_cycle(graph):
        raise ValueError("graph contains a cycle")

    visited = set()
    order = []

    def _dfs(node):
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                _dfs(neighbor)
        order.append(node)

    for node in graph.nodes():
        if node not in visited:
            _dfs(node)

    order.reverse()
    return order
