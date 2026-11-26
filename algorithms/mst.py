"""Minimum Spanning Tree using Kruskal's algorithm."""

def kruskal_mst(graph, base_id, weight_fn):
    component = _connected_component(graph, base_id)

    candidate_edges = []
    for edge in graph.get_all_edges():
        origin_in_component = edge.u.id in component
        destination_in_component = edge.v.id in component
        if origin_in_component and destination_in_component and edge.enabled:
            candidate_edges.append(edge)

    candidate_edges.sort(key=lambda edge: (weight_fn(edge), edge.id))
    parent = {}
    for vertex_id in component:
        parent[vertex_id] = vertex_id

    def find(vertex_id):
        while parent[vertex_id] != vertex_id:
            parent[vertex_id] = parent[parent[vertex_id]] 
            vertex_id = parent[vertex_id]
        return vertex_id

    def union(vertex_a, vertex_b):
        root_a = find(vertex_a)
        root_b = find(vertex_b)
        if root_a == root_b:
            return False
        parent[root_b] = root_a
        return True

    tree_edges = []
    total_weight = 0.0
    for edge in candidate_edges:
        origin_id = edge.u.id
        destination_id = edge.v.id
        if union(origin_id, destination_id):
            tree_edges.append(edge)
            total_weight += weight_fn(edge)

    return tree_edges, total_weight


def _connected_component(graph, start_id):
    """BFS from start_id returning the set of ids reachable from it."""
    visited = set()
    stack = [start_id]
    while stack:
        current_id = stack.pop()
        if current_id in visited:
            continue
        visited.add(current_id)
        for neighbor_vertex, _ in graph.get_neighbors(current_id):
            if neighbor_vertex.id not in visited:
                stack.append(neighbor_vertex.id)
    return visited