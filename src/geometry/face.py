import functools
from src.geometry.vector3d import Vector3d
from src.geometry.loop import Loop
from src.eatcut.earcut import earcut


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
        all_loops = [self.outer_loop]
        all_loops += self.inner_loops
        for loop in all_loops:
            loop_faces = loop.extrude(value)
            all_faces += loop_faces
        move_vector = Vector3d(*self.normal.scale(value))
        cap = self.move(move_vector)
        all_faces.append(cap)
        return all_faces

    def mesh_polygon_vertices(self):
        all_loops = [self.outer_loop]
        all_loops += self.inner_loops
        all_points = self.outer_loop.points[:-1]
        hole_start_indexes = []
        for inner_loop in self.inner_loops:
            hole_start_indexes.append(len(all_points))
            all_points += inner_loop.points[:-1]

        hole_indices = None if len(hole_start_indexes) == 0 else hole_start_indexes
        flatten_coordinates = [num for sublist in all_points for num in sublist]
        polygons = earcut(flatten_coordinates, holeIndices=hole_indices, dim=3)

        n = 3
        triangular_polygons = [polygons[i:i + n] for i in range(0, len(polygons), n)]

        triangular_points = []
        for triangular_polygon in triangular_polygons:
            tp = triangular_polygon
            triangular_points.append([all_points[tp[0]], all_points[tp[1]], all_points[tp[2]]])

        return triangular_points


