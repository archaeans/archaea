# Archaea

Archaea is a base geometric library that includes basic geometric objects
to create meshes and triangulated exports of meshes.

Motivation of creating this library is started with master thesis, departments of Computational
Science and Engineering and Architecture at Istanbul Technical University. 
Aim of thesis is to create geometric definitions for different environmental
solvers like EnergyPlus and OpenFOAM to run them parallely on Linux environment.

Archaea is a geometrical playground for now, most important functionality of library
is executing earcut algorithm on 3D coordinate system by plane (u, v) transformations.
Shortly library can create triangulations with holes on 3D.


## Supported Objects

- CoordinateArray: Base object for vectoral operations on Vector and Point objects.
- Vector, Vector2d, Vector3d: Vector operations like Dot and Cross Product, also
serves transformations of other geometrical objects.
- Point, Point2d, Point3d: Position object to construct other geometric objects
like LineSegment, Polyline, Mesh..
- LineSegment: Construct with start and end point.
- Polyline: List of consecutive LineSegments
- Loop: Closed polyline definition.
- Face: Face is a loop definition that might have holes with inner loops.
- Mesh: Polygon and vertex list definition for exporting.


## Supported Operations

- Move: Objects can be moved by creating copy of source object.
- Reverse: LineSegment, Polyline, Loop and Face can be reversed.
- Offset: Loops and Faces can be offseted.
- Extrude: Faces can be extruded that creates list of Faces. Holes also covered.
