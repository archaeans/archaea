import unittest
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.loop import Loop
from src.geometry.face import Face
from src.geometry.mesh import Mesh


class Setup(unittest.TestLoader):
    # outer loop
    p0 = Point3d(0, 0, 0)
    p1 = Point3d(10, 0, 0)
    p2 = Point3d(10, 10, 0)
    p3 = Point3d(0, 10, 0)

    # inner loop - 1
    p4 = Point3d(2, 2, 0)
    p5 = Point3d(4, 2, 0)
    p6 = Point3d(4, 4, 0)
    p7 = Point3d(2, 4, 0)

    # inner loop - 2
    p8 = Point3d(5, 5, 0)
    p9 = Point3d(7, 5, 0)
    p10 = Point3d(7, 7, 0)
    p11 = Point3d(5, 7, 0)

    # loops
    outer_loop = Loop([p0, p1, p2, p3])
    inner_loop_1 = Loop([p4, p5, p6, p7])
    inner_loop_2 = Loop([p8, p9, p10, p11])

    # faces
    face_rectangle = Face(Loop([p0, p1, p2, p3]))
    face_rectangle_with_holes = Face(outer_loop, [inner_loop_1, inner_loop_2])
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
        self.assertEqual(mesh.polygons, [[0, 1, 2], [0, 2, 3]])

    def test_multiple_polygon_to_stl(self):
        # Arrange
        mesh = Mesh()
        mesh.add_polygon(Setup.face_triangle_1.outer_loop.points[:-1])
        mesh.add_polygon(Setup.face_triangle_2.outer_loop.points[:-1])

        # Act
        mesh.to_stl("", "test")

    def test_extruded_faces_to_stl(self):
        # Arrange
        mesh = Mesh()
        extruded_faces = Setup.face_rectangle.extrude(3)

        # Act
        mesh.add_from_faces(extruded_faces)
        mesh.to_stl("", "test_box")

    def test_face_with_holes(self):
        # Arrange
        mesh = Mesh()

        # Act
        mesh.add_from_face(Setup.face_rectangle_with_holes)
        mesh.to_stl("", "test_face_with_hole")

    def test_extruded_face_with_holes(self):
        # Arrange
        mesh = Mesh()
        extruded_faces = Setup.face_rectangle_with_holes.extrude(3)

        # Act
        mesh.add_from_faces(extruded_faces)
        mesh.to_stl("", "test_extruded_face_with_hole")

    def test_vertical_face(self):
        # Arrange
        mesh = Mesh()
        p0 = Point3d(0, 0, 0)
        p1 = Point3d(10, 0, 0)
        p2 = Point3d(10, 0, 10)
        p3 = Point3d(0, 0, 10)
        vertical_face = Face(Loop([p0, p1, p2, p3]))

        # Act
        mesh.add_from_face(vertical_face)
        mesh.to_stl("", "test_vertical_face")

    def test_horizontal_face(self):
        # Arrange
        mesh = Mesh()

        # Act
        mesh.add_from_face(Setup.face_rectangle)
        mesh.to_stl("", "test_horizontal_face")

