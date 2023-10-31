import unittest
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d
from archaea.geometry.plane import Plane

class TestPlane(unittest.TestCase):
    def test_get_xy_plane_for_angle(self):
        # Arrange
        angle = 45.0

        # Act
        plane = Plane.get_xy_plane_for_angle(origin_point=Point3d.origin(), angle=angle)

        # Assert
        self.assertEqual(plane.normal, Vector3d(0, 0, 1))