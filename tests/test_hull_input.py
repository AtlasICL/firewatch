import unittest

from src.point import HullInput, Point


class TestQuickhull(unittest.TestCase):
    def test_cannot_create_hullinput_with_fewer_than_two_distinct_points(self):
        """
        Unit test to verify that an instance of the `HullInput` class
        cannot be created with fewer than two distinct `Point` objects.
        """
        invalid_inputs = {
            "zero points": [],
            "one point": [Point(1, 1)],
            "two non-distinct points": [Point(2, 2), Point(2, 2)],
        }
        for description, points in invalid_inputs.items():
            with self.subTest(description), self.assertRaises(ValueError):
                HullInput(points)

    def test_can_create_hullinput_with_at_least_two_distinct_points(self):
        valid_inputs = {
            "two distinct points": [Point(7, 8), Point(9, 10)],
            "mix of distinct and non-distinct points": [
                Point(-1, -2),
                Point(-3, 4),
                Point(-3, -4),
                Point(-4, -5),
                Point(-4, -5),
            ],
            "many distinct points": [
                Point(11, 12),
                Point(13, 14),
                Point(13, 15),
                Point(14, -5),
                Point(-4, -5),
            ],
        }
        for description, points in valid_inputs.items():
            with self.subTest(description):
                hull_input = HullInput(points)
                self.assertEqual(hull_input.points, tuple(points))
