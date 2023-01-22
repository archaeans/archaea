import math

__all__ = ['earcut', 'deviation', 'flatten']


def earcut(data, hole_indices=None, dim=None):
    dim = dim or 2

    has_holes = hole_indices and len(hole_indices)
    outer_len = hole_indices[0] * dim if has_holes else len(data)
    outer_node = linked_list(data, 0, outer_len, dim, True)
    triangles = []

    if not outer_node:
        return triangles

    min_x = None
    min_y = None
    max_x = None
    max_y = None
    x = None
    y = None
    size = None

    if has_holes:
        outer_node = eliminate_holes(data, hole_indices, outer_node, dim)

    # if the shape is not too simple, we'll use z-order curve hash later; calculate polygon bbox
    if len(data) > 80 * dim:
        min_x = max_x = data[0]
        min_y = max_y = data[1]

        for i in range(dim, outer_len, dim):
            x = data[i]
            y = data[i + 1]
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        # minX, minY and size are later used to transform coords into integers for z-order calculation
        size = max(max_x - min_x, max_y - min_y)

    earcut_linked(outer_node, triangles, dim, min_x, min_y, size)

    return triangles


# create a circular doubly linked _list from polygon points in the specified winding order
def linked_list(data, start, end, dim, clockwise):
    i = None
    last = None

    if clockwise == (signed_area(data, start, end, dim) > 0):
        for i in range(start, end, dim):
            last = insert_node(i, data[i], data[i + 1], last)

    else:
        for i in reversed(range(start, end, dim)):
            last = insert_node(i, data[i], data[i + 1], last)

    if last and equals(last, last.next):
        remove_node(last)
        last = last.next

    return last


# eliminate collinear or duplicate points
def filter_points(start, end=None):
    if not start:
        return start
    if not end:
        end = start

    p = start
    again = True

    while again or p != end:
        again = False

        if not p.steiner and (equals(p, p.next) or area(p.prev, p, p.next) == 0):
            remove_node(p)
            p = end = p.prev
            if p == p.next:
                return None

            again = True

        else:
            p = p.next

    return end


# main ear slicing loop which triangulates a polygon (given as a linked _list)
def earcut_linked(ear, triangles, dim, minX, minY, size, _pass=None):
    if not ear:
        return

    # interlink polygon nodes in z-order
    if not _pass and size:
        index_curve(ear, minX, minY, size)

    stop = ear
    prev = None
    next = None

    # iterate through ears, slicing them one by one
    while ear.prev != ear.next:
        prev = ear.prev
        next = ear.next

        if is_ear_hashed(ear, minX, minY, size) if size else is_ear(ear):
            # cut off the triangle
            triangles.append(prev.i // dim)
            triangles.append(ear.i // dim)
            triangles.append(next.i // dim)

            remove_node(ear)

            # skipping the next vertex leads to less sliver triangles
            ear = next.next
            stop = next.next

            continue

        ear = next

        # if we looped through the whole remaining polygon and can't find any more ears
        if ear == stop:
            # try filtering points and slicing again
            if not _pass:
                earcut_linked(filter_points(ear), triangles, dim, minX, minY, size, 1)

                # if this didn't work, try curing all small self-intersections locally
            elif _pass == 1:
                ear = cure_local_intersections(ear, triangles, dim)
                earcut_linked(ear, triangles, dim, minX, minY, size, 2)

                # as a last resort, try splitting the remaining polygon into two
            elif _pass == 2:
                split_earcut(ear, triangles, dim, minX, minY, size)

            break


# check whether a polygon node forms a valid ear with adjacent nodes
def is_ear(ear):
    a = ear.prev
    b = ear
    c = ear.next

    if area(a, b, c) >= 0:
        return False  # reflex, can't be an ear

    # now make sure we don't have other points inside the potential ear
    p = ear.next.next

    while p != ear.prev:
        if point_in_triangle(a.x, a.y, b.x, b.y, c.x, c.y, p.x, p.y) and area(p.prev, p, p.next) >= 0:
            return False
        p = p.next

    return True


def is_ear_hashed(ear, min_x, min_y, size):
    a = ear.prev
    b = ear
    c = ear.next

    if area(a, b, c) >= 0:
        return False # reflex, can't be an ear

    # triangle bbox; min & max are calculated like this for speed
    min_tx = (a.x if a.x < c.x else c.x) if a.x < b.x else (b.x if b.x < c.x else c.x)
    min_ty = (a.y if a.y < c.y else c.y) if a.y < b.y else (b.y if b.y < c.y else c.y)
    max_tx = (a.x if a.x > c.x else c.x) if a.x > b.x else (b.x if b.x > c.x else c.x)
    max_ty = (a.y if a.y > c.y else c.y) if a.y > b.y else (b.y if b.y > c.y else c.y)

    # z-order range for the current triangle bbox;
    min_z = z_order(min_tx, min_ty, min_x, min_y, size)
    max_z = z_order(max_tx, max_ty, min_x, min_y, size)

    # first look for points inside the triangle in increasing z-order
    p = ear.nextZ

    while p and p.z <= max_z:
        if p != ear.prev and p != ear.next and point_in_triangle(a.x, a.y, b.x, b.y, c.x, c.y, p.x, p.y) and area(p.prev, p, p.next) >= 0:
            return False
        p = p.nextZ

    # then look for points in decreasing z-order
    p = ear.prevZ

    while p and p.z >= min_z:
        if p != ear.prev and p != ear.next and point_in_triangle(a.x, a.y, b.x, b.y, c.x, c.y, p.x, p.y) and area(p.prev, p, p.next) >= 0:
            return False
        p = p.prevZ

    return True


# go through all polygon nodes and cure small local self-intersections
def cure_local_intersections(start, triangles, dim):
    do = True
    p = start

    while do or p != start:
        do = False

        a = p.prev
        b = p.next.next

        if not equals(a, b) and intersects(a, p, p.next, b) and locally_inside(a, b) and locally_inside(b, a):
            triangles.append(a.i // dim)
            triangles.append(p.i // dim)
            triangles.append(b.i // dim)

            # remove two nodes involved
            remove_node(p)
            remove_node(p.next)

            p = start = b

        p = p.next

    return p


# try splitting polygon into two and triangulate them independently
def split_earcut(start, triangles, dim, min_x, min_y, size):
    # look for a valid diagonal that divides the polygon into two
    do = True
    a = start

    while do or a != start:
        do = False
        b = a.next.next

        while b != a.prev:
            if a.i != b.i and is_valid_diagonal(a, b):
                # split the polygon in two by the diagonal
                c = split_polygon(a, b)

                # filter collinear points around the cuts
                a = filter_points(a, a.next)
                c = filter_points(c, c.next)

                # run earcut on each half
                earcut_linked(a, triangles, dim, min_x, min_y, size)
                earcut_linked(c, triangles, dim, min_x, min_y, size)
                return

            b = b.next

        a = a.next


# link every hole into the outer loop, producing a single-ring polygon without holes
def eliminate_holes(data, hole_indices, outer_node, dim):
    queue = []
    i = None
    _len = len(hole_indices)
    start = None
    end = None
    _list = None

    for i in range(len(hole_indices)):
        start = hole_indices[i] * dim
        end = hole_indices[i + 1] * dim if i < _len - 1 else len(data)
        _list = linked_list(data, start, end, dim, False)

        if _list == _list.next:
            _list.steiner = True

        queue.append(get_leftmost(_list))

    queue = sorted(queue, key=lambda i: i.x)

    # process holes from left to right
    for i in range(len(queue)):
        eliminate_hole(queue[i], outer_node)
        outer_node = filter_points(outer_node, outer_node.next)

    return outer_node


# find a bridge between vertices that connects hole with an outer ring and and link it
def eliminate_hole(hole, outer_node):
    outer_node = find_hole_bridge(hole, outer_node)
    if outer_node:
        b = split_polygon(outer_node, hole)
        filter_points(b, b.next)


# David Eberly's algorithm for finding a bridge between hole and outer polygon
def find_hole_bridge(hole, outer_node):
    do = True
    p = outer_node
    hx = hole.x
    hy = hole.y
    qx = -math.inf
    m = None

    # find a segment intersected by a ray from the hole's leftmost point to the left;
    # segment's endpoint with lesser x will be potential connection point
    while do or p != outer_node:
        do = False
        if p.y >= hy >= p.next.y and p.next.y - p.y != 0:
            x = p.x + (hy - p.y) * (p.next.x - p.x) / (p.next.y - p.y)

            if hx >= x > qx:
                qx = x

                if x == hx:
                    if hy == p.y:
                        return p
                    if hy == p.next.y:
                        return p.next

                m = p if p.x < p.next.x else p.next

        p = p.next

    if not m:
        return None

    if hx == qx:
        return m.prev # hole touches outer segment; pick lower endpoint

    # look for points inside the triangle of hole point, segment intersection and endpoint;
    # if there are no points found, we have a valid connection;
    # otherwise choose the point of the minimum angle with the ray as connection point

    stop = m
    mx = m.x
    my = m.y
    tan_min = math.inf
    tan = None

    p = m.next

    while p != stop:
        hx_or_qx = hx if hy < my else qx
        qx_or_hx = qx if hy < my else hx

        if hx >= p.x >= mx and point_in_triangle(hx_or_qx, hy, mx, my, qx_or_hx, hy, p.x, p.y):

            tan = abs(hy - p.y) / (hx - p.x)  # tangential

            if (tan < tan_min or (tan == tan_min and p.x > m.x)) and locally_inside(p, hole):
                m = p
                tan_min = tan

        p = p.next

    return m


# interlink polygon nodes in z-order
def index_curve(start, min_x, min_y, size):
    do = True
    p = start

    while do or p != start:
        do = False

        if p.z is None:
            p.z = z_order(p.x, p.y, min_x, min_y, size)

        p.prevZ = p.prev
        p.nextZ = p.next
        p = p.next

    p.prevZ.nextZ = None
    p.prevZ = None

    sort_linked(p)


# Simon Tatham's linked _list merge sort algorithm
# http:#www.chiark.greenend.org.uk/~sgtatham/algorithms/_listsort.html
def sort_linked(_list):
    do = True
    i = None
    p = None
    q = None
    e = None
    tail = None
    num_merges = None
    p_size = None
    q_size = None
    in_size = 1

    while do or num_merges > 1:
        do = False
        p = _list
        _list = None
        tail = None
        num_merges = 0

        while p:
            num_merges += 1
            q = p
            p_size = 0
            for i in range(in_size):
                p_size += 1
                q = q.nextZ
                if not q:
                    break

            q_size = in_size

            while p_size > 0 or (q_size > 0 and q):

                if p_size == 0:
                    e = q
                    q = q.nextZ
                    q_size -= 1

                elif q_size == 0 or not q:
                    e = p
                    p = p.nextZ
                    p_size -= 1

                elif p.z <= q.z:
                    e = p
                    p = p.nextZ
                    p_size -= 1

                else:
                    e = q
                    q = q.nextZ
                    q_size -= 1

                if tail:
                    tail.nextZ = e

                else:
                    _list = e

                e.prevZ = tail
                tail = e

            p = q

        tail.nextZ = None
        in_size *= 2

    return _list


# z-order of a point given coords and size of the data bounding box
def z_order(x, y, min_x, min_y, size):
    # coords are transformed into non-negative 15-bit integer range
    x = 32767 * (x - min_x) // size
    y = 32767 * (y - min_y) // size

    x = (x | (x << 8)) & 0x00FF00FF
    x = (x | (x << 4)) & 0x0F0F0F0F
    x = (x | (x << 2)) & 0x33333333
    x = (x | (x << 1)) & 0x55555555

    y = (y | (y << 8)) & 0x00FF00FF
    y = (y | (y << 4)) & 0x0F0F0F0F
    y = (y | (y << 2)) & 0x33333333
    y = (y | (y << 1)) & 0x55555555

    return x | (y << 1)


# find the leftmost node of a polygon ring
def get_leftmost(start):
    do = True
    p = start
    leftmost = start

    while do or p != start:
        do = False
        if p.x < leftmost.x:
            leftmost = p
        p = p.next

    return leftmost


# check if a point lies within a convex triangle
def point_in_triangle(ax, ay, bx, by, cx, cy, px, py):
    return (cx - px) * (ay - py) - (ax - px) * (cy - py) >= 0 and \
        (ax - px) * (by - py) - (bx - px) * (ay - py) >= 0 and \
        (bx - px) * (cy - py) - (cx - px) * (by - py) >= 0


# check if a diagonal between two polygon nodes is valid (lies in polygon interior)
def is_valid_diagonal(a, b):
    return a.next.i != b.i and a.prev.i != b.i and not intersects_polygon(a, b) and \
        locally_inside(a, b) and locally_inside(b, a) and middle_inside(a, b)


# signed area of a triangle
def area(p, q, r):
    return (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)


# check if two points are equal
def equals(p1, p2):
    return p1.x == p2.x and p1.y == p2.y


# check if two segments intersect
def intersects(p1, q1, p2, q2):
    if (equals(p1, q1) and equals(p2, q2)) or (equals(p1, q2) and equals(p2, q1)):
        return True

    return area(p1, q1, p2) > 0 != area(p1, q1, q2) > 0 and \
        area(p2, q2, p1) > 0 != area(p2, q2, q1) > 0


# check if a polygon diagonal intersects any polygon segments
def intersects_polygon(a, b):
    do = True
    p = a

    while do or p != a:
        do = False
        if p.i != a.i and p.next.i != a.i and p.i != b.i and p.next.i != b.i and intersects(p, p.next, a, b):
            return True

        p = p.next

    return False


# check if a polygon diagonal is locally inside the polygon
def locally_inside(a, b):
    if area(a.prev, a, a.next) < 0:
        return area(a, b, a.next) >= 0 and area(a, a.prev, b) >= 0
    else:
        return area(a, b, a.prev) < 0 or area(a, a.next, b) < 0


# check if the middle point of a polygon diagonal is inside the polygon
def middle_inside(a, b):
    do = True
    p = a
    inside = False
    px = (a.x + b.x) / 2
    py = (a.y + b.y) / 2

    while do or p != a:
        do = False
        if ((p.y > py) != (p.next.y > py)) and (px < (p.next.x - p.x) * (py - p.y) / (p.next.y - p.y) + p.x):
            inside = not inside

        p = p.next

    return inside


# link two polygon vertices with a bridge; if the vertices belong to the same ring, it splits polygon into two;
# if one belongs to the outer ring and another to a hole, it merges it into a single ring
def split_polygon(a, b):
    a2 = Node(a.i, a.x, a.y)
    b2 = Node(b.i, b.x, b.y)
    an = a.next
    bp = b.prev

    a.next = b
    b.prev = a

    a2.next = an
    an.prev = a2

    b2.next = a2
    a2.prev = b2

    bp.next = b2
    b2.prev = bp

    return b2


# create a node and optionally link it with previous one (in a circular doubly linked _list)
def insert_node(i, x, y, last):
    p = Node(i, x, y)

    if not last:
        p.prev = p
        p.next = p

    else:
        p.next = last.next
        p.prev = last
        last.next.prev = p
        last.next = p

    return p


def remove_node(p):
    p.next.prev = p.prev
    p.prev.next = p.next

    if p.prevZ:
        p.prevZ.nextZ = p.nextZ

    if p.nextZ:
        p.nextZ.prevZ = p.prevZ


class Node(object):
    def __init__(self, i, x, y):
        # vertex index in coordinates array
        self.i = i

        # vertex coordinates

        self.x = x
        self.y = y

        # previous and next vertex nodes in a polygon ring
        self.prev = None
        self.next = None

        # z-order curve value
        self.z = None

        # previous and next nodes in z-order
        self.prevZ = None
        self.nextZ = None

        # indicates whether this is a steiner point
        self.steiner = False


# return a percentage difference between the polygon area and its triangulation area;
# used to verify correctness of triangulation
def deviation(data, hole_indices, dim, triangles):
    _len = len(hole_indices)
    has_holes = hole_indices and len(hole_indices)
    outer_len = hole_indices[0] * dim if has_holes else len(data)

    polygon_area = abs(signed_area(data, 0, outer_len, dim))

    if has_holes:
        for i in range(_len):
            start = hole_indices[i] * dim
            end = hole_indices[i + 1] * dim if i < _len - 1 else len(data)
            polygon_area -= abs(signed_area(data, start, end, dim))

    triangles_area = 0

    for i in range(0, len(triangles), 3):
        a = triangles[i] * dim
        b = triangles[i + 1] * dim
        c = triangles[i + 2] * dim
        triangles_area += abs(
            (data[a] - data[c]) * (data[b + 1] - data[a + 1]) -
            (data[a] - data[b]) * (data[c + 1] - data[a + 1]))

    if polygon_area == 0 and triangles_area == 0:
        return 0

    return abs((triangles_area - polygon_area) / polygon_area)


def signed_area(data, start, end, dim):
    sum_area = 0
    j = end - dim

    for i in range(start, end, dim):
        sum_area += (data[j] - data[i]) * (data[i + 1] + data[j + 1])
        j = i

    return sum_area


# turn a polygon in a multi-dimensional array form (e.g. as in GeoJSON) into a form Earcut accepts
def flatten(data):
    dim = len(data[0][0])
    result = {
        'vertices': [],
        'holes': [],
        'dimensions': dim
    }
    hole_index = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            for d in range(dim):
                result['vertices'].append(data[i][j][d])

        if i > 0:
            hole_index += len(data[i - 1])
            result['holes'].append(hole_index)

    return result


def unflatten(data):
    result = []

    for i in range(0, len(data), 3):
        result.append(tuple(data[i:i + 3]))

    return result
