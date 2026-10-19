import unittest

from src.point import Point
from tests.hull_checks import HullTestCase

SQUARE_HULL = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]


class TestIsInside(HullTestCase):
    """
    Tests for `assert_point_inside_convex_hull`, used by
    `assert_is_convex_hull_of`.
    """

    def test_accepts_point_strictly_inside(self):
        self.assert_point_inside_convex_hull(SQUARE_HULL, Point(2, 2))

    def test_accepts_points_on_the_boundary(self):
        boundary_points = {
            "corner": Point(0, 0),
            "left edge": Point(0, 2),
            "top edge": Point(2, 4),
            "right edge": Point(4, 2),
            "bottom (closing) edge": Point(2, 0),
        }
        for description, point in boundary_points.items():
            with self.subTest(description):
                self.assert_point_inside_convex_hull(SQUARE_HULL, point)


if __name__ == "__main__":
    unittest.main()
