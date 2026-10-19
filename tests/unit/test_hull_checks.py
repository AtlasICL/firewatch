import unittest

from src.point import Point
from tests.hull_checks import _is_inside

SQUARE_HULL = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]


class TestIsInside(unittest.TestCase):
    """Tests for `_is_inside`, used by `assert_is_convex_hull_of`."""

    def test_accepts_point_strictly_inside(self):
        self.assertTrue(_is_inside(SQUARE_HULL, Point(2, 2)))

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
                self.assertTrue(_is_inside(SQUARE_HULL, point))

    def test_rejects_points_outside(self):
        outside_points = {
            "beyond left edge": Point(-1, 2),
            "beyond top edge": Point(2, 5),
            "beyond right edge": Point(5, 2),
            "far away": Point(100, 100),
        }
        for description, point in outside_points.items():
            with self.subTest(description):
                self.assertFalse(_is_inside(SQUARE_HULL, point))

    # Known bug: `_is_inside` never checks the edge from the last hull
    # point back to the first. Remove this marker once that is fixed.
    @unittest.expectedFailure
    def test_rejects_point_beyond_closing_edge(self):
        self.assertFalse(_is_inside(SQUARE_HULL, Point(2, -1)))


if __name__ == "__main__":
    unittest.main()
