import unittest

from src.point import HullInput, Point
from src.quickhull import (
    _cross_product,
    _farthest_point,
    _find_leftmost_point_in,
    _find_rightmost_point_in,
)
from tests.resources.test_data import typical_test_datasets


class TestQuickhull(unittest.TestCase):
    def setUp(self):
        """
        Transforms the list of typical test datasets into a list of
        iterable HullInput objects.
        """
        self.test_cases: list[HullInput] = []
        for test_dataset in typical_test_datasets:
            self.test_cases.append(HullInput(test_dataset))

    def test_leftmost_point_has_minimum_x_coordinate(self):
        """
        The leftmost point chosen by the algorithm is the Point object
        with the minimum x coordinate.
        """
        expected_outputs = [55.4245, 51.1398, 50.4169, 54.8026]
        for expected, test_case in zip(expected_outputs, self.test_cases):
            self.assertEqual(
                expected,
                _find_leftmost_point_in(test_case).x,
            )

    def test_rightmost_point_has_maximum_x_coordinate(self):
        """
        The rightmost point chosen by the algorithm is the Point object
        with the maximum x coordinate.
        """
        expected_outputs = [57.4624, 52.0173, 52.9985, 55.5164]
        for expected, test_case in zip(expected_outputs, self.test_cases):
            self.assertEqual(
                expected,
                _find_rightmost_point_in(test_case).x,
            )

    def test_cross_product_of_two_vectors_calculated_correctly(self):
        """
        The cross product of two vectors AB and AC should be calculated
        according to the cross product formula.
        """
        expected_outputs = [-0.1335, 0.0025, 0.1011, 0.1449]
        for expected, test_case in zip(expected_outputs, self.test_cases):
            a: Point = test_case.points[0]
            b: Point = test_case.points[1]
            c: Point = test_case.points[2]
            self.assertEqual(
                expected,
                round(_cross_product(a, b, c), 4),
            )

    def test_farthest_point_from_segment_calculated_correctly(self):
        """
        The farthest point on the graph from the segment [AB] should
        be returned.
        """
        expected_outputs = [
            Point(55.5164, -2.088),
            Point(51.9744, -4.7628),
            Point(52.9985, -4.2297),
            Point(55.5164, -2.088),
        ]
        for expected, test_case in zip(expected_outputs, self.test_cases):
            a: Point = test_case.points[0]
            b: Point = test_case.points[1]
            self.assertEqual(
                expected,
                _farthest_point(a, b, test_case.points),
            )


if __name__ == "__main__":
    unittest.main()
