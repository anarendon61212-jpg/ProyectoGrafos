class TransportOrder:
    def __init__(self, soldiers, route, mode, destination_tower):
        self.soldiers = soldiers
        self.route = route
        self.mode = mode
        self.destination_tower = destination_tower
        
        self.progress = 0.0
        self.status = "moving"