from archaea.geometry.coordinate_array import CoordinateArray
from archaea.geometry.vector2d import Vector2d


# 2 dimensional point.
class Point2d(CoordinateArray):
    def __init__(self, *coordinates):
        filtered_coordinates = [entry for entry in coordinates if isinstance(entry, (int, float))]
        self.coordinates = filtered_coordinates[:2]
        super(CoordinateArray, self).__init__(filtered_coordinates)

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    def position_vector(self):
        return Vector2d(self.x, self.y)

    def move(self, vector):
        return Point2d(self.x + vector.x, self.y + vector.y)

    def vector_to(self, other):
        return Vector2d(other.x - self.x, other.y - self.y)

    def distance_to(self, other):
        return (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** 0.5
