"""Tower entity.
"Towers hold up to three soldiers."
It also stores a height (z) used to compute effective soldier range.
"""
class Tower:
    MAX_SOLDIERS = 3

    def __init__(self, tower_id, vertex, height=0.0):
        if vertex.type != "Candidate":
            raise ValueError(f"Tower must be on a Candidate vertex, got {vertex.type}")
        self.id = tower_id
        self.vertex = vertex
        self.height = height
        self.soldiers = []

    def free_capacity(self):
        """How many more soldiers can enter this tower."""
        return self.MAX_SOLDIERS - len(self.soldiers)

    def can_accept(self, soldier):
        """Return True if the soldier can enter without breaking any rule."""
        if soldier in self.soldiers:
            return False
        return self.free_capacity() > 0

    def add_soldier(self, soldier):
        if not self.can_accept(soldier):
            raise ValueError(f"Cannot add soldier {soldier.id} to tower {self.id}")
        self.soldiers.append(soldier)
        soldier.tower = self
        soldier.position = self.vertex
        soldier.in_transit = False

    def remove_soldier(self, soldier):
        if soldier not in self.soldiers:
            raise ValueError(f"Soldier {soldier.id} is not in tower {self.id}")
        self.soldiers.remove(soldier)
        soldier.tower = None
        soldier.position = None

    def __repr__(self):
        return f"Tower({self.id}, soldiers={len(self.soldiers)}/{self.MAX_SOLDIERS})"