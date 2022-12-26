import functools
from vector3d import Vector3d
from point3d import Point3d
from face import Face


class Triangle(Face):
    points: "list[Point3d]"

    def __init__(self, points: "list[Point3d]"):
        if len(points) != 4:
            raise Exception("Triangle3d accept 4 point to define it as closed face.")

        if points[0] != points[-1]:
            raise Exception("First and last point of Triangle3d should be identical to define closed face.")

        Face.__init__(self, points=points)

    @functools.cached_property
    def normal(self):
        v1: Vector3d = self.points[0].vector_to(self.points[1])
        v2: Vector3d = self.points[0].vector_to(self.points[2])
        return v1.cross_product(v2).normalize()
