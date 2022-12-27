from src.geometry.point3d import Point3d
from src.writer.to_stl import to_stl
import numpy as np


class Mesh:
    polygons: "list[list[int]]"
    vertices: "list[Point3d]"

    def __init__(self):
        self.polygons = []
        self.vertices = []

    def add_from_face(self, face):
        raise 'Not implemented'

    def add_polygon(self, vertices: "list[Point3d]"):
        polygon_indexes = []
        for vertex in vertices:
            matches = [existing_vertex for existing_vertex in self.vertices if existing_vertex == vertex]
            if any(matches):
                existing_vertex_index = self.vertices.index(matches[0])
                polygon_indexes.append(existing_vertex_index)
            else:
                self.vertices.append(vertex)
                polygon_indexes.append(len(self.vertices) - 1)
        self.polygons.append(polygon_indexes)

    def to_stl(self, path, file_name):
        vertices = np.array([vertex.to_a() for vertex in self.vertices])
        faces = np.array(self.polygons)
        to_stl(faces, vertices, file_name)
