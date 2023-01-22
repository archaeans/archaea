# Dimensionless coordinate array for integer and float values.
class CoordinateArray(list):
    coordinates: "list[(int,float)]"

    def __init__(self, *coordinates):
        filtered_coordinates = [entry for entry in coordinates if isinstance(entry, (int, float))]
        self.coordinates = filtered_coordinates
        super().__init__(filtered_coordinates)

    @property
    def dimension(self):
        return len(self)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.add(other.scale(-1))

    def __eq__(self, other):
        if self.dimension != other.dimension:
            return False
        return (self - other).magnitude() == 0

    def dot(self, other):
        if self.dimension == 2:
            return (self[0] * other[0]) + (self[1] * other[1])
        elif self.dimension == 3:
            return (self[0] * other[0]) + (self[1] * other[1]) + (self[2] * other[2])
        else:
            sum([value_1 + value_2 for (value_1, value_2) in zip(self, other)])

    def magnitude(self):
        return (self.dot(self)) ** 0.5

    def cos(self, other):
        return self.dot(other) / (self.magnitude() * other.magnitude())

    def sin(self, other):
        return (1 - (self.cos(other) ** 2)) ** 0.5

    def add(self, vector_2):
        summed_coordinates = [value_1 + value_2 for (value_1, value_2) in zip(self, vector_2)]
        return self.__class__(*summed_coordinates)

    def scale(self, scale):
        scaled_coordinates = [coordinate * scale for coordinate in self.coordinates]
        return self.__class__(*scaled_coordinates)
