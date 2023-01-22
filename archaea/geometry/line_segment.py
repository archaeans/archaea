import functools
from archaea.geometry.point3d import Point3d
from archaea.geometry.plane import Plane
from archaea.geometry.vector3d import Vector3d


# FIXME: Inherit later from base LineSegment object to cover common functionality
#  to prevent duplicated codes
class LineSegment:
    start: Point3d
    end: Point3d

    def __init__(self, start: Point3d, end: Point3d):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    @classmethod
    def from_point_and_vector(cls, start: Point3d, vector: Vector3d):
        end_point = start.move(vector)
        return cls(start, end_point)

    @functools.cached_property
    def length(self):
        return self.start.distance_to(self.end)

    @functools.cached_property
    def vector(self):
        return self.start.vector_to(self.end)

    def reverse(self):
        return LineSegment(self.end, self.start)

    def point_at(self, t: float) -> Point3d:
        return self.start + self.vector.scale(t)

    def parameter_at(self, point: Point3d):
        return self.start.vector_to(point).dot(self.vector) / self.vector.magnitude()**2

    def is_point_on_line(self, point: Point3d):
        return point == self.point_at(self.parameter_at(point))

    def is_point_on_segment(self, point: Point3d):
        parameter = self.parameter_at(point)
        return self.is_point_on_line(point) and 0 <= parameter <= 1

    def closest_point(self, point: Point3d):
        closest_parameter = self.closest_point_parameter(point)
        if closest_parameter <= 0:
            return self.start
        elif closest_parameter >= 1:
            return self.end
        else:
            return self.point_at(closest_parameter)

    def closest_point_parameter(self, point: Point3d):
        return self.vector.dot(self.start.vector_to(point)) / self.length**2

    def distance_to_point(self, point: Point3d):
        closest_point = self.closest_point(point)
        return closest_point.distance_to(point)

    def normal_on_plane(self, plane: Plane):
        return self.vector.cross_product(plane.normal).normalize()

    def distance_to_segment(self, segment):
        if self.is_intersects(segment):
            return 0
        distances = [
            self.distance_to_point(segment.start),
            self.distance_to_point(segment.end),
            segment.distance_to_point(self.start),
            segment.distance_to_point(self.end)
        ]
        return min(distances)

    # Thanks to https://stackoverflow.com/questions/55220355/how-to-detect-whether-two-segments-in-3d-space-intersect
    def is_intersects(self, segment):
        p1 = self.start.position_vector
        p2 = self.end.position_vector
        q1 = segment.start.position_vector
        q2 = segment.end.position_vector
        p_segment_vector = p2 - p1
        q_segment_vector = q2 - q1
        qp_distance_vector = q1 - p1
        p_length = self.length

        a = p_segment_vector.dot(qp_distance_vector) / p_length**2
        b = p_segment_vector.dot(q_segment_vector) / p_length**2
        c = p_segment_vector.scale(b) - q_segment_vector
        c_length = c.length
        if c_length == 0:
            c_length = 1
        t1 = c.dot(q1 - p1.scale(1 - a) - p2.scale(a)) / c_length**2
        t0 = a + (t1 * b)
        is_intersects = (0 <= t0 <= 1) and (0 <= t1 <= 1)
        return is_intersects

    def extrude(self, vector):
        start = self.start
        end = self.end
        extruded_start = start.move(vector)
        extruded_end = end.move(vector)
        from archaea.geometry.loop import Loop
        from archaea.geometry.face import Face
        loop = Loop([start, end, extruded_end, extruded_start])
        return Face(loop)

    def move(self, vector):
        moved_start = self.start.move(vector)
        moved_end = self.end.move(vector)
        return LineSegment(moved_start, moved_end)

    @staticmethod
    def line_intersection(line1, line2):
        plane = Plane.from_3_point(line1.start, line1.end, line2.start)
        line1_uv = [plane.plane_coordinates(line1.start), plane.plane_coordinates(line1.end)]
        line2_uv = [plane.plane_coordinates(line2.start), plane.plane_coordinates(line2.end)]
        intersected_uv = LineSegment.line_intersection_uv(line1_uv, line2_uv)
        return plane.point_at(intersected_uv[0], intersected_uv[1])

    @staticmethod
    def line_intersection_uv(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    @staticmethod
    def line_intersection_2(line1, line2):
        xdiff = (line1.start.x - line1.end.x, line2.start.x - line2.end.x)
        ydiff = (line1.start.y - line1.end.y, line2.start.y - line2.end.y)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')
        d = (det([line1.start.x, line1.start.y], [line1.end.x, line1.end.y]),
             det([line2.start.x, line2.start.y], [line2.end.x, line2.end.y]))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y
