"""Graph algorithms: shortest path, cycle detection."""

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
                return dist
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1


def has_cycle(graph):
    """Return True if the graph contains at least one cycle."""
    visited = set()

    def _dfs(node):
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor in visited:
                return True
            if _dfs(neighbor):
                return True
        return False

    for node in graph.nodes():
        if node not in visited:
            if _dfs(node):
                return True
    return False
