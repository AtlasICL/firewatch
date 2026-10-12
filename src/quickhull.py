from src.point import Point


def _find_leftmost_point_in(points: list[Point]) -> Point:
    """Finds the leftmost point in the given set."""
    if not points:
        raise RuntimeError("Attempted to find leftmost point of empty set.")
    return min(points, key=lambda point: point.x)


def _find_rightmost_point_in(points: list[Point]) -> Point:
    """Finds the rightmost point in the given set."""
    if not points:
        raise RuntimeError("Attempted to find rightmost point of empty set.")
    return max(points, key=lambda point: point.x)


def _cross_product(
    a: Point,
    b: Point,
    c: Point,
) -> float:
    """Finds the cross product of vectors AB and AC."""
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def quickhull(points: list[Point]) -> list[Point]:
    """
    Quickhull algorithm.

    Args:
        points: The set of points whose convex hull to calculate.

    Returns:
        The ordered list of points which form the convex hull of the
        input points.
    """
    leftmost_point: Point = _find_leftmost_point_in(points)
    rightmost_point: Point = _find_rightmost_point_in(points)

    points_above_inital_line = [
        point
        for point in points
        if _cross_product(leftmost_point, rightmost_point, point) > 0
    ]

    points_below_inital_line = [
        point
        for point in points
        if _cross_product(leftmost_point, rightmost_point, point) < 0
    ]

    print(points_above_inital_line, points_below_inital_line)
