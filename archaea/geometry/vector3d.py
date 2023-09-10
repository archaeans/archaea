import math

from archaea.geometry.coordinate_array import CoordinateArray
from archaea.geometry.vector import Vector


# 3 dimensional vector.
class Vector3d(Vector):
    def __init__(self, *coordinates):
        filtered_coordinates = [entry for entry in coordinates if isinstance(entry, (int, float))]
        self.coordinates = filtered_coordinates[:3]
        super(CoordinateArray, self).__init__(filtered_coordinates)

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    @property
    def z(self):
        return self.coordinates[2]

    @property
    def length(self):
        return ((self.x ** 2) + (self.y ** 2) + (self.z ** 2)) ** 0.5

    def cross_product(self, other):
        return Vector3d(
            (self.y * other.z) - (self.z * other.y),
            (self.z * other.x) - (self.x * other.z),
            (self.x * other.y) - (self.y * other.x)
        )

    def azimuth_angle(self):
        result = 0
        if self.x > 0:
            result = (math.pi * 0.5) - math.atan(self.y / self.x)
        elif self.x < 0:
            result = (math.pi * 1.5) - math.atan(self.y / self.x)
        elif self.y > 0:
            result = 0
        elif self.y < 0:
            result = math.pi

        return math.degrees(result)

    def normalized(self):
        length = self.length
        if length == 0:
            return Vector3d(0, 0, 0)
        return Vector3d(self.x / length, self.y / length, self.z / length)

    def rotate(self, axis, angle, origin_point):
        # Calculate the vector from the origin to the point
        vector_to_point = self - origin_point.position_vector

        # Perform the rotation
        rotated_vector = vector_to_point.rotate(axis, angle)

        # Calculate the final position after rotation
        rotated_point = origin_point.position_vector + rotated_vector

        return Vector3d(rotated_point.x, rotated_point.y, rotated_point.z)

