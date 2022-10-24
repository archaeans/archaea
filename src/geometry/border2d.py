from .point2d import Point2d
from .vector3d import Vector3d


class Border2d:
    points: "list[Point2d]"
    normal: Vector3d

    def __init__(self, points: "list[Point2d]"):
        self.points = self.close_loop(points)
        self.normal = Vector3d(0, 0, 1)

    @staticmethod
    def close_loop(points: "list[Point2d]") -> "list[Point2d]":
        if points[-1] != points[0]:
            points.append(points[-1])
            return points
        else:
            return points
