import unittest
from collections.abc import Iterable

from numpy import sign

from src.point import Point
from src.quickhull import _cross_product


class HullTestCase(unittest.TestCase):
    """`unittest.TestCase` with assertions for checking convex hulls."""

    def assert_is_convex_hull_of(
        self,
        points: Iterable[Point],
        hull: list[Point],
    ) -> None:
        """
        Asserts that `hull` is exactly the convex hull of `points`, in
        a cycle.

        For a set of points to be a convex hull, they must:

        1. Output must be a subset of the input.
        2. No point in the output should appear more than once.
        3. Every consecutive 3-tuple of points in the output turns the
           same way.
        4. Every single point from the input is either inside the hull,
           or part of the hull border.
        """
        self.assertTrue(set(hull).issubset(points))
        self.assertEqual(len(hull), len(list(set(hull))))
        for i in range(len(hull)):
            start, end = i * 3, min((i * 3) + 3, len(hull))
            thruple: list = hull[slice(start, end)]
            if not thruple or len(thruple) < 3:
                continue

            cross_product = _cross_product(thruple[0], thruple[1], thruple[2])
            self.assertEqual(sign(cross_product), -1)

            x_vals = [p.x for p in thruple]
            y_vals = [p.y for p in thruple]
            self.assertTrue(sorted(x_vals) or sorted(x_vals, reverse=True))
            self.assertTrue(sorted(y_vals) or sorted(y_vals, reverse=True))

        for point in points:
            self.assert_point_inside_convex_hull(hull, point)

    def assert_same_cycle(
        self,
        hull: list[Point],
        expected: list[Point],
    ) -> None:
        """
        Asserts that `hull` lists the same points as `expected` in the
        same cyclic order. It may start at any point and run in either
        direction.
        """
        rotations = [expected[i:] + expected[:i] for i in range(len(expected))]
        self.assertTrue(
            hull in rotations or hull[::-1] in rotations,
            f"Hull is not the same cycle as expected.\n"
            f"Hull:     {hull}\n"
            f"Expected: {expected}",
        )

    def assert_point_inside_convex_hull(
        self,
        hull: list[Point],
        point: Point,
    ) -> None:
        """
        Asserts that `point` lies inside the convex hull, or on its
        boundary.
        """
        for i in range(len(hull)):
            a = hull[i]
            b = hull[(i + 1) % len(hull)]
            self.assertLessEqual(
                _cross_product(a, b, point),
                0,
                f"Hull does not encapsulate all points.\n"
                f"Excluded point: {point}",
            )
