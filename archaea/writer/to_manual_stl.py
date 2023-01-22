from typing import TextIO
from pathlib import Path

from archaea.geometry.face import Face
from archaea.geometry.point3d import Point3d
from archaea.geometry.triangle import Triangle

p1 = Point3d(0, 0, 0)
p2 = Point3d(10, 0, 0)
p3 = Point3d(10, 10, 0)
p4 = Point3d(0, 10, 0)

p5 = Point3d(0, 0, 10)
p6 = Point3d(10, 0, 10)
p7 = Point3d(10, 10, 10)
p8 = Point3d(0, 10, 10)

triangle_floor_1 = Triangle([p1, p3, p2, p1])
triangle_floor_2 = Triangle([p1, p4, p3, p1])

triangle_ceiling_1 = Triangle([p5, p6, p7, p5])
triangle_ceiling_2 = Triangle([p5, p7, p8, p5])

triangle_left_1 = Triangle([p1, p8, p4, p1])
triangle_left_2 = Triangle([p1, p5, p8, p1])

triangle_right_1 = Triangle([p2, p3, p7, p2])
triangle_right_2 = Triangle([p2, p7, p6, p2])

triangle_front_1 = Triangle([p1, p6, p5, p1])
triangle_front_2 = Triangle([p1, p2, p6, p1])

triangle_back_1 = Triangle([p4, p8, p7, p4])
triangle_back_2 = Triangle([p4, p7, p3, p4])


def border_to_stl(file: TextIO, border: Face):
    file.write("facet normal {x} {y} {z}\n".format(x=border.normal.x, y=border.normal.y, z=border.normal.z))
    file.write("outer loop\n")
    for vertex in border.points[0:-1]:
        file.write("vertex {x} {y} {z}\n".format(x=vertex.x, y=vertex.y, z=vertex.z))
    file.write("endloop\n")
    file.write("endfacet\n")


def to_stl(solid_name: str, borders: "list[Face]", export_name: str, path: str = None):
    filtered_borders = [border for border in borders if len(border.points) == 4]
    if path is None:
        current_path = Path.cwd()
        parent_directory = current_path.parent.absolute()
        path = parent_directory.joinpath("format", "export", "stl", "{file_name}.stl".format(file_name=export_name))
    file = open(path, "w")
    file.write("solid {solid_name}\n".format(solid_name=solid_name))
    for border in filtered_borders:
        border_to_stl(file, border)
    file.write("endsolid {solid_name}".format(solid_name=solid_name))


to_stl("test", [
    triangle_floor_1, triangle_floor_2,
    triangle_ceiling_1, triangle_ceiling_2,
    triangle_left_1, triangle_left_2,
    triangle_right_1, triangle_right_2,
    triangle_back_1, triangle_back_2,
    triangle_front_1, triangle_front_2
    ], "test_border")
