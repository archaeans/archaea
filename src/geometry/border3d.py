from .point3d import Point3d
from .vector3d import Vector3d


class Border3d:
    points: "list[Point3d]"
    normal: Vector3d

    def __init__(self, points: "list[Point3d]"):
        self.points = self.close_loop(points)
        self.normal = self.calculate_normal(self.points)

    @staticmethod
    def close_loop(points: "list[Point3d]") -> "list[Point3d]":
        if points[-1] != points[0]:
            points.append(points[-1])
            return points
        else:
            return points

    @staticmethod
    def calculate_normal(points: "list[Point3d]") -> Vector3d:
        v1: Vector3d = points[0].vector_to(points[1])
        v2: Vector3d = points[0].vector_to(points[2])
        return v1.cross_product(v2).normalize()
