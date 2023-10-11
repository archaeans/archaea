import unittest
from archaea.geometry.bounding_box import BoundingBox
from archaea.geometry.point3d import Point3d


class Setup(unittest.TestLoader):
    p1 = Point3d(7, 0, 0)
    p2 = Point3d(-2, 2, 3)
    p3 = Point3d(5, 5, -5)

    bbox_from_2_points = BoundingBox.from_2_points(p1, p2)
    bbox_from_points = BoundingBox.from_points([p1, p2, p3])

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