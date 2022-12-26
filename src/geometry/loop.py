import functools
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.line_segment import LineSegment
from src.geometry.polyline import Polyline
from src.geometry.plane import Plane
from src.geometry.utils import area


class Loop:
    points: "list[Point3d]"
    normal: Vector3d

    def __init__(self, points: "list[Point3d]"):
        if points[-1] != points[0]:
            points.append(points[0])
        self.points = points
        self.normal = self._calculate_normal(self.points)

    @functools.cached_property
    def segments(self):
        consecutive_pairs = [[self.points[i], self.points[i + 1]]
                             for i in range(len(self.points) - 1)]
        return [LineSegment(start, end) for [start, end] in consecutive_pairs]

    @functools.cached_property
    def area(self):
        poly = [point.to_a() for point in self.points]
        return area(poly)

    @functools.cached_property
    def segment_count(self):
        return len(self.segments)

    def plane(self):
        u: Vector3d = self.points[0].vector_to(self.points[1])
        v: Vector3d = self.points[0].vector_to(self.points[2])
        return Plane(self.points[0], u, v)

    def to_polyline(self):
        return Polyline(self.segments)

    def to_face(self):
        from src.geometry.face import Face
        return Face(self)

    def move(self, vector):
        moved_points = []
        for point in self.points:
            moved_points.append(point.move(vector))
        return Loop(moved_points)

    def extrude(self, value):
        faces = [self.to_face()]
        move_vector = Vector3d(*self.normal.scale(value))
        for line in self.segments:
            border = line.extrude(move_vector)
            faces.append(border)
        cap = self.move(move_vector)
        faces.append(cap.to_face())
        return faces

    @staticmethod
    def _calculate_normal(points: "list[Point3d]") -> Vector3d:
        """
        Method that calculates normal from first point and vectors with second and third point.
        :param: points to calculate normal
        :returns normal as vector
        """
        v1: Vector3d = points[0].vector_to(points[1])
        v2: Vector3d = points[0].vector_to(points[2])
        return v1.cross_product(v2).normalize()
