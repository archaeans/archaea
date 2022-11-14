import unittest
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.border import Border
from src.simulation_objects.wall import Wall


class Setup(unittest.TestLoader):
    p1 = Point3d(0, 0, 0)
    p2 = Point3d(5, 0, 0)
    p3 = Point3d(5, 0, 5)
    p4 = Point3d(0, 0, 5)

    p5 = Point3d(1.5, 0, 0.9)
    p6 = Point3d(3, 0, 0.9)
    p7 = Point3d(3, 0, 2.4)
    p8 = Point3d(1.5, 0, 2.4)

    wall_border = Border([p1, p2, p3, p4])
    window_border = Border([p8, p7, p6, p5])
    wall = Wall(wall_border, [window_border])


class TestLoop3d(unittest.TestCase):
    def test_close_loop(self):
        # Assert
        self.assertEqual(len(Setup.wall_border.points), 5)

    def test_calculate_normal(self):
        # Assert
        self.assertEqual(Setup.wall_border.normal, Vector3d(0, -1, 0))

    # FIXME: z axis does not work with area calculation
    # def test_opening_area(self):
    #     # Assert
    #     self.assertEqual(Setup.wall.openings[0].area, 2.25)


if __name__ == '__main__':
    unittest.main()
