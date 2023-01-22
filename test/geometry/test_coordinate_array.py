import unittest
from archaea.geometry.coordinate_array import CoordinateArray


class Setup(unittest.TestLoader):
    coordinate_array_1 = CoordinateArray(0, 1, 2)
    coordinate_array_2 = CoordinateArray(1, -1, 4)
    coordinate_array_3 = CoordinateArray(1, -1, 2.0, 4, "a")
    coordinate_array_4 = CoordinateArray(3, 4, 0)
    coordinate_array_5 = CoordinateArray(5, 12, 0)


class TestCoordinateArray(unittest.TestCase):
    def test_dimension(self):
        # Assert
        self.assertEqual(Setup.coordinate_array_1.dimension, 3)
        self.assertEqual(Setup.coordinate_array_2.dimension, 3)
        self.assertEqual(Setup.coordinate_array_3.dimension, 4)

    def test_dot(self):
        # Act
        dot_value = Setup.coordinate_array_1.dot(Setup.coordinate_array_2)

        # Assert
        self.assertEqual(dot_value, 7)

    def test_magnitude(self):
        # Act
        magnitude_4 = Setup.coordinate_array_4.magnitude()
        magnitude_5 = Setup.coordinate_array_5.magnitude()

        # Assert
        self.assertEqual(magnitude_4, 5)
        self.assertEqual(magnitude_5, 13)

    def test_cos(self):
        # Act
        cos_value = Setup.coordinate_array_1.cos(Setup.coordinate_array_2)

        # Assert
        self.assertAlmostEqual(cos_value, 0.73786479, delta=1e-5)

    def test_sin(self):
        # Act
        sin_value = Setup.coordinate_array_1.sin(Setup.coordinate_array_2)

        # Assert
        self.assertAlmostEqual(sin_value, 0.67494856, delta=1e-5)

    def test_add(self):
        # Act
        added_coordinate_arrays = Setup.coordinate_array_1 + Setup.coordinate_array_2

        # Assert
        self.assertEqual(added_coordinate_arrays.coordinates, [1, 0, 6])

    def test_scale(self):
        # Act
        scaled_coordinate_array = Setup.coordinate_array_1.scale(3)

        # Assert
        self.assertEqual(scaled_coordinate_array.coordinates, [0, 3, 6])


if __name__ == '__main__':
    unittest.main()
