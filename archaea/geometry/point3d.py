import math
from archaea.geometry.coordinate_array import CoordinateArray
from archaea.geometry.vector3d import Vector3d


# 3 dimensional point.
class Point3d(CoordinateArray):
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

    def __sub__(self, other):
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, vector):
        return Point3d(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def to_a(self):
        return [self.x, self.y, self.z]

    @property
    def position_vector(self):
        return Vector3d(self.x, self.y, self.z)

    def move(self, vector):
        return Point3d(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def vector_to(self, other):
        return Vector3d(other.x - self.x, other.y - self.y, other.z - self.z)

    def distance_to(self, other):
        return (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2) + ((self.z - other.z) ** 2)) ** 0.5

    @classmethod
    def origin(cls):
        return cls(0, 0, 0)

    def rotate(self, axis, angle, origin=None):
        if origin is None:
            origin = Point3d(0, 0, 0)

        # Translate the point to the origin
        translated_point = self - origin

        # Create a rotation matrix
        axis = axis.normalized()
        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))
        t = 1 - c

        rotation_matrix = [
            [t * axis.x ** 2 + c, t * axis.x * axis.y - s * axis.z, t * axis.x * axis.z + s * axis.y],
            [t * axis.x * axis.y + s * axis.z, t * axis.y ** 2 + c, t * axis.y * axis.z - s * axis.x],
            [t * axis.x * axis.z - s * axis.y, t * axis.y * axis.z + s * axis.x, t * axis.z ** 2 + c]
        ]

        # Apply the rotation matrix to the translated point
        x_rotated = translated_point.x * rotation_matrix[0][0] + translated_point.y * rotation_matrix[1][
            0] + translated_point.z * rotation_matrix[2][0]
        y_rotated = translated_point.x * rotation_matrix[0][1] + translated_point.y * rotation_matrix[1][
            1] + translated_point.z * rotation_matrix[2][1]
        z_rotated = translated_point.x * rotation_matrix[0][2] + translated_point.y * rotation_matrix[1][
            2] + translated_point.z * rotation_matrix[2][2]

        # Translate the rotated point back to its original position
        rotated_point = Point3d(x_rotated, y_rotated, z_rotated) + origin

        return rotated_point
