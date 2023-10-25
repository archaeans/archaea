import unittest
from archaea.geometry.bounding_box import BoundingBox
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d
from archaea.geometry.plane import Plane


class Setup(unittest.TestLoader):
    p1 = Point3d(7, 0, 0)
    p2 = Point3d(-2, 2, 3)
    p3 = Point3d(5, 5, -5)

    plane = Plane(Point3d.origin(), Vector3d(1, 0, 0), Vector3d(0, 1, 0))
    bbox_from_2_points = BoundingBox.from_2_points(p1, p2, plane)
    bbox_from_points = BoundingBox.from_points([p1, p2, p3], plane)
    
    p4 = Point3d(2, 2, 0)
    p5 = Point3d(3, 1, 0)
    p6 = Point3d(5, 5, 0)
    p7 = Point3d(6, 4, 0)
    bbox_from_points_in_plane = BoundingBox.from_points_in_plane(
        [p4, p5, p6, p7], 
        Plane(Point3d.origin(), Vector3d(1, 1, 0).normalized(), Vector3d(-1, 1, 0).normalized())
    )

class TestBoundingBox(unittest.TestCase):
    def test_from_2_points(self):
        # Assert
        self.assertEqual(Setup.bbox_from_2_points.min, Point3d(-2, 0, 0))
        self.assertEqual(Setup.bbox_from_2_points.max, Point3d(7, 2, 3))

    def test_from_points(self):
        # Assert
        self.assertEqual(Setup.bbox_from_points.min, Point3d(-2, 0, -5))
        self.assertEqual(Setup.bbox_from_points.max, Point3d(7, 5, 3))

    def test_center(self):
        # Assert
        self.assertEqual(Setup.bbox_from_2_points.center, Point3d(2.5, 1, 1.5))
        self.assertEqual(Setup.bbox_from_points.center, Point3d(2.5, 2.5, -1))

    def test_volume(self):
        # Assert
        self.assertEqual(Setup.bbox_from_2_points.volume, 54)
        self.assertEqual(Setup.bbox_from_points.volume, 360)

    def test_area(self):
        # Assert
        self.assertEqual(Setup.bbox_from_2_points.area, 102)
        self.assertEqual(Setup.bbox_from_points.area, 314)

    def test_from_points_in_plane(self):
        # Assert
        self.assertEqual(Setup.bbox_from_points_in_plane.min, Point3d(2, 2, 0))
        self.assertEqual(Setup.bbox_from_points_in_plane.max, Point3d(6, 4, 0))