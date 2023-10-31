import unittest
from archaea.geometry.vector import Vector
from archaea.geometry.vector3d import Vector3d


class Setup(unittest.TestLoader):
    vector3d_1 = Vector3d(0, 1, 2)
    vector3d_2 = Vector3d(1, -1, 4)
    vector3d_3 = Vector3d(1, 1, 2)


class TestVector3d(unittest.TestCase):
    def test_add_operator(self):
        # Act
        summed_vector: Vector3d = Setup.vector3d_1 + Setup.vector3d_2

        # Assert
        self.assertEqual(summed_vector.coordinates, [1, 0, 6])

    def test_subtract_operator(self):
        # Act
        subtracted_vector: Vector3d = Setup.vector3d_1 - Setup.vector3d_2

        # Assert
        self.assertEqual(subtracted_vector.coordinates, [-1, 2, -2])

    def test_add_class_method(self):
        # Act
        summed_vector: Vector3d = Vector3d.add(Setup.vector3d_1, Setup.vector3d_2)

        # Assert
        self.assertEqual(summed_vector.coordinates, [1, 0, 6])

    def test_dimension(self):
        # Assert
        self.assertEqual(Setup.vector3d_3.dimension, 3)

    def test_azimuth_angle(self):
        # Assert
        self.assertEqual(Setup.vector3d_3.azimuth_angle(), 45)

    def test_from_azimuth_45(self):
        # Act
        vector = Vector3d.from_azimuth_angle(45)

        # Assert
        self.assertAlmostEqual(vector.x, 2 ** 0.5 / -2, delta=10e-5)
        self.assertAlmostEqual(vector.y, 2 ** 0.5 / -2, delta=10e-5)

    def test_from_azimuth_90(self):
        # Act
        vector = Vector3d.from_azimuth_angle(90)

        # Assert
        self.assertAlmostEqual(vector.x, -1, delta=10e-5)
        self.assertAlmostEqual(vector.y, 0, delta=10e-5)
    
    def test_from_azimuth_135(self):
        # Act
        vector = Vector3d.from_azimuth_angle(135)

        # Assert
        self.assertAlmostEqual(vector.x, 2 ** 0.5 / -2, delta=10e-5)
        self.assertAlmostEqual(vector.y, 2 ** 0.5 / 2, delta=10e-5)
        


if __name__ == '__main__':
    unittest.main()
