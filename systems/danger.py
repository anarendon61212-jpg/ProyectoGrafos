"""Danger estimation for maze corridors."""
import math


def _midpoint(edge):
    """Euclidean midpoint between the two endpoints of the edge."""
    x = (edge.u.x + edge.v.x) / 2.0
    y = (edge.u.y + edge.v.y) / 2.0
    return x, y


def _damage_rate_at(x, y, soldiers, beta):
    """D(q) = sum of damage * frequency over soldiers that cover (x, y)."""
    total = 0.0
    for s in soldiers:
        if not s.can_attack():
            continue
        tx = s.tower.vertex.x
        ty = s.tower.vertex.y
        dist = math.hypot(tx - x, ty - y)
        if dist <= s.effective_range(beta):
            total += s.damage * s.frequency
    return total


def corridor_danger(edge, soldiers, beta):
    """Return P(e) for one corridor,
    soldiers: iterable of Soldier instances (only those with a tower count).
    beta    : scenario coefficient for effective range.
    """
    t_e = edge.length / edge.speed
    d_start = _damage_rate_at(edge.u.x, edge.u.y, soldiers, beta)
    mx, my = _midpoint(edge)
    d_mid = _damage_rate_at(mx, my, soldiers, beta)
    d_end = _damage_rate_at(edge.v.x, edge.v.y, soldiers, beta)
    avg = (d_start + d_mid + d_end) / 3.0
    return avg * t_e


def danger_map(maze_graph, soldiers, beta):
    """Return {edge_id: P(e)} for every edge in the maze."""
    return {eid: corridor_danger(e, soldiers, beta) for eid, e in maze_graph.edges.items()}