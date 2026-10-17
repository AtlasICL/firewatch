import unittest
from collections.abc import Iterable

from src.point import Point
from src.quickhull import _is_inside


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
            if not thruple:
                continue

            x_vals = [p.x for p in thruple]
            y_vals = [p.y for p in thruple]
            self.assertTrue(sorted(x_vals) or sorted(x_vals, reverse=True))
            self.assertTrue(sorted(y_vals) or sorted(y_vals, reverse=True))

        for point in points:
            self.assertTrue(_is_inside(hull, point))

    def assert_same_cycle(
        self,
        expected: list[Point],
        hull: list[Point],
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
