import unittest
from src.geometry.point3d import Point3d
from src.geometry.vector3d import Vector3d
from src.geometry.loop import Loop


class Setup(unittest.TestLoader):
    p1 = Point3d(0, 0, 0)
    p2 = Point3d(10, 0, 0)
    p3 = Point3d(10, 10, 0)
    p4 = Point3d(0, 10, 0)
    loop_triangle = Loop([p1, p2, p3])
    loop_rectangle = Loop([p1, p2, p3, p4])


class TestLoop3d(unittest.TestCase):
    def test_close_loop(self):
        # Assert
        self.assertEqual(len(Setup.loop_triangle.points), 4)

    def test_calculate_normal(self):
        # Assert
        self.assertEqual(Setup.loop_triangle.normal, Vector3d(0, 0, 1))

    def test_points(self):
        # Assert
        self.assertEqual(len(Setup.loop_rectangle.points), 5)

    def test_segments(self):
        # Act
        segments = Setup.loop_rectangle.segments

        self.assertTrue(True)

    def test_segment_count(self):
        # Assert
        self.assertEqual(Setup.loop_triangle.segment_count, 3)

    def test_extrude(self):
        # Act
        faces = Setup.loop_rectangle.extrude(5)
        faces_area = sum(face.area for face in faces)

        # Assert
        self.assertEqual(len(faces), 6)
        self.assertEqual(faces_area, 400)


if __name__ == '__main__':
    unittest.main()
