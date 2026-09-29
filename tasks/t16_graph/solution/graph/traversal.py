"""BFS and DFS traversal helpers."""

from collections import deque


def bfs(graph, start):
    """Return nodes reachable from *start* in breadth-first order."""
    result = []
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result


def dfs(graph, start):
    """Return nodes reachable from *start* in depth-first order."""
    visited = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.append(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                stack.append(neighbor)
    return visited
