from src.geometry.face import Face
from src.geometry.point3d import Point3d
from src.simulation_objects.wall_type import WallType


class Wall(Face):
    border: Face
    openings: "list[Face]"
    wall_type: WallType
    has_hole: bool
    thickness: float

    def __init__(self, points: "list[Point3d]", openings: "list[Face]", wall_type: WallType, thickness=0.2):
        super().__init__(points)
        self.openings = openings
        self.wall_type = wall_type
        self.has_hole = len(openings) > 0
        self.thickness = thickness

    def to_stl(self):
        raise 'Not implemented'
