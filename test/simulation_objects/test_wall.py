import unittest
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.face import Face
from src.simulation_objects.wall import Wall
from src.simulation_objects.wall_type import WallType


class Setup(unittest.TestLoader):
    p1 = Point3d(0, 0, 0)
    p2 = Point3d(5, 0, 0)
    p3 = Point3d(5, 0, 3)
    p4 = Point3d(0, 0, 3)

    p5 = Point3d(1.5, 0, 0.9)
    p6 = Point3d(3, 0, 0.9)
    p7 = Point3d(3, 0, 2.4)
    p8 = Point3d(1.5, 0, 2.4)

    wall_border = Face([p1, p2, p3, p4])
    window_border = Face([p8, p7, p6, p5])
    wall = Wall([p1, p2, p3, p4], [window_border], WallType.OUTER)


class TestLoop3d(unittest.TestCase):
    def test_close_loop(self):
        # Assert
        self.assertEqual(len(Setup.wall_border.points), 5)

    def test_calculate_normal(self):
        # Assert
        self.assertEqual(Setup.wall_border.normal, Vector3d(0, -1, 0))

    def test_wall_area(self):
        # Assert
        self.assertEqual(Setup.wall.area, 15)

    def test_opening_area(self):
        # Assert
        self.assertEqual(Setup.wall.openings[0].area, 2.25)


if __name__ == '__main__':
    unittest.main()
