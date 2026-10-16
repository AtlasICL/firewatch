import itertools
import unittest

from src.point import HullInput, Point
from src.quickhull import quickhull
from tests.resources.hull_checks import HullTestCase


class TestHullKnownCases(HullTestCase):
    """
    Manually created inputs, known hulls.
    Each test should `assertCountEqual` and `assert_same_cycle`.
    """

    def test_hull_of_mixed_point_set(self):
        """
        Worked example matching the explanatory diagrams in
        `../../img/example_output/`.
        """
        a = Point(-2, -1)
        b = Point(-4, 1)
        c = Point(-5, 3)
        d = Point(-3, 5)
        e = Point(2, 5)
        f = Point(6, 3)
        g = Point(6, 0)
        h = Point(5, -2)

        points = [
            a,
            b,
            c,
            d,
            e,
            f,
            g,
            h,
            Point(1, 0),
            Point(2, 3),
            Point(2, 0.5),
            Point(1, 4),
            Point(-3, 1),
            Point(1, -1),
            Point(-2, 2.5),
            Point(0, 3),
            Point(-0.5, 0.5),
            Point(-2, 4),
            Point(4, 2),
            Point(4, 1),
            Point(1, 1.5),
            Point(3.5, -1),
            Point(-1, 4.5),
        ]
        expected_hull = [c, b, a, h, g, f, e, d]

        hull = quickhull(HullInput(points))

        self.assertCountEqual(hull, expected_hull)
        self.assert_same_cycle(hull, expected_hull)

    def test_hull_excludes_edge_points_in_any_input_order(self):
        """
        When several points tie as farthest from a line, only the
        corners are on the hull. A point lying partway along a hull
        edge must be left out, whatever order the input is given in.
        """
        corners = [Point(0, 0), Point(1, 2), Point(3, 2), Point(4, 0)]
        edge_point = Point(2, 2)

        for points in itertools.permutations([*corners, edge_point]):
            with self.subTest(points=points):
                hull = quickhull(HullInput(points))

                self.assertCountEqual(hull, corners)
                self.assert_same_cycle(hull, corners)

    def test_only_two_distinct_points(self):
        self.skipTest("TODO")

    def test_two_points_with_duplicates(self):
        self.skipTest("TODO")

    def test_triangle(self):
        self.skipTest("TODO")

    def test_square_with_point_inside(self):
        self.skipTest("TODO")

    def test_horizontally_collinear_points(self):
        self.skipTest("TODO")

    def test_vertical_collinear_points(self):
        self.skipTest("TODO")

    def test_diagonally_collinear_points(self):
        self.skipTest("TODO")

    def test_multiple_points_tied_for_leftmost(self):
        self.skipTest("TODO")

    def test_multiple_points_tied_for_rightmost(self):
        self.skipTest("TODO")

    def test_negative_and_mixed_sign_coordinates(self):
        self.skipTest("TODO")


if __name__ == "__main__":
    unittest.main()
