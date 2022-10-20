import unittest
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.border3d import Border3d


class Setup(unittest.TestLoader):
    p1 = Point3d(0, 0, 0)
    p2 = Point3d(10, 0, 0)
    p3 = Point3d(10, 10, 0)

    border = Border3d([p1, p2, p3])


class TestLoop3d(unittest.TestCase):
    def test_close_loop(self):
        # Act
        points = Border3d.close_loop([Setup.p1, Setup.p2, Setup.p3])

        # Assert
        self.assertEqual(len(points), 4)

    def test_calculate_normal(self):
        # Assert
        self.assertEqual(Setup.border.normal, Vector3d(0, 0, 1))
