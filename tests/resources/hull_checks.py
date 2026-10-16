import unittest
from collections.abc import Iterable

from src.point import Point


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
        raise NotImplementedError

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
