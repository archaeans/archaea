import functools
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.line_segment import LineSegment
from src.geometry.polyline import Polyline
from src.geometry.plane import Plane
import numpy as np


class Border:
    points: "list[Point3d]"
    normal: Vector3d

    def __init__(self, points: "list[Point3d]"):
        if points[-1] != points[0]:
            points.append(points[-1])
        self.points = points
        self.normal = self._calculate_normal(self.points)

    @functools.cached_property
    def segments(self):
        consecutive_pairs = [[self.points[i], self.points[i + 1]]
                             for i in range(len(self.points) - 1)]
        return [LineSegment(start, end) for [start, end] in consecutive_pairs]

    @functools.cached_property
    def area(self):
        x = []
        y = []
        z = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        return area

    @functools.cached_property
    def segment_count(self):
        return len(self.segments)

    def plane(self):
        u: Vector3d = self.points[0].vector_to(self.points[1])
        v: Vector3d = self.points[0].vector_to(self.points[2])
        return Plane(self.points[0], u, v)

    def to_polyline(self):
        return Polyline(self.segments)

    def move(self, vector):
        moved_points = []
        for point in self.points:
            moved_points.append(point.move(vector))
        return Border(moved_points)

    @staticmethod
    def _calculate_normal(points: "list[Point3d]") -> Vector3d:
        """
        Method that calculates normal from first point and vectors with second and third point.
        :param points to calculate normal
        :returns normal as vector
        """
        v1: Vector3d = points[0].vector_to(points[1])
        v2: Vector3d = points[0].vector_to(points[2])
        return v1.cross_product(v2).normalize()

