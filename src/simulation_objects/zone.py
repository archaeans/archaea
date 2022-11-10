from src.geometry.border import Border
from src.geometry.vector3d import Vector3d


class Zone:
    floor: Border
    ceiling: Border
    walls: "list[Border]"
    height: float
    volume: float

    def __init__(self, border, height):
        self.floor = border
        self.height = height
        self.volume = self.floor.area * height
        self.create_zone()

    def create_zone(self):
        wall_lines = self.floor.segments
        move_vector = Vector3d(0, 0, self.height)
        walls = []
        for line in wall_lines:
            border = line.extrude(move_vector)
            walls.append(border)
        self.walls = walls
        self.ceiling = self.floor.move(move_vector)

