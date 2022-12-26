from src.geometry.border import Border
from src.geometry.vector3d import Vector3d


class Zone:
    floor: Border
    ceiling: Border
    walls: "list[Border]"
    height: float
    volume: float
    openings: "list[Border]"

    def __init__(self, border, height, walls=None):
        self.floor = border
        self.height = height
        self.volume = self.floor.area * height
        move_vector = Vector3d(0, 0, self.height)
        self.ceiling = self.floor.move(move_vector)
        if walls is None:
            self.create_walls(move_vector)
        else:
            self.walls = walls

    def create_walls(self, move_vector):
        wall_lines = self.floor.segments
        walls = []
        for line in wall_lines:
            border = line.extrude(move_vector)
            walls.append(border)
        self.walls = walls
