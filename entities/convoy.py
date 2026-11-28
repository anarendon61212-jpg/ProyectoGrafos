class Machine:
    def __init__(self, machine_id, kind):
        self.id = machine_id
        self.kind = kind
        
        if kind == "tank":
            self.max_hp = 200
            self.hp = 200
            self.reward = 150
        elif kind == "truck":
            self.max_hp = 100
            self.hp = 100
            self.reward = 100
        elif kind == "robot":
            self.max_hp = 50
            self.hp = 50
            self.reward = 50

    def is_alive(self):
        return self.hp > 0


class Convoy:
    def __init__(self, convoy_data):
        self.machines = []
        
        for i in range(convoy_data.get("tanks", 0)):
            self.machines.append(Machine(f"tank_{i}", "tank"))
        for i in range(convoy_data.get("trucks", 0)):
            self.machines.append(Machine(f"truck_{i}", "truck"))
        for i in range(convoy_data.get("robot_soldiers", 0)):
            self.machines.append(Machine(f"robot_{i}", "robot"))

        self.current_vertex = None
        self.previous_vertex = None
        self.route = []
        self.transit_progress = 0.0
        self.current_edge = None

    def is_defeated(self):
        return all(not m.is_alive() for m in self.machines)

    def get_first_alive(self):
        for m in self.machines:
            if m.is_alive():
                return m
        return None