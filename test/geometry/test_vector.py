import unittest
from archaea.geometry.vector import Vector
from archaea.geometry.vector3d import Vector3d


class Setup(unittest.TestLoader):
    vector_1 = Vector(0, 1, 2)
    vector_2 = Vector(1, -1, 4)
    vector_3 = Vector(1, -1, 2.0, 4, "a")
    vector_4_3d = Vector3d(1, 1, 2)


class VectorAdditionTest(unittest.TestCase):
    def test_add_operator(self):
        # Act
        summed_vector: Vector = Setup.vector_1 + Setup.vector_2

        # Assert
        self.assertEqual(summed_vector.coordinates, [1, 0, 6])

    def test_subtract_operator(self):
        # Act
        subtracted_vector: Vector = Setup.vector_1 - Setup.vector_2

        # Assert
        self.assertEqual(subtracted_vector.coordinates, [-1, 2, -2])

    def test_add_class_method(self):
        # Act
        summed_vector: Vector = Vector.add(Setup.vector_1, Setup.vector_2)

        # Assert
        self.assertEqual(summed_vector.coordinates, [1, 0, 6])

    def test_dimension(self):
        # Assert
        self.assertEqual(Setup.vector_3.dimension, 4)

    def test_azimuth_angle(self):
        # Assert
        self.assertEqual(Setup.vector_4_3d.azimuth_angle(), 45)


if __name__ == '__main__':
    unittest.main()
