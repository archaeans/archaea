import unittest
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d
from archaea.geometry.loop import Loop
from archaea.geometry.face import Face
from archaea.geometry.mesh import Mesh


class Setup(unittest.TestLoader):
    # outer loop
    p0 = Point3d(0, 0, 0)
    p1 = Point3d(10, 0, 0)
    p2 = Point3d(10, 10, 0)
    p3 = Point3d(0, 10, 0)

    clockwise_loop = Loop([p0, p3, p2, p1])
    clockwise_face = Face(clockwise_loop)
    counter_clockwise_loop = Loop([p0, p1, p2, p3])
    counter_clockwise_face = Face(counter_clockwise_loop)

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
        mesh.add_polygon(Setup.face_triangle_2.outer_loop.points[:-1])

        # Act
        mesh.to_stl("", "test")

    def test_rotated_multiple_polygon_to_stl(self):
        # Arrange
        mesh = Mesh()
        mesh.add_polygon(Setup.face_triangle_2.outer_loop.points[:-1])

        # Act
        mesh.rotate(Vector3d(0, 0, 1), 90, Point3d(1,0,0)).to_stl("", "test_rotated")

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

    def test_horizontal_extruded_face_with_holes(self):
        # Arrange
        mesh = Mesh()
        extruded_faces = Setup.face_rectangle_with_holes.extrude(3)

        # Act
        mesh.add_from_faces(extruded_faces)
        mesh.to_stl("", "test_horizontal_extruded_face_with_holes")

    def test_vertical_extruded_face_with_holes(self):
        # Arrange
        p0 = Point3d(0, 0, 0)
        p1 = Point3d(10, 0, 0)
        p2 = Point3d(10, 0, 10)
        p3 = Point3d(0, 0, 10)

        # inner loop - 1
        p4 = Point3d(2, 0, 2)
        p5 = Point3d(4, 0, 2)
        p6 = Point3d(4, 0, 4)
        p7 = Point3d(2, 0, 4)

        # inner loop - 2
        p8 = Point3d(5, 0, 0.2)
        p9 = Point3d(7, 0, 0.2)
        p10 = Point3d(7, 0, 7)
        p11 = Point3d(5, 0, 7)

        # loops
        outer_loop = Loop([p0, p1, p2, p3])
        inner_loop_1 = Loop([p4, p5, p6, p7])
        inner_loop_2 = Loop([p8, p9, p10, p11])

        # faces
        face_vertical_rectangle_with_holes = Face(outer_loop, [inner_loop_1, inner_loop_2])

        mesh = Mesh()
        extruded_faces = face_vertical_rectangle_with_holes.extrude(0.2)

        # Act
        mesh.add_from_faces(extruded_faces)
        mesh.to_stl("", "test_vertical_extruded_face_with_holes")

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

    def test_clockwise_extrude_face(self):
        # Arrange
        mesh = Mesh()
        extruded_faces = Setup.clockwise_face.extrude(3)

        # Act
        mesh.add_from_faces(extruded_faces)
        mesh.to_stl("", "test_clockwise_extrude_face")

    def test_counter_clockwise_extrude_face(self):
        # Arrange
        mesh = Mesh()
        extruded_faces = Setup.counter_clockwise_face.extrude(3)

        # Act
        mesh.add_from_faces(extruded_faces)
        mesh.to_stl("", "test_counter_clockwise_extrude_face")

    def test_offset_and_move_face_with_hole(self):
        # Arrange
        mesh = Mesh()
        offset_value = 0.5
        wall_thickness = -0.2

        # Act
        offset_face = Setup.face_rectangle_with_holes.offset(offset_value)
        moved_face = offset_face.move(offset_face.plane.normal.scale(wall_thickness))
        mesh.add_from_faces([Setup.face_rectangle_with_holes, moved_face])
        mesh.to_stl("", "test_offset_and_move_face_with_hole")

    def test_from_ngon_mesh(self):
        # Arrange
        flat_point_values = [0, 0, 0, 5, 0, 0, 0, 0, 5,
                             0, 0, 0, 5, 0, 0, 5, 5, 0, 0, 5, 0,
                             0, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, -2.5, 2.5, 5]
        ngon_mesh_indices = [3, 0, 1, 2, 
                             4, 3, 4, 5, 6,
                             5, 7, 8, 9, 10, 11]
        mesh = Mesh.from_ngon_mesh(flat_point_values, ngon_mesh_indices)

        # Act
        self.assertEqual(len(mesh.polygons), 6)
        self.assertEqual(len(mesh.vertices), 12)
        mesh.to_stl("", "test_from_ngon_mesh")


if __name__ == '__main__':
    unittest.main()
