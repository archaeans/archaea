import numpy as np
from archaea.geometry.point3d import Point3d
from archaea.geometry.plane import Plane


class BoundingBox:
    min: Point3d
    max: Point3d
    center: Point3d
    plane: Plane
    area: float
    volume: float
    x_dist: float
    y_dist: float
    z_dist: float

    def __init__(self, minX: float, minY: float, minZ: float, maxX: float, maxY: float, maxZ: float, plane: Plane = Plane.xyz()) -> None:
        self.min = Point3d(minX, minY, minZ)
        self.max = Point3d(maxX, maxY, maxZ)
        self.plane = plane
        self.__calculate_values()

    @classmethod
    def from_points(cls, points: "list[Point3d]", plane: Plane = Plane.xyz()):
        x_values = [p.x for p in points]
        y_values = [p.y for p in points]
        z_values = [p.z for p in points]
        min_x = min(x_values)
        min_y = min(y_values)
        min_z = min(z_values)
        max_x = max(x_values)
        max_y = max(y_values)
        max_z = max(z_values)
        return cls(min_x, min_y, min_z, max_x, max_y, max_z, plane)
    
    @classmethod
    def from_points_in_plane(cls, points: "list[Point3d]", plane: Plane):
        # Transform the points to the new coordinate system
        transformed_points = []
        
        for point in points:
            p = plane.plane_coordinates(point)
            transformed_points.append(Point3d(p[0], p[1], point.z))

        # Find the bounding box in the new coordinate system
        x_values = [p.x for p in transformed_points]
        y_values = [p.y for p in transformed_points]
        z_values = [p.z for p in transformed_points]
        min_x = min(x_values)
        min_y = min(y_values)
        min_z = min(z_values)
        max_x = max(x_values)
        max_y = max(y_values)
        max_z = max(z_values)

        # return cls(min_point.x, min_point.y, min_point.z, max_point.x, max_point.y, max_point.z, plane)
        return cls(min_x, min_y, min_z, max_x, max_y, max_z, plane)
    
    @classmethod
    def from_2_points(cls, p1: Point3d, p2: Point3d, plane: Plane):
        return cls.from_points([p1, p2], plane)

    def __calculate_values(self):
        self.center = Point3d(
            (self.max.x + self.min.x) / 2,
            (self.max.y + self.min.y) / 2,
            (self.max.z + self.min.z) / 2
        )
        self.x_dist = abs(self.max.x - self.min.x)
        self.y_dist = abs(self.max.y - self.min.y)
        self.z_dist = abs(self.max.z - self.min.z)
        self.volume = self.x_dist * self.y_dist * self.z_dist
        self.area = 2 * ((self.x_dist * self.y_dist) + (self.x_dist * self.z_dist) + (self.y_dist * self.z_dist))
