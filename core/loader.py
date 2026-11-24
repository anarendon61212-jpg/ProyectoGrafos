"""Load scenario JSON files and build the two graphs (elevated and maze)."""
import json

from core.graph import (
    Graph,
    ElevatedVertex,
    ElevatedEdge,
    MazeVertex,
    MazeEdge,
)


def load_scenario(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    elevated = _build_elevated(data["elevated_graph"])
    maze = _build_maze(data["maze_graph"])

    base_id = _find_single_vertex(elevated, lambda v: v.is_base, "base")
    entry_id = _find_single_vertex(maze, lambda v: v.is_entry, "entry")
    exit_id = _find_single_vertex(maze, lambda v: v.is_exit, "exit")

    return {
        "params": data["params"],
        "elevated": elevated,
        "maze": maze,
        "convoy": data["convoy"],
        "base_id": base_id,
        "entry_id": entry_id,
        "exit_id": exit_id,
    }


def _build_elevated(graph_data):
    """Build the elevated graph G_E from the JSON section."""
    g = Graph("elevated")

    for v in graph_data["vertices"]:
        g.add_vertex(ElevatedVertex(v["id"], v["x"], v["y"], v["type"]))

    for e in graph_data["edges"]:
        bridge_kwargs = {}
        if e.get("is_bridge", False):
            bridge_kwargs = {
                "is_bridge": True,
                "max_resistance": e["max_resistance"],
                "rebuild_time": e["rebuild_time"],
            }
        g.add_edge(ElevatedEdge(
            e["id"],
            g.vertices[e["u"]],
            g.vertices[e["v"]],
            e["walking_time"],
            e["motorcycle_time"],
            **bridge_kwargs,
        ))

    return g


def _build_maze(graph_data):
    """Build the maze graph G_M from the JSON section."""
    g = Graph("maze")

    for v in graph_data["vertices"]:
        g.add_vertex(MazeVertex(
            v["id"], v["x"], v["y"],
            is_entry=v.get("is_entry", False),
            is_exit=v.get("is_exit", False),
        ))

    for e in graph_data["edges"]:
        g.add_edge(MazeEdge(
            e["id"],
            g.vertices[e["u"]],
            g.vertices[e["v"]],
            e["length"],
            e["speed"],
        ))

    return g


def _find_single_vertex(graph, predicate, label):
    """Return the id of the only vertex matching predicate. """
    matches = [vid for vid, v in graph.vertices.items() if predicate(v)]
    if len(matches) != 1:
        raise ValueError(f"Scenario must have exactly one {label} vertex, found {len(matches)}")
    return matches[0]