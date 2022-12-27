import functools
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d


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

    def extrude(self, vector):
        start = self.start
        end = self.end
        extruded_start = start.move(vector)
        extruded_end = end.move(vector)
        from src.geometry.loop import Loop
        from src.geometry.face import Face
        loop = Loop([start, end, extruded_end, extruded_start])
        return Face(loop)
