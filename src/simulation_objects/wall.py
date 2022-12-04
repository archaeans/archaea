from src.geometry.border import Border
from src.simulation_objects.wall_type import WallType


class Wall:
    border: Border
    openings: "list[Border]"
    wall_type: WallType
    has_hole: bool

    def __init__(self, border: Border, openings: "list[Border]", wall_type: WallType):
        self.border = border
        self.openings = openings
        self.wall_type = wall_type
        self.has_hole = len(openings) > 0

    def center(self):
        self.border

    def to_stl(self):
        raise 'Not implemented'
