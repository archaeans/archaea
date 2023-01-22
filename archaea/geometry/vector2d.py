from archaea.geometry.coordinate_array import CoordinateArray


# 2 dimensional vector.
class Vector2d(CoordinateArray):
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

    def outer_product(self, other):
        return (self.x * other.y) - (self.y * other.x)

