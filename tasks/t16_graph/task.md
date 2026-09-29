You are working in a small Python package, `graph/`, in the current directory. Users filed these issues:

1. BFS visits nodes more than once when multiple paths lead to the same node. The `visited` check is missing before enqueuing neighbors, so the result list contains duplicates.
2. `shortest_path(g, start, end)` returns a distance that is off by one (too small). It should return the number of edges on the shortest path.
3. `has_cycle` reports a false positive on directed acyclic graphs. It reuses the global `visited` set instead of tracking the current recursion stack, so a node visited from a different branch is mistaken for a back edge.
4. `add_edge` on an undirected graph only stores the edge in one direction. `neighbors("B")` is empty after `add_edge("A", "B")`.
5. `remove_node` deletes the node from the adjacency dict but leaves references to it in other nodes' neighbor lists.
6. New feature: `topological_sort()` returns a list of nodes in topological order for a directed acyclic graph. Raise `ValueError` if the graph is undirected or contains a cycle.

Fix all of these. Run the tests with `python3 -m unittest discover -s tests -t .` and add tests for your changes. When you are done, reply with a short summary.
