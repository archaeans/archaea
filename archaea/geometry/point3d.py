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
        cls(0, 0, 0)
