from archaea.geometry.point3d import Point3d


class BoundingBox:
    min: Point3d
    max: Point3d
    center: Point3d
    area: float
    volume: float

    def __init__(self, minX: float, minY: float, minZ: float, maxX: float, maxY: float, maxZ: float) -> None:
        self.min = Point3d(minX, minY, minZ)
        self.max = Point3d(maxX, maxY, maxZ)
        self.__calculate_values()

    @classmethod
    def from_points(cls, points: "list[Point3d]"):
        x_values = [p.x for p in points]
        y_values = [p.y for p in points]
        z_values = [p.z for p in points]
        min_x = min(x_values)
        min_y = min(y_values)
        min_z = min(z_values)
        max_x = max(x_values)
        max_y = max(y_values)
        max_z = max(z_values)
        return cls(min_x, min_y, min_z, max_x, max_y, max_z)
    
    @classmethod
    def from_2_points(cls, p1: Point3d, p2: Point3d):
        return cls.from_points([p1, p2])

    def __calculate_values(self):
        self.center = Point3d(
            (self.max.x + self.min.x) / 2,
            (self.max.y + self.min.y) / 2,
            (self.max.z + self.min.z) / 2
        )
        x_dist = abs(self.max.x - self.min.x)
        y_dist = abs(self.max.y - self.min.y)
        z_dist = abs(self.max.z - self.min.z)
        self.volume = x_dist * y_dist * z_dist
        self.area = 2 * ((x_dist * y_dist) + (x_dist * z_dist) + (y_dist * z_dist))
