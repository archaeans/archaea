import functools
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.line_segment import LineSegment
from src.geometry.polyline import Polyline
from src.geometry.plane import Plane
from src.geometry.utils import area


class Loop(Polyline):
    points: "list[Point3d]"
    normal: Vector3d

    def __init__(self, points: "list[Point3d]"):
        if points[-1] != points[0]:
            points.append(points[0])
        self.points = points
        super().__init__(self.points)
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
        return Plane.from_3_point(self.points[0], self.points[1], self.points[2])

    def to_face(self):
        from src.geometry.face import Face
        return Face(self)

    def move(self, vector):
        moved_points = []
        for point in self.points:
            moved_points.append(point.move(vector))
        return Loop(moved_points)

    def extrude(self, value):
        faces = []
        move_vector = Vector3d(*self.normal.scale(value))
        for line in self.segments:
            border = line.extrude(move_vector)
            faces.append(border)
        return faces

    def is_point_in_loop(self, point: Point3d) -> bool:
        plane = self.plane()
        on_plane = plane.is_on_plane(point)
        if not on_plane:
            return False

        # convert points to u,v coordinates
        plane_coordinates = [plane.plane_coordinates(point) for point in self.points]
        point_plane_coordinates = plane.plane_coordinates(point)

        sum_segment_length = sum([segment.length for segment in self.segments])
        sum_segment_distances = sum([segment.distance_to_point(point) for segment in self.segments])
        max_length = sum_segment_length + sum_segment_distances

        consecutive_pairs = [[plane_coordinates[i], plane_coordinates[i + 1]]
                             for i in range(len(plane_coordinates) - 1)]
        uv_segments = [LineSegment(Point3d(start[0], start[1], 0), Point3d(end[0], end[1], 0)) for [start, end] in consecutive_pairs]

        uv_point = Point3d(point_plane_coordinates[0], point_plane_coordinates[1], 0)
        # Create a point at infinity, y is same as point p
        x_line = LineSegment(uv_point, Point3d(max_length, point_plane_coordinates[1], 0))
        count = 0

        for uv_segment in uv_segments:
            if uv_segment.is_point_on_segment(uv_point):
                return True

            if uv_segment.is_intersects(x_line):
                count += 1

        #i = 0
        #n = len(plane_coordinates) - 1
        #while True:
        #    # Forming a line from two consecutive points of
        #    # poly
        #    pc = plane_coordinates[i]
        #    pc_next = plane_coordinates[i + 1]
        #    side = LineSegment(Point3d(pc[0], pc[1], 0), Point3d(pc_next[0], pc_next[1], 0))
        #    if x_line.is_intersects(side):
        #        # If side is intersects x_line
        #        if side.is_point_on_line(uv_point):
        #            return True
        #    count += 1
        #    i = (i + 1) % n
        #    if i != 0:
        #        break

        # True when count is odd
        return count % 2 == 1


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
