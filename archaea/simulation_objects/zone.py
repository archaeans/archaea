from archaea.geometry.face import Face
from archaea.geometry.vector3d import Vector3d
from archaea.simulation_objects.wall import Wall
from archaea.simulation_objects.wall_type import WallType


class Zone:
    floor: Wall
    ceiling: Wall
    walls: "list[Wall]"
    height: float
    volume: float
    wall_default_thickness: float
    openings: "list[Face]"

    def __init__(self, floor: Face, height, walls=None, wall_default_thickness=0.1):
        self.floor = Wall(floor.outer_loop, floor.inner_loops)
        self.floor.update_wall_type(WallType.INNER)
        self.height = height
        self.wall_default_thickness = wall_default_thickness
        self.volume = self.floor.area * height
        move_vector = Vector3d(0, 0, self.height)
        self.ceiling = self.floor.move(move_vector).reverse()
        if walls is None:
            self.create_walls(move_vector)
        else:
            self.walls = walls

    def create_walls(self, move_vector):
        wall_lines = self.floor.outer_loop.segments
        walls = []
        for line in wall_lines:
            border: Face = line.extrude(move_vector)
            wall = Wall(border.outer_loop, border.inner_loops)
            walls.append(wall)
        self.walls = walls

    def create_solid_faces(self):
        all_walls = self.walls
        all_walls.append(self.floor.reverse())
        all_walls.append(self.ceiling.reverse())

        faces = []
        for wall in all_walls:
            faces += wall.create_solid_faces()

        return faces
