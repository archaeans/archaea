from src.geometry.border import Border
from src.simulation_objects.zone import Zone


class Domain:
    border: Border
    height: float
    context: "list[Border]"
    zones: "list[Zone]"

    def __init__(self, border, height, zones):
        self.border = border
        self.height = height
        self.zones = zones
