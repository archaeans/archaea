import numpy as np
from stl import mesh


def build_stl(faces, vertices, file_name):
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j], :]

    # Write the mesh to file "cube.stl"
    cube.save('%s.stl' % file_name)
