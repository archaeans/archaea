from typing import List

from archaea.geometry.point3d import Point3d
from archaea.geometry.face import Face
from archaea.writer.to_stl import to_stl
import numpy as np
import os


class Mesh:
    polygons: "list[list[int]]"
    vertices: "list[Point3d]"

    def __init__(self, polygons=None, vertices=None):
        if polygons is None:
            self.polygons = []
        else:
            self.polygons = polygons
        if vertices is None:
            self.vertices = []
        else:
            self.vertices = vertices

    @classmethod
    def from_ngon_mesh(cls, flat_point_values: "list[float]", ngon_mesh_indices: "list[int]"):
        points = []
        for i in range(0, len(flat_point_values), 3):
            pt = flat_point_values[i:i+3]
            points.append(Point3d(pt[0], pt[1], pt[2]))
        triangles = []
        i = 0

        while i < len(ngon_mesh_indices):
            num_edges = ngon_mesh_indices[i]
            i += 1
            polygon = ngon_mesh_indices[i:i + num_edges]
            i += num_edges

            if num_edges == 3:
                # If it's already a triangle, just add it to the list
                triangles.append(polygon)
            else:
                # Split the NGON into triangles while maintaining the same orientation
                for j in range(1, num_edges - 1):
                    triangles.append([polygon[0], polygon[j], polygon[j + 1]])
        
        return cls(triangles, points)
        

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

    def find_average_point(self) -> Point3d:
        # Initialize variables to store the sum of coordinates
        sum_x = sum_y = sum_z = 0

        # Iterate through the list of points and sum up their coordinates
        for point in self.vertices:
            sum_x += point.x
            sum_y += point.y
            sum_z += point.z

        # Calculate the average by dividing by the number of points
        num_points = len(self.vertices)
        average_x = sum_x / num_points
        average_y = sum_y / num_points
        average_z = sum_z / num_points

        # Create and return the average point
        return Point3d(average_x, average_y, average_z)

    def rotate(self, axis, angle, origin=None):
        origin_to_rotate_around = origin
        if origin is None:
            origin_to_rotate_around = self.find_average_point()

        rotated_vertices = []
        for point in self.vertices:
            rotated_vertices.append(point.rotate(axis, angle, origin_to_rotate_around))

        return Mesh(self.polygons, rotated_vertices)
