"""Cost functions for graph edges."""
from core.danger import danger_map


def maze_time(edge):
    """t(e) = length / speed."""
    return edge.length / edge.speed


def convoy_weight(edge, danger_cache, alpha):
    t_e = edge.length / edge.speed
    p_e = danger_cache.get(edge.id, 0.0)
    return t_e + alpha * p_e


def elevated_walking_time(edge):
    return edge.walking_time


def elevated_motorcycle_time(edge):
    return edge.motorcycle_time