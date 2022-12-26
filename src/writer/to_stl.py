import numpy as np
from stl import mesh


def build_stl(faces, vertices, file_name):
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j], :]

    # Write the mesh to file "cube.stl"
    cube.save('%s.stl' % file_name)


vertices = np.random.random((100, 3))
faces = np.array(
    [
        [0, 3, 1],
        [1, 3, 2],

        [4, 7, 5],
        [5, 7, 6]
    ]
)

vertices = np.array(
    [
        [0, 0, 0], # 0
        [10, 0, 0], # 1
        [10, 10, 0], # 2
        [0, 10, 0], # 3

        [0, 0, 0],
        [10, 0, 0],
        [10, 0, 10],
        [0, 0, 10]
    ]
)

build_stl(faces, vertices, "test")