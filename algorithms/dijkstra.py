""" Dijkstra shortest paths without external graph libraries """
import heapq

def dijkstra(graph,source_id,weight_fn,target_id=None):
    """ Find minimum cost from source to every reachable vertex."""
    dist={}
    for vid in graph.vertices:
        dist[vid]=float('inf')
    prev={}
    for vid in graph.vertices:
        prev[vid]=None
    dist[source_id]=0.0
    visited=set()
    heap=[(0.0,source_id)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        if u == target_id:
            break

        for neighbor, edge in graph.get_neighbors(u):
            w = weight_fn(edge)
            if w < 0:
                raise ValueError("negative weight on edge " + str(edge.id))

            new_d = d + w
            if new_d < dist[neighbor.id]:
                dist[neighbor.id] = new_d
                prev[neighbor.id] = (u, edge)   # u is a string id; edge.u is a Vertex
                heapq.heappush(heap, (new_d, neighbor.id))

    return dist, prev


def build_path(prev, target_id):
    """Reconstruct path from source to target as a list of Edge objects.
    Returns [] if target is unreachable.
    """
    path = []
    node = target_id

    while prev[node] is not None:
        parent, edge = prev[node]
        path.append(edge)
        node = parent

    path.reverse()
    return path

