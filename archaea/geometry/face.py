import functools
from archaea.geometry.vector3d import Vector3d
from archaea.geometry.loop import Loop
from archaea.earcut.earcut import earcut


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

    @functools.cached_property
    def has_hole(self):
        return self.inner_loops != 0

    def move(self, vector):
        moved_outer_loop = self.outer_loop.move(vector)
        moved_inner_loops = []
        for loop in self.inner_loops:
            moved_inner_loops.append(loop.move(vector))
        return self.__class__(moved_outer_loop, moved_inner_loops)

    def extrude(self, value):
        if value == 0:
            return self
        all_faces = [self]
        all_loops = [self.outer_loop]
        all_loops += self.inner_loops
        all_faces += self.outer_loop.extrude(value)
        for loop in self.inner_loops:
            loop_faces = loop.extrude(value, True)
            all_faces += loop_faces
        move_vector = Vector3d(*self.normal.scale(value))
        cap: Face = self.move(move_vector)
        all_faces.append(cap.reverse())
        return all_faces

    def reverse(self):
        reversed_outer_loop = self.outer_loop.reverse()
        reversed_inner_loops = [loop.reverse() for loop in self.inner_loops]
        return self.__class__(reversed_outer_loop, reversed_inner_loops)

    def offset(self, value):
        offset_outer_loop = self.outer_loop.offset(value)
        return self.__class__(offset_outer_loop, self.inner_loops)

    def mesh_polygon_vertices(self):
        all_loops = [self.outer_loop]
        all_loops += self.inner_loops
        all_points = self.outer_loop.points[:-1]
        all_uv_points = self.outer_loop.uv_points()
        hole_start_indexes = []
        for inner_loop in self.inner_loops:
            hole_start_indexes.append(len(all_uv_points))
            all_points += inner_loop.points[:-1]
            all_uv_points += inner_loop.uv_points(self.outer_loop.plane())

        hole_indices = None if len(hole_start_indexes) == 0 else hole_start_indexes
        flatten_coordinates = [num for sublist in all_uv_points for num in sublist]
        polygons = earcut(flatten_coordinates, hole_indices=hole_indices)

        n = 3
        triangular_polygons = [polygons[i:i + n] for i in range(0, len(polygons), n)]

        triangular_points = []
        for triangular_polygon in triangular_polygons:
            tp = triangular_polygon
            triangular_points.append([all_points[tp[0]], all_points[tp[1]], all_points[tp[2]]])

        return triangular_points
