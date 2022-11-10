import functools
from src.geometry.line_segment import LineSegment
from src.geometry.point3d import Point3d


class Polyline:
    segments: "list[LineSegment]"

    def __init__(self, segments: "list[LineSegment]"):
        self.segments = segments

    @functools.cached_property
    def segment_count(self):
        return len(self.segments)

    @functools.cached_property
    def length(self):
        return sum(segment.length for segment in self.segments)

    @functools.cached_property
    def point_at_start(self) -> Point3d:
        return self.segments[0].start

    @functools.cached_property
    def point_at_end(self) -> Point3d:
        return self.segments[-1].end

    @functools.cached_property
    def is_closed(self):
        return self.point_at_start == self.point_at_end

