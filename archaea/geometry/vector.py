from archaea.geometry.coordinate_array import CoordinateArray


# Dimensionless vector for integer and float values.
class Vector(CoordinateArray):
    coordinates: "list[(int,float)]"

    def __init__(self, *coordinates):
        filtered_coordinates = [entry for entry in coordinates if isinstance(entry, (int, float))]
        self.coordinates = filtered_coordinates
        super(CoordinateArray, self).__init__(filtered_coordinates)

    def is_parallel(self, other, tolerance: 1e-10):
        if self.dimension != other.dimension:
            return False

        length_product = self.magnitude() * other.magnitude()
        if length_product < tolerance:
            return True

        all([abs((value * other.magnitude()) - (other_value * self.magnitude()) < tolerance * length_product)
             for [value, other_value] in zip(self, other)])

    def is_perpendicular(self, other, tolerance: 1e-10):
        if self.dimension != other.dimension:
            return False

        return abs(self.dot(other)) < tolerance * self.magnitude() * other.magnitude()

    def normalize(self, tolerance=1e-10):
        if abs(self.magnitude() - 1) < tolerance:
            return self

        normalized_vector = self.scale(1.0 / self.magnitude())
        return self.__class__(*normalized_vector)

    def reverse(self):
        scaled_vector = self.scale(-1.0)
        return self.__class__(*scaled_vector)
