import itertools
import unittest

from src.point import HullInput, Point
from src.quickhull import quickhull


def _is_same_cycle(hull: list[Point], expected: list[Point]) -> bool:
    """
    Checks whether `hull` lists the same points as `expected` in the
    same cyclic order. It may start at any vertex and run in either
    direction.
    """
    rotations = [expected[i:] + expected[:i] for i in range(len(expected))]
    return hull in rotations or hull[::-1] in rotations


class TestQuickhull(unittest.TestCase):
    def test_minimum_x_is_furthest_west_point(self):
        """
        Point min_x chosen by the algorithm is the coordinate that lies
        furthest west.
        """
        self.skipTest("TODO")

    def test_maximum_x_is_furthest_east_point(self):
        """
        Point max_x chosen by the algorithm is the coordinate that lies
        furthest east.
        """
        self.skipTest("TODO")

    def test_p_is_furthest_point_from_minmax_line(self):
        """
        Point p chosen by the algorithm is the coordinate that lies
        furthest from the straight line formed between min_x and max_x.
        """
        self.skipTest("TODO")

    def test_all_coordinates_lie_in_convex_hull_boundary(self):
        """
        All coordinates lie either within the convex hull, or on its
        boundary.
        """
        self.skipTest("TODO")

    def test_hull_of_mixed_point_set(self):
        """
        Sample test case for quickhull, taken from the explanatory
        visual graph in ../../img/example_output/
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
        self.assertTrue(
            _is_same_cycle(hull, expected_hull),
            f"Hull vertices are out of order. See below:\n{hull}",
        )

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
                self.assertTrue(_is_same_cycle(hull, corners))


if __name__ == "__main__":
    unittest.main()
