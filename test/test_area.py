import unittest
from src.geometry.point3d import Point3d
from src.geometry.utils import area



class Setup(unittest.TestLoader):
    # outer loop
    p0 = Point3d(0, 0, 0)
    p1 = Point3d(10, 0, 0)
    p2 = Point3d(10, 10, 0)
    p3 = Point3d(0, 10, 0)

    clockwise = [p3.to_a(), p2.to_a(), p1.to_a(), p0.to_a()]
    counter_clockwise = [p0.to_a(), p1.to_a(), p2.to_a(), p3.to_a()]


class TestArea(unittest.TestCase):
    def test_clockwise(self):
        # Act
        calculated_area = area(Setup.clockwise)

        # Assert
        self.assertEqual(calculated_area, -100)

    def test_counter_clockwise(self):
        # Act
        calculated_area = area(Setup.counter_clockwise)

        # Assert
        self.assertEqual(calculated_area, 100)
