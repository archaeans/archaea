import unittest
from src.geometry.point3d import Point3d
from src.geometry.point2d import Point2d
from src.geometry.vector3d import Vector3d
from src.geometry.loop import Loop


class Setup(unittest.TestLoader):
    p1 = Point3d(0, 0, 0)
    p2 = Point3d(10, 0, 0)
    p3 = Point3d(10, 10, 0)
    p4 = Point3d(0, 10, 0)
    loop_triangle = Loop([p1, p2, p3])
    loop_rectangle = Loop([p1, p2, p3, p4])


class TestLoop(unittest.TestCase):
    def test_close_loop(self):
        # Assert
        self.assertEqual(len(Setup.loop_triangle.points), 4)

    def test_calculate_normal(self):
        # Assert
        self.assertEqual(Setup.loop_triangle.normal, Vector3d(0, 0, 1))

    def test_points(self):
        # Assert
        self.assertEqual(len(Setup.loop_rectangle.points), 5)

    def test_segments(self):
        # Act
        segments = Setup.loop_rectangle.segments

        self.assertTrue(True)

    def test_segment_count(self):
        # Assert
        self.assertEqual(Setup.loop_triangle.segment_count, 3)

    def test_extrude(self):
        # Act
        faces = Setup.loop_rectangle.extrude(5)
        faces_area = sum(face.area for face in faces)

        # Assert
        self.assertEqual(len(faces), 6)
        self.assertEqual(faces_area, 400)

    def test_is_point_in_loop(self):
        # Arrange
        # FIXME: Need collinear check
        point_out_collinear = Point3d(-1, 0, 0)
        point_out = Point3d(-1, 2, 0)
        point_on = Point3d(2, 0, 0)
        point_in = Point3d(2, 2, 0)

        # Act
        point_out_collinear_should_false = Setup.loop_rectangle.is_point_in_loop(point_out_collinear)
        point_out_should_false = Setup.loop_rectangle.is_point_in_loop(point_out)
        point_on_should_true = Setup.loop_rectangle.is_point_in_loop(point_on)
        point_in_should_true = Setup.loop_rectangle.is_point_in_loop(point_in)

        # Assert
        self.assertFalse(point_out_collinear_should_false)
        self.assertFalse(point_out_should_false)
        self.assertTrue(point_on_should_true)
        self.assertTrue(point_in_should_true)

    def test_uv_points(self):
        # Act
        uv_points = Setup.loop_rectangle.uv_points()

        # Assert
        self.assertEqual(len(Setup.loop_rectangle.points), 5)
        self.assertEqual(len(uv_points), 4)

        self.assertEqual(uv_points[0], Point2d(0, 0))
        self.assertEqual(uv_points[1], Point2d(10, 0))
        self.assertEqual(uv_points[2], Point2d(10, -10))
        self.assertEqual(uv_points[3], Point2d(0, -10))

        self.assertEqual(Setup.p1, Setup.loop_rectangle.point_from_uv(uv_points[0]))
        self.assertEqual(Setup.p2, Setup.loop_rectangle.point_from_uv(uv_points[1]))
        self.assertEqual(Setup.p3, Setup.loop_rectangle.point_from_uv(uv_points[2]))
        self.assertEqual(Setup.p4, Setup.loop_rectangle.point_from_uv(uv_points[3]))


if __name__ == '__main__':
    unittest.main()
