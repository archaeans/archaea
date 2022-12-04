from src.geometry.border import Border
from src.geometry.point3d import Point3d
from src.simulation_objects.wall_type import WallType


class Wall(Border):
    border: Border
    openings: "list[Border]"
    wall_type: WallType
    has_hole: bool

    def __init__(self, points: "list[Point3d]", openings: "list[Border]", wall_type: WallType):
        super().__init__(points)
        self.openings = openings
        self.wall_type = wall_type
        self.has_hole = len(openings) > 0

    def to_stl(self):
        raise 'Not implemented'
