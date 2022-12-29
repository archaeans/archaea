import unittest
from src.geometry.vector3d import Vector3d
from src.geometry.point3d import Point3d
from src.geometry.loop import Loop
from src.geometry.face import Face
from src.geometry.mesh import Mesh
from src.simulation_objects.wall import Wall
from src.simulation_objects.zone import Zone
from src.simulation_objects.wall_type import WallType


class Setup(unittest.TestLoader):
    # ground loop
    p0 = Point3d(0, 0, 0)
    p1 = Point3d(4, 0, 0)
    p2 = Point3d(4, 4, 0)
    p3 = Point3d(0, 4, 0)

    ground_loop = Loop([p0, p3, p2, p1])
    ground_face = Face(ground_loop)
    ground_wall = Wall(ground_face.outer_loop, ground_face.inner_loops, wall_type=WallType.INNER)

    zone = Zone(ground_face, 3)

    # outer wall
    p4 = Point3d(0, 0, 0)
    p5 = Point3d(4, 0, 0)
    p6 = Point3d(4, 0, 3)
    p7 = Point3d(0, 0, 3)

    # outer wall hole loop
    p8 = Point3d(1, 0, 0.8)
    p9 = Point3d(3, 0, 0.8)
    p10 = Point3d(3, 0, 2.4)
    p11 = Point3d(1, 0, 2.4)

    outer_wall_hole_loop = Loop([p8, p11, p10, p9])
    outer_wall_loop = Loop([p4, p7, p6, p5])
    outer_wall_face = Face(outer_wall_loop, [outer_wall_hole_loop])

    outer_wall_with_opening = Wall(outer_wall_face.outer_loop, outer_wall_face.inner_loops)

class TestZone(unittest.TestCase):
    def test_zone_with_extrude(self):
        # Arrange
        mesh = Mesh()

        # Act
        walls = Setup.zone.create_solid_faces()
        mesh.add_from_faces(walls)
        mesh.to_stl("", "test_zone_with_extrude")

    def test_zone_with_hole_extrude(self):
        # Arrange
        mesh = Mesh()

        # Act
        Setup.zone.walls[3].add_opening(Setup.outer_wall_hole_loop)
        walls = Setup.zone.create_solid_faces()
        mesh.add_from_faces(walls)
        mesh.to_stl("", "test_zone_with_hole_extrude")
