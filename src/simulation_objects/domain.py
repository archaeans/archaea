from src.geometry.face import Face
from src.simulation_objects.zone import Zone


class Domain:
    border: Face
    height: float
    context: "list[Face]"
    zones: "list[Zone]"

    def __init__(self, border, height, zones):
        self.border = border
        self.height = height
        self.zones = zones
