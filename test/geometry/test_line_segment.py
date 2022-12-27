import unittest
from src.geometry.point3d import Point3d
from src.geometry.line_segment import LineSegment


class Setup(unittest.TestLoader):
    point3d_1 = Point3d(0, 0, 0)
    point3d_1_2 = Point3d(0, 0, 0)
    point3d_2 = Point3d(5, 0, 0)
    point3d_2_2 = Point3d(5, 0, 0)
    point3d_on_line = Point3d(1, 0, 0)
    point3d_not_on_line = Point3d(2, 1, 0)
    line_segment = LineSegment(point3d_1, point3d_2)
    line_segment_2 = LineSegment(point3d_1_2, point3d_2_2)


class TestLineSegment(unittest.TestCase):
    def test_length(self):
        # Assert
        self.assertEqual(Setup.line_segment.length, 5)

    def test_point_at(self):
        # Assert
        self.assertEqual(Setup.line_segment.point_at(0), Point3d(0, 0, 0))
        self.assertEqual(Setup.line_segment.point_at(1), Point3d(5, 0, 0))
        self.assertEqual(Setup.line_segment.point_at(0.5), Point3d(2.5, 0, 0))
        self.assertEqual(Setup.line_segment.point_at(1.5), Point3d(7.5, 0, 0))
        self.assertEqual(Setup.line_segment.point_at(-1.5), Point3d(-7.5, 0, 0))

    def test_on_line(self):
        # Assert
        self.assertTrue(Setup.line_segment.is_point_on_line(Setup.point3d_on_line))
        self.assertFalse(Setup.line_segment.is_point_on_line(Setup.point3d_not_on_line))

    def test_parameter_at(self):
        # Assert
        self.assertEqual(Setup.line_segment.parameter_at(Setup.point3d_on_line), 0.2)
        self.assertEqual(Setup.line_segment.parameter_at(Setup.point3d_not_on_line), 0.4)

    def test_closest_point(self):
        # Assert
        self.assertEqual(Setup.line_segment.closest_point(Setup.point3d_not_on_line), Point3d(2, 0, 0))

    def test_equilibrium(self):
        # Assert
        self.assertTrue(Setup.line_segment == Setup.line_segment_2)

    def test_distance_to_point(self):
        # Assert
        self.assertEqual(Setup.line_segment.distance_to_point(Setup.point3d_not_on_line), 1)

    def test_intersects_not_by_origin(self):
        # Arrange
        line_segment_1 = LineSegment(Point3d(1, 1, 1), Point3d(5, 5, 5))
        line_segment_2 = LineSegment(Point3d(4, 1, 1), Point3d(2, 5, 5))

        # Act
        is_intersects = line_segment_1.is_intersects(line_segment_2)

        # Assert
        self.assertTrue(is_intersects)

    def test_intersects_on_origin(self):
        # Arrange
        line_segment_on_x = LineSegment(Point3d(-1, 0, 0), Point3d(1, 0, 0))
        line_segment_on_y = LineSegment(Point3d(0, -1, 0), Point3d(0, 1, 0))
        line_segment_on_z = LineSegment(Point3d(0, 0, -1), Point3d(0, 0, 1))

        # Act
        is_intersects_on_xy = line_segment_on_x.is_intersects(line_segment_on_y)
        is_intersects_on_xz = line_segment_on_x.is_intersects(line_segment_on_z)
        is_intersects_on_yz = line_segment_on_y.is_intersects(line_segment_on_z)

        # Assert
        self.assertTrue(is_intersects_on_xy)
        self.assertTrue(is_intersects_on_xz)
        self.assertTrue(is_intersects_on_yz)

    def test_distance_to_segment(self):
        # Arrange
        line_segment_1 = LineSegment(Point3d(1, 0, 1), Point3d(5, 0, 1))
        line_segment_2 = LineSegment(Point3d(2, 0, 5), Point3d(4, 0, 3))

        # Act
        is_intersects = line_segment_1.is_intersects(line_segment_2)
        distance = line_segment_1.distance_to_segment(line_segment_2)

        # Assert
        self.assertFalse(is_intersects)
        self.assertEqual(distance, 2)
