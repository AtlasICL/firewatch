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


def _farthest_point(
    a: Point,
    b: Point,
    points: list[Point],
) -> Point:
    """Finds the furthest point in `points` to the segment [AB]."""
    return max(points, key=lambda point: abs(_cross_product(a, b, point)))


def _quickhull_recurse(
    a: Point,
    b: Point,
    subset: list[Point],
) -> list[Point]:
    """
    Recursive part of the algorithm. A and B are the intial extrema.
    This function completes the convex hull on one side of [AB]. It does
    so by recursing.

    Args:
        `a`: One extremity of the initial line.
        `b`: The other extremity of the initial line.
        `subset`: The subset of the original set of points upon which
        the initial recursion is called.

    Returns:
        The convex hull of subset (which evidently includes A and B).
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
