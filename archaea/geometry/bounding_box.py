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
        # Extract the rotation matrix from the new plane
        rotation_matrix = plane.get_rotation_matrix()

        # Transform the points to the new coordinate system
        transformed_points = [point.rotate_with_matrix(rotation_matrix) for point in points]

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

        # Define the inverse rotation matrix to transform back to the standard XYZ plane
        inverse_rotation_matrix = np.linalg.inv(rotation_matrix)

        # Apply the inverse rotation to find min and max aligned with the standard XYZ plane
        min_point = Point3d(min_x, min_y, min_z).rotate_with_matrix(inverse_rotation_matrix)
        max_point = Point3d(max_x, max_y, max_z).rotate_with_matrix(inverse_rotation_matrix)

        return cls(min_point.x, min_point.y, min_point.z, max_point.x, max_point.y, max_point.z, plane)
    
    @classmethod
    def from_2_points(cls, p1: Point3d, p2: Point3d, plane: Plane):
        return cls.from_points([p1, p2], plane)

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
