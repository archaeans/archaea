import functools
import numpy as np
import math

from archaea.geometry.vector3d import Vector3d
from archaea.geometry.point3d import Point3d


class Plane:
    u: Vector3d
    v: Vector3d
    origin: Point3d

    def __init__(self, origin: Point3d, u: Vector3d, v: Vector3d):
        if u.dot(v) > 1e-5:
            raise 'u-v should be orthogonal'
        self.u = u
        self.v = v
        self.origin = origin

    def xyz():
        return Plane(Point3d.origin, Vector3d(1, 0, 0), Vector3d(0, 1, 0))

    @functools.cached_property
    def normal(self):
        return self.u.cross_product(self.v).normalize()

    @classmethod
    def from_3_point(cls, origin_point: Point3d, point_2: Point3d, point_3: Point3d):
        u_direction = origin_point.vector_to(point_2).normalize()
        normal = u_direction.cross_product(origin_point.vector_to(point_3))
        v_direction = u_direction.cross_product(normal.normalize())
        return cls(origin_point, u_direction, v_direction)
    
    @classmethod
    def get_xy_plane_for_angle(cls, origin_point: Point3d, angle: float):
        wind_direction_rad = math.radians(angle)

        # Calculate the velocity components Ux and Uy
        v_x = -math.sin(wind_direction_rad)
        v_y = -math.cos(wind_direction_rad)

        v = Vector3d(v_x, v_y, 0)
        u = v.cross_product(Vector3d(0, 0, 1))
        return cls(origin_point, u, v)

    def point_at(self, u, v):
        return self.origin.move(self.u.scale(u) + self.v.scale(v))

    def plane_coordinates(self, point):
        origin_to_point = self.origin.vector_to(point)
        coordinate_u = origin_to_point.dot(self.u)
        coordinate_v = origin_to_point.dot(self.v)
        return [coordinate_u, coordinate_v]

    def project_to_plane(self, point):
        plane_coordinates = self.plane_coordinates(point)
        return self.point_at(plane_coordinates[0], plane_coordinates[1])

    def project_to_plane_on_z(self, point):
        d = self.normal.dot(self.origin.position_vector)
        z_value_on_plane = (d - (self.normal.x * point.x) - (self.normal.y * point.y)) / self.normal.z
        return Point3d(point.x, point.y, z_value_on_plane)

    def is_on_plane(self, point):
        return point.distance_to(self.project_to_plane(point)) < 1e-5

    def is_same_plane(self, other):
        return (self.is_on_plane(other.origin)) and self.is_on_plane(other.point_at(1, 0) and
                                                                     self.is_on_plane(other.point_at(0, 1)))

    def rotate(self, axis, angle, origin_point=None):
        if origin_point is None:
            origin_point = self.origin

        # Perform the rotation on the origin
        rotated_origin = origin_point.rotate(axis, angle)
        rotated_u = self.u.rotate(axis, angle)
        rotated_v = self.v.rotate(axis, angle)

        return Plane(rotated_origin, rotated_u, rotated_v)

    def get_rotation_matrix(self):
        # Create a rotation matrix that aligns the plane with the standard xyz plane
        return np.column_stack((self.u, self.v, self.normal))
