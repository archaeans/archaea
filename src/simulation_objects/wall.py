from src.geometry.border import Border
from src.geometry.vector3d import Vector3d


class Wall:
    border: Border
    openings: "list[Border]"

    def __init__(self, border, openings):
        self.border = border
        self.openings = openings

