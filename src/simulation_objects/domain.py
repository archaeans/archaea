from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.loop import Loop
from src.geometry.face import Face
from src.simulation_objects.wall import Wall
from src.simulation_objects.wall_type import WallType
from src.simulation_objects.zone import Zone


class Domain(Zone):
    center: Point3d
    ground: Face
    x: float
    y: float
    z: float
    zones: "list[Zone]"
    context: "list[Wall]"
    openings: "list[Wall]"

    def __init__(self, center: Point3d, x: float, y: float, z: float, zones=None, context=None):
        if context is None:
            context = []
        if zones is None:
            zones = []
        self.center = center
        self.x = x
        self.y = y
        self.z = z
        self.zones = zones
        self.context = context
        ground = self.init_ground()
        super().__init__(ground, self.z, wall_default_thickness=0)
        self.ground = self.floor

    def init_ground(self) -> Face:
        c = self.center
        ground_outer_loop = Loop([
            c.move(Vector3d(self.x / 2 * -1, self.y / 2 * -1, 0)),  # left-bottom
            c.move(Vector3d(self.x / 2 * -1, self.y / 2, 0)),  # left-top
            c.move(Vector3d(self.x / 2, self.y / 2, 0)),  # right-top
            c.move(Vector3d(self.x / 2, self.y / 2 * -1, 0)),  # right-bottom
        ])
        ground_inner_loops = [zone.floor.wall_border for zone in self.zones if zone.floor.wall_border.normal.z == 0]
        ground = Face(ground_outer_loop, ground_inner_loops)
        return ground

    def add_zone(self, zone: Zone):
        self.zones.append(zone)
        if zone.floor.wall_border.point_at_start.z == 0:
            self.floor.add_opening(zone.floor.wall_border.reverse())

    def create_solid_faces(self):
        faces = [self.floor.reverse(), self.ceiling.reverse()]
        faces += self.walls

        for zone in self.zones:
            faces += zone.create_solid_faces()

        return faces

