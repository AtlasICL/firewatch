import unittest

from src.point import HullInput, Point
from tests.resources.test_data import (
    boundary_test_datasets,
    erroneous_test_datasets,
    erroneous_test_points,
    typical_test_datasets,
)


class TestHullInput(unittest.TestCase):
    def test_cannot_create_invalid_point(self):
        for test_case in erroneous_test_points:
            with self.assertRaises(TypeError):
                Point(*test_case)

    def test_cannot_create_hullinput_with_fewer_than_two_distinct_points(self):
        """
        ValueError should be thrown when attempting to create a
        HullInput instance using the erroneous test datasets.
        """
        for test_case in erroneous_test_datasets:
            with self.assertRaises(ValueError):
                HullInput(test_case)

    def test_can_create_hullinput_with_at_least_two_distinct_points(self):
        """
        An iterable HullInput instance should be created when using the
        boundary and typical test datasets to do so.
        """
        for test_case in boundary_test_datasets:
            hull_input = HullInput(test_case)
            self.assertEqual(hull_input.points, tuple(test_case))
        for test_case in typical_test_datasets:
            hull_input = HullInput(test_case)
            self.assertEqual(hull_input.points, tuple(test_case))
