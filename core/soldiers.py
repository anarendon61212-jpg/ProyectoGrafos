INFANTRY = "infantry"
SNIPER = "sniper"
ARTILLERY = "artillery"

SOLDIER_STATS = {
    INFANTRY:  {"cost": 100, "damage": 10,  "range": 5,  "frequency": 1.0},
    SNIPER:    {"cost": 300, "damage": 50,  "range": 20, "frequency": 0.5},
    ARTILLERY: {"cost": 500, "damage": 100, "range": 15, "frequency": 0.2},
}


class Soldier:


    def __init__(self, soldier_id, kind):
        if kind not in SOLDIER_STATS:
            raise ValueError(f"Unknown soldier type: {kind}")
        stats = SOLDIER_STATS[kind]
        self.id = soldier_id
        self.kind = kind
        self.damage = stats["damage"]
        self.base_range = stats["range"]
        self.frequency = stats["frequency"]
        self.cost = stats["cost"]
        self.tower = None
        self.position = None
        self.in_transit = False

    def effective_range(self, beta):
        z = self.tower.height if self.tower is not None else 0.0
        return self.base_range * (1.0 + beta * z)

    def can_attack(self):
        return not self.in_transit and self.tower is not None

    def __repr__(self):
        return f"Soldier({self.id}, {self.kind})"