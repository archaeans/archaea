import unittest
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.border import Border


class Setup(unittest.TestLoader):
    p1 = Point3d(0, 0, 0)
    p2 = Point3d(10, 0, 0)
    p3 = Point3d(10, 10, 0)

    border = Border([p1, p2, p3])


class TestLoop3d(unittest.TestCase):
    def test_close_loop(self):
        # Act
        border = Border([Setup.p1, Setup.p2, Setup.p3])

        # Assert
        self.assertEqual(len(border.points), 4)

    def test_calculate_normal(self):
        # Assert
        self.assertEqual(Setup.border.normal, Vector3d(0, 0, 1))


if __name__ == '__main__':
    unittest.main()
