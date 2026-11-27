import math

from algorithms.dijkstra import dijkstra, build_path
from systems.tower_planner import plan_towers
from core.weights import maze_time, convoy_weight, elevated_walking_time
from systems.danger import danger_map
from entities.orders import TransportOrder

class Simulation:
    def __init__(self, scenario_data):
        self.params = scenario_data["params"]
        self.elevated = scenario_data["elevated"]
        self.maze = scenario_data["maze"]
        self.base_id = scenario_data["base_id"]
        self.entry_id = scenario_data["entry_id"]
        self.exit_id = scenario_data["exit_id"]
        
        self.current_time = 0.0
        self.is_game_over = False
        self.result = None
        self.budget = self.params["budget"]
        
        self.towers = []
        self.soldiers = [] 
        self.transit_order = []
        

    def update(self, dt):
        if self.is_game_over:
            return

        self.current_time += dt

        self._update_bridges()
        
        self._update_soldiers(dt)
        
        self._update_combat(dt)
        
        self._update_convoy(dt)
        
        self._check_game_over()


    def _update_bridges(self):
        for edge in self.elevated.get_all_edges():
            if edge.is_bridge and not edge.enabled:
                if self.current_time >= edge.rebuild_at:
                    edge.enabled = True
                    edge.current_resistance = edge.max_resistance
                    edge.rebuild_at = None


    def _update_soldiers(self, dt):
        for order in list(self.transit_order):
            
            if order.status != "moving":
                continue
            
            edge = order.route[0]
            
            if order.mode == "walking":
                order.progress += dt / edge.walking_time
                
            elif order.mode == "motorcycle":
                order.progress += dt / edge.motorcycle_time
                
            else:
                raise ValueError(f"Error: {order.mode}")
            
            if order.progress >= 1.0:
                order.progress = 0.0
                order.route.pop(0)
                if (order.mode == "motorcycle" and edge.is_bridge):
                    edge.current_resistance -= 1
                    if edge.current_resistance <= 0:
                        edge.enabled = False
                        edge.rebuild_at = self.current_time + edge.rebuild_time
                        
                if not order.route:
                    for soldier in order.soldiers:
                        order.destination_tower.add_soldier(soldier)
                    order.destination_tower.reserved_slots -= len(order.soldiers)
                    self.transit_order.remove(order)


    