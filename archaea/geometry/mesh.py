from archaea.geometry.point3d import Point3d
from archaea.geometry.face import Face
from archaea.writer.to_stl import to_stl
import numpy as np
import os


class Mesh:
    polygons: "list[list[int]]"
    vertices: "list[Point3d]"

    def __init__(self):
        self.polygons = []
        self.vertices = []

    def add_from_faces(self, faces: "list[Face]", share_vertices: bool = True):
        for face in faces:
            self.add_from_face(face, share_vertices)

    def add_from_face(self, face: Face, share_vertices: bool = True):
        face_vertices = face.mesh_polygon_vertices()
        for vertices in face_vertices:
            self.add_polygon(vertices, share_vertices)

    def add_polygon(self, vertices: "list[Point3d]", share_vertices: bool = True):
        polygon_indexes = []
        for vertex in vertices:
            if share_vertices:
                matches = [existing_vertex for existing_vertex in self.vertices if existing_vertex == vertex]
                if any(matches):
                    existing_vertex_index = self.vertices.index(matches[0])
                    polygon_indexes.append(existing_vertex_index)
                else:
                    self.vertices.append(vertex)
                    polygon_indexes.append(len(self.vertices) - 1)
            else:
                self.vertices.append(vertex)
                polygon_indexes.append(len(self.vertices) - 1)

        self.polygons.append(polygon_indexes)

    def to_stl(self, path, file_name):
        vertices = np.array([vertex.to_a() for vertex in self.vertices])
        faces = np.array(self.polygons)
        file_path = os.path.join(path, file_name)
        to_stl(faces, vertices, file_path)
