from src.geometry.vector3d import Vector3d
from src.geometry.point3d import Point3d


class Plane:
    u: Vector3d
    v: Vector3d
    origin: Point3d

    def __init__(self, origin, u, v):
        if u.dot(v) > 1e-5:
            raise 'u-v should be orthogonal'
        self.u = u
        self.v = v
        self.origin = origin

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

    def is_on_plane(self, point):
        return point.distance_to(self.project_to_plane(point)) < 1e-5

    def is_same_plane(self, other):
        return (self.is_on_plane(other.origin)) and self.is_on_plane(other.point_at(1, 0) and
                                                                     self.is_on_plane(other.point_at(0, 1)))
