import functools
from src.geometry.face import Face
from src.geometry.loop import Loop
from src.simulation_objects.wall_type import WallType


class Wall(Face):
    border: Face
    openings: "list[Loop]"
    wall_type: WallType
    has_hole: bool
    thickness: float

    def __init__(self, border: Loop, openings: "list[Loop]", wall_type: WallType, thickness=0.2):
        super().__init__(border, inner_loops=openings)
        self.openings = openings
        self.wall_type = wall_type
        self.has_hole = len(openings) > 0
        self.thickness = thickness

    @functools.cached_property
    def gross_wall_area(self):
        return self.outer_loop.area

    @functools.cached_property
    def net_wall_area(self):
        return self.area

    @functools.cached_property
    def openings_area(self):
        return self.gross_wall_area - self.net_wall_area
