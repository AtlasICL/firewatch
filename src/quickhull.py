from src.point import HullInput, Point


def _find_leftmost_point_in(points: HullInput) -> Point:
    """Finds the leftmost point in the given set."""
    return min(points.points, key=lambda point: (point.x, point.y))


def _find_rightmost_point_in(points: HullInput) -> Point:
    """Finds the rightmost point in the given set."""
    return max(points.points, key=lambda point: (point.x, point.y))


def _cross_product(
    a: Point,
    b: Point,
    c: Point,
) -> float:
    """Finds the cross product of vectors AB and AC."""
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def _dot_product(
    a: Point,
    b: Point,
    c: Point,
) -> float:
    """Finds the dot product of vectors AB and AC."""
    return (b.x - a.x) * (c.x - a.x) + (b.y - a.y) * (c.y - a.y)


def _farthest_point(
    a: Point,
    b: Point,
    points: list[Point],
) -> Point:
    """
    Finds the furthest point in `points` to the segment [AB].

    Ties are broken in favour of the point closest to A along AB. Tied
    points lie on a line parallel to AB, and only the two ends of that
    line are hull vertices, therefore we must pick one of the "ends".
    """
    return max(
        points,
        key=lambda point: (
            abs(_cross_product(a, b, point)),
            -_dot_product(a, b, point),
        ),
    )


def _quickhull_recurse(
    a: Point,
    b: Point,
    subset: list[Point],
) -> list[Point]:
    """
    Recursive part of the algorithm. Completes the convex hull on the
    LHS of the directed segment [AB].

    Args:
        `a`: Start of the segment, already known to be on the hull.
        `b`: End of the segment, already known to be on the hull.
        `subset`: The points lying strictly to the left of [AB].

    Returns:
        The hull vertices (excluding A and B) lying strictly to the
        left of [AB], (ordered A to B).
    """

    # Base case.
    if not subset:
        return []

    # Find the farthest point from [AB].
    farthest_point: Point = _farthest_point(a=a, b=b, points=subset)

    subset_outside_ac = [
        point
        for point in subset
        if _cross_product(a, farthest_point, point) > 0
    ]

    subset_outside_cb = [
        point
        for point in subset
        if _cross_product(farthest_point, b, point) > 0
    ]

    return (
        _quickhull_recurse(a, farthest_point, subset_outside_ac)
        + [farthest_point]
        + _quickhull_recurse(farthest_point, b, subset_outside_cb)
    )


def quickhull(points: HullInput) -> list[Point]:
    """
    Quickhull algorithm. Given a set of at least 2 distinct points,
    returns the ordered list of points (subset of the input) which form
    its convex hull.

    Args:
        `points`: The set of points whose convex hull to calculate.

    Returns:
        The ordered list of points which form the convex hull of the
        input points.
    """
    leftmost_point: Point = _find_leftmost_point_in(points)
    rightmost_point: Point = _find_rightmost_point_in(points)

    # Divide into two sub-problems: the points either side of the
    # original line => divide and conquer.
    points_above_initial_line = [
        point
        for point in points.points
        if _cross_product(leftmost_point, rightmost_point, point) > 0
    ]
    points_below_initial_line = [
        point
        for point in points.points
        if _cross_product(leftmost_point, rightmost_point, point) < 0
    ]

    return (
        [leftmost_point]
        + _quickhull_recurse(
            leftmost_point,
            rightmost_point,
            points_above_initial_line,
        )
        + [rightmost_point]
        + _quickhull_recurse(
            rightmost_point,
            leftmost_point,
            points_below_initial_line,
        )
    )
