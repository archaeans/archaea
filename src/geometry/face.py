import functools
from src.geometry.vector3d import Vector3d
from src.geometry.loop import Loop


class Face:
    outer_loop: Loop
    inner_loops: "list[Loop]"
    normal: Vector3d

    def __init__(self, outer_loop: Loop, inner_loops: "list[Loop]" = None):
        self.outer_loop = outer_loop
        self.normal = self.outer_loop.normal
        if inner_loops is None:
            self.inner_loops = []
        else:
            self.inner_loops = inner_loops

    @functools.cached_property
    def area(self):
        inner_loops_area = 0
        for loop in self.inner_loops:
            inner_loops_area += loop.area
        return self.outer_loop.area - inner_loops_area

    @functools.cached_property
    def plane(self):
        return self.outer_loop.plane()

    def move(self, vector):
        moved_outer_loop = self.outer_loop.move(vector)
        moved_inner_loops = []
        for loop in self.inner_loops:
            moved_inner_loops.append(loop.move(vector))
        return Face(moved_outer_loop, moved_inner_loops)

    def extrude(self, value):
        all_faces = [self]
        move_vector = Vector3d(self.normal.scale(value))
        all_loops = self.inner_loops.append(self.outer_loop)
        for loop in all_loops:
            loop_faces = loop.extrude(move_vector)
            all_faces += loop_faces
        cap = self.move(move_vector)
        all_faces.append(cap)

