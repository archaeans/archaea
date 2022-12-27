import unittest
from src.geometry.point3d import Point3d
from src.geometry.line_segment import LineSegment


class Setup(unittest.TestLoader):
    point3d_1 = Point3d(0, 0, 0)
    point3d_2 = Point3d(5, 0, 0)
    point3d_on_line = Point3d(1, 0, 0)
    point3d_not_on_line = Point3d(2, 1, 0)
    line_segment = LineSegment(point3d_1, point3d_2)


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
