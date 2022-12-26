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

    @classmethod
    def from_point_and_vector(cls, start: Point3d, vector: Vector3d):
        end_point = start.move(vector)
        return cls(start, end_point)

    @functools.cached_property
    def length(self):
        return self.start.distance_to(self.end)

    def point_at(self, t: float) -> Point3d:
        vector = self.start.vector_to(self.end)
        return self.start + vector.scale(t)

    def extrude(self, vector):
        start = self.start
        end = self.end
        extruded_start = start.move(vector)
        extruded_end = end.move(vector)
        from src.geometry.loop import Loop
        from src.geometry.face import Face
        loop = Loop([start, end, extruded_end, extruded_start])
        return Face(loop)
