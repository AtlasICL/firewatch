import itertools
import unittest

from src.point import HullInput, Point
from src.quickhull import quickhull
from tests.resources.hull_checks import HullTestCase, _is_inside


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
        d = Point(-3, 5.8)
        e = Point(2.1, 5)
        f = Point(6, 3)
        g = Point(6, 0.03)
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
                self.assert_same_cycle(corners, hull)

    def test_only_two_distinct_points(self):
        points = [Point(0, 1), Point(5, 6)]
        hull = quickhull(HullInput(points))

        self.assert_is_convex_hull_of(points, hull)
        self.assert_same_cycle(points, hull)

    def test_two_points_with_duplicates(self):
        pair = [Point(0, 0), Point(1, 2)]
        duplicates = [Point(0, 0), Point(1, 2), Point(0, 0), Point(1, 2)]
        hull = quickhull(HullInput(duplicates))

        self.assert_is_convex_hull_of(duplicates, hull)
        self.assert_same_cycle(pair, hull)

    def test_triangle(self):
        points = [Point(0, 1), Point(5, 6), Point(9, 4)]
        hull = quickhull(HullInput(points))

        self.assert_is_convex_hull_of(points, hull)
        self.assert_same_cycle(points, hull)

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
        self.assert_same_cycle(corners, hull)

    def test_horizontally_collinear_points(self):
        end_points = [Point(0, 1), Point(3, 1)]
        inbetween_points = [Point(0, 1), Point(3, 1), Point(1, 1), Point(2, 1)]
        hull = quickhull(HullInput(inbetween_points))

        self.assert_is_convex_hull_of(inbetween_points, hull)
        self.assert_same_cycle(end_points, hull)

    def test_vertical_collinear_points(self):
        end_points = [Point(0, 1), Point(0, 5)]
        inbetween_points = [Point(0, 1), Point(0, 5), Point(0, 2), Point(0, 3)]

        hull = quickhull(HullInput(inbetween_points))

        self.assert_is_convex_hull_of(inbetween_points, hull)
        self.assert_same_cycle(end_points, hull)

    def test_diagonally_collinear_points(self):
        end_points = [Point(0, 1), Point(3, 4)]
        inbetween_points = [Point(0, 1), Point(3, 4), Point(1, 2), Point(2, 3)]

        hull = quickhull(HullInput(inbetween_points))

        self.assert_is_convex_hull_of(inbetween_points, hull)
        self.assert_same_cycle(end_points, hull)

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
        self.assert_same_cycle(expected, hull)

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
        self.assert_same_cycle(expected, hull)

    def test_isinside(self):
        point_list = [
            Point(0, 1),
            Point(5, 6),
            Point(9, 6),
            Point(7, 6),
            Point(9, 0),
        ]

        hull = quickhull(HullInput(point_list))
        # Outside hull
        self.assertFalse(_is_inside(point_list, Point(100, 100)))
        # Border case
        self.assertTrue(_is_inside(hull, Point(9, 3)))


if __name__ == "__main__":
    unittest.main()
