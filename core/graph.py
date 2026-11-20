class Vertex:
    def __init__(self, vertex_id, x, y):
        self.id = vertex_id
        self.x = x
        self.y = y

    def get_coordinates(self):
        return (self.x, self.y)

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2)**0.5


class ElevatedVertex(Vertex):
    def __init__(self, vertex_id, x, y, position_type):
        super().__init__(vertex_id, x, y)
        self.type = position_type
        self.is_base = position_type == "Base"


class MazeVertex(Vertex):
    def __init__(self, vertex_id, x, y, is_entry=False, is_exit=False):
        super().__init__(vertex_id, x, y)
        self.is_entry = is_entry
        self.is_exit = is_exit


class Edge:
    def __init__(self, edge_id, u, v):
        self.id = edge_id
        self.u = u
        self.v = v
        self.enabled = True


class ElevatedEdge(Edge):
    def __init__(self, edge_id, u, v, walking_time, motorcycle_time,  is_bridge=False, max_resistance=None, rebuild_time=None):

        super().__init__(edge_id, u, v)

        self.walking_time = walking_time
        self.motorcycle_time = motorcycle_time
        self.is_bridge = is_bridge

        if is_bridge:
            if max_resistance is None or max_resistance <= 0:
                raise ValueError("Invalid bridge resistance")

            if rebuild_time is None or rebuild_time <= 0:
                raise ValueError("Invalid rebuild time")

            self.max_resistance = max_resistance
            self.current_resistance = max_resistance
            self.rebuild_time = rebuild_time
            self.rebuild_at = None

        else:
            self.max_resistance = None
            self.current_resistance = None
            self.rebuild_time = None
            self.rebuild_at = None


class MazeEdge(Edge):
    def __init__(self, edge_id, u, v, length, speed):
        super().__init__(edge_id, u, v)

        self.length = length
        self.speed = speed


class Graph:
    def __init__(self, name):
        self.name = name
        self.vertices = {}
        self.edges = {}
        self.adjacency = {}

    def add_vertex(self, vertex):
        if vertex.id in self.vertices:
            raise ValueError("Vertex already exists")

        self.vertices[vertex.id] = vertex
        self.adjacency[vertex.id] = []

    def add_edge(self, edge):
        if edge.id in self.edges:
            raise ValueError("Edge already exists")

        if edge.u.id not in self.vertices or edge.v.id not in self.vertices:
            raise ValueError("Vertex does not exist")

        if edge.u.id == edge.v.id:
            raise ValueError("A vertex cannot connect to itself")

        self.edges[edge.id] = edge

        self.adjacency[edge.u.id].append(edge)
        self.adjacency[edge.v.id].append(edge)

    def get_neighbors(self, vertex_id):
        neighbors = []

        for edge in self.adjacency[vertex_id]:
            if edge.enabled:
                if edge.u.id == vertex_id:
                    neighbors.append((edge.v, edge))
                else:
                    neighbors.append((edge.u, edge))

        return neighbors

    def get_all_edges(self):
        return list(self.edges.values())
