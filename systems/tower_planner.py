"""Tower planning based on the MST."""
import math

def plan_towers(
    elevated_graph,
    maze_graph,
    base_id,
    candidate_ids,
    vigilance_radii,
    tree_edges,
    weight_fn,
    K,
    D0,
):
    """Return the list of chosen candidate ids, in selection order."""
    distance_on_tree = _distances_on_tree(tree_edges, base_id, weight_fn)

    uncovered_edges = {edge.id: edge for edge in maze_graph.get_all_edges()}
    total_corridor_length = sum(
        math.hypot(edge.v.x - edge.u.x, edge.v.y - edge.u.y)
        for edge in maze_graph.get_all_edges()
    )

    chosen = []
    covered_length = 0.0

    while len(chosen) < K:
        best_id = None
        best_score = -1.0
        best_newly_covered = []

        for candidate_id in candidate_ids:
            if candidate_id in chosen:
                continue

            vertex = elevated_graph.vertices[candidate_id]
            radius = vigilance_radii[candidate_id]

            newly_covered = _edges_covered_by(
                vertex, radius, uncovered_edges
            )
            if not newly_covered:
                continue

            covered_now = sum(
                math.hypot(edge.v.x - edge.u.x, edge.v.y - edge.u.y)
                for edge in newly_covered
            )

            dist_on_tree = distance_on_tree.get(candidate_id, float("inf"))
            if dist_on_tree == float("inf"):
                continue

            score = covered_now / ((1.0 + dist_on_tree) / D0)

            if score > best_score:
                best_score = score
                best_id = candidate_id
                best_newly_covered = newly_covered

        if best_id is None:
            break

        chosen.append(best_id)
        covered_length += sum(
            math.hypot(edge.v.x - edge.u.x, edge.v.y - edge.u.y)
            for edge in best_newly_covered
        )
        for edge in best_newly_covered:
            uncovered_edges.pop(edge.id, None)

    return chosen, covered_length, total_corridor_length


def _distances_on_tree(tree_edges, source_id, weight_fn):
    """Distances from source_id following only the MST edges."""
    adjacency = {}
    for edge in tree_edges:
        adjacency.setdefault(edge.u.id, []).append((edge.v.id, weight_fn(edge)))
        adjacency.setdefault(edge.v.id, []).append((edge.u.id, weight_fn(edge)))

    distances = {source_id: 0.0}
    stack = [source_id]
    while stack:
        current = stack.pop()
        for neighbor_id, weight in adjacency.get(current, []):
            new_distance = distances[current] + weight
            if neighbor_id not in distances or new_distance < distances[neighbor_id]:
                distances[neighbor_id] = new_distance
                stack.append(neighbor_id)
    return distances


def _edges_covered_by(vertex, radius, candidate_edges):
    covered = []
    for edge in candidate_edges.values():
        mid_x = (edge.u.x + edge.v.x) / 2.0
        mid_y = (edge.u.y + edge.v.y) / 2.0
        dist = math.hypot(mid_x - vertex.x, mid_y - vertex.y)
        if dist <= radius:
            covered.append(edge)
    return covered