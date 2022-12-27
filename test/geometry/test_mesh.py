import unittest
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.loop import Loop
from src.geometry.face import Face
from src.geometry.mesh import Mesh


class Setup(unittest.TestLoader):
    p0 = Point3d(0, 0, 0)
    p1 = Point3d(10, 0, 0)
    p2 = Point3d(10, 10, 0)
    p3 = Point3d(0, 10, 0)
    face_rectangle = Face(Loop([p0, p1, p2, p3]))

    face_triangle_1 = Face(Loop([p0, p1, p2]))
    face_triangle_2 = Face(Loop([p0, p2, p3]))


class TestMesh(unittest.TestCase):
    def test_add_single_polygon(self):
        # Arrange
        mesh = Mesh()

        # Act
        mesh.add_polygon(Setup.face_triangle_1.outer_loop.points[:-1])

        # Assert
        self.assertEqual(len(mesh.vertices), 3)
        self.assertEqual(len(mesh.polygons), 1)
        self.assertEqual(mesh.polygons[0], [0, 1, 2])

    def test_add_multiple_polygon(self):
        # Arrange
        mesh = Mesh()

        # Act
        mesh.add_polygon(Setup.face_triangle_1.outer_loop.points[:-1])
        mesh.add_polygon(Setup.face_triangle_2.outer_loop.points[:-1])

        # Assert
        self.assertEqual(len(mesh.vertices), 4)
        self.assertEqual(len(mesh.polygons), 2)
        self.assertEqual(mesh.polygons, [[0, 1, 2], [1, 2, 3]])

    def test_multiple_polygon_to_stl(self):
        # Arrange
        mesh = Mesh()
        mesh.add_polygon(Setup.face_triangle_1.outer_loop.points[:-1])
        mesh.add_polygon(Setup.face_triangle_2.outer_loop.points[:-1])

        # Act
        mesh.to_stl("", "test")