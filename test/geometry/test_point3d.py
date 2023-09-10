import unittest
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d


class Setup(unittest.TestLoader):
    point3d_origin = Point3d.origin()
    point3d_1 = Point3d(0, 1, 0)
    point3d_2 = Point3d(0, -1, 0)


class TestPoint3d(unittest.TestCase):
    def test_origin(self):
        # Assert
        self.assertEqual(Setup.point3d_origin.x, 0)
        self.assertEqual(Setup.point3d_origin.y, 0)
        self.assertEqual(Setup.point3d_origin.z, 0)

    def test_distance_to(self):
        # Act
        distance = Setup.point3d_1.distance_to(Setup.point3d_2)

        # Assert
        self.assertEqual(distance, 2)

    def test_rotate(self):
        # Act
        rotated_point = Setup.point3d_1.rotate(Vector3d(0, 0, 1), 90, Setup.point3d_2)

        # Assert
        self.assertAlmostEqual(rotated_point.x, 2,  delta=1e05)
        self.assertAlmostEqual(rotated_point.y, -1, delta=1e05)
