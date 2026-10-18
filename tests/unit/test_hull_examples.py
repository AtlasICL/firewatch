import itertools
import unittest

from src.point import HullInput, Point
from src.quickhull import quickhull
from tests.hull_checks import HullTestCase


class TestHullKnownCases(HullTestCase):
    """
    Hand-picked inputs with known hulls. Each test checks the result
    against the exact expected hull with `assert_same_cycle`, which
    compares both the points and their order.
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

                self.assert_is_convex_hull_of(corners, hull)
                self.assert_same_cycle(hull, corners)

    def test_only_two_distinct_points(self):
        points = [Point(0, 1), Point(5, 6)]
        hull = quickhull(HullInput(points))

        self.assert_is_convex_hull_of(points, hull)
        self.assert_same_cycle(hull, points)

    def test_two_points_with_duplicates(self):
        pair = [Point(0, 0), Point(1, 2)]
        duplicates = [Point(0, 0), Point(1, 2), Point(0, 0), Point(1, 2)]
        hull = quickhull(HullInput(duplicates))

        self.assert_is_convex_hull_of(duplicates, hull)
        self.assert_same_cycle(hull, pair)

    def test_triangle(self):
        points = [Point(0, 1), Point(5, 6), Point(9, 4)]
        hull = quickhull(HullInput(points))

        self.assert_is_convex_hull_of(points, hull)
        self.assert_same_cycle(hull, points)

    def test_square_with_point_inside(self):
        corners = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]
        centre_point = [
            Point(0, 0),
            Point(0, 4),
            Point(4, 4),
            Point(4, 0),
            Point(2, 2),
        ]

        hull = quickhull(HullInput(centre_point))

        self.assert_is_convex_hull_of(centre_point, hull)
        self.assert_same_cycle(hull, corners)

    def test_horizontally_collinear_points(self):
        end_points = [Point(0, 1), Point(3, 1)]
        inbetween_points = [Point(0, 1), Point(3, 1), Point(1, 1), Point(2, 1)]
        hull = quickhull(HullInput(inbetween_points))

        self.assert_is_convex_hull_of(inbetween_points, hull)
        self.assert_same_cycle(hull, end_points)

    def test_vertical_collinear_points(self):
        end_points = [Point(0, 1), Point(0, 5)]
        inbetween_points = [Point(0, 1), Point(0, 5), Point(0, 2), Point(0, 3)]

        hull = quickhull(HullInput(inbetween_points))

        self.assert_is_convex_hull_of(inbetween_points, hull)
        self.assert_same_cycle(hull, end_points)

    def test_diagonally_collinear_points(self):
        end_points = [Point(0, 1), Point(3, 4)]
        inbetween_points = [Point(0, 1), Point(3, 4), Point(1, 2), Point(2, 3)]

        hull = quickhull(HullInput(inbetween_points))

        self.assert_is_convex_hull_of(inbetween_points, hull)
        self.assert_same_cycle(hull, end_points)

    def test_multiple_points_tied_for_leftmost(self):
        expected = [Point(0, 1), Point(0, 5), Point(5, 6), Point(9, 6)]
        hull_input = [
            Point(0, 1),
            Point(5, 6),
            Point(9, 6),
            Point(7, 6),
            Point(0, 5),
        ]

        hull = quickhull(HullInput(hull_input))

        self.assert_is_convex_hull_of(hull_input, hull)
        self.assert_same_cycle(hull, expected)

    def test_multiple_points_tied_for_rightmost(self):
        expected = [Point(0, 1), Point(5, 6), Point(9, 6), Point(9, 0)]
        hull_input = [
            Point(0, 1),
            Point(5, 6),
            Point(9, 6),
            Point(7, 6),
            Point(9, 0),
        ]

        hull = quickhull(HullInput(hull_input))

        self.assert_is_convex_hull_of(hull_input, hull)
        self.assert_same_cycle(hull, expected)

    def test_floating_point_values(self):
        expected = [
            Point(-3.164, 1.8),
            Point(-2.24, 2.51),
            Point(1.05, 4.987),
            Point(1.3701, -1.0006),
        ]
        hull_input = [
            Point(1.05, 4.987),
            Point(-3.164, 1.8),
            Point(1.3701, -1.0006),
            Point(-2.24, 2.51),
            Point(0, 3.531),
            Point(-0.5001, 0.59987),
        ]

        hull = quickhull(HullInput(hull_input))
        self.assert_is_convex_hull_of(hull_input, hull)
        self.assert_same_cycle(hull, expected)


if __name__ == "__main__":
    unittest.main()
