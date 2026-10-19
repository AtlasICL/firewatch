import unittest

from src.point import HullInput, Point


class TestPoint(unittest.TestCase):
    def test_accepts_int_and_float_mixed_coordinates(self):
        self.skipTest("TODO")

    def test_rejects_non_numeric_coordinates(self):
        self.skipTest("TODO")

    def test_rejects_bool_coordinates(self):
        self.skipTest("TODO")

    def test_rejects_nan_and_infinite_coordinates(self):
        self.skipTest("TODO")


class TestHullInput(unittest.TestCase):
    def test_cannot_create_hullinput_with_fewer_than_two_distinct_points(self):
        """
        ValueError should be thrown when attempting to create a
        HullInput instance with fewer than two distinct points.
        """
        invalid_test_datasets: dict[str, list[Point]] = {
            "no points": [],
            "one point (North-east Scotland)": [
                Point(56.9148, -2.9096),
            ],
            "two identical points": [
                Point(2, 2),
                Point(2, 2),
            ],
            "many copies of one point": [Point(2, 2)] * 5,
        }

        for description, test_case in invalid_test_datasets.items():
            with self.subTest(description), self.assertRaises(ValueError):
                HullInput(test_case)

    def test_can_create_hullinput_with_at_least_two_distinct_points(self):
        """
        An iterable HullInput instance should be created when using the
        boundary and typical test datasets to do so.
        """
        boundary_test_datasets: dict[str, list[Point]] = {
            "two points (North-east Scotland)": [
                Point(56.9148, -2.9096),
                Point(57.186, -2.8699),
            ],
            "two points (Central and North Scotland)": [
                Point(56.5211, -3.8046),
                Point(55.9308, -3.9848),
            ],
            "two distinct points with duplicates": [
                Point(2, 2),
                Point(2, 2),
                Point(3, 3),
            ],
        }

        typical_test_datasets: dict[str, list[Point]] = {
            "Central and North Scotland": [
                Point(56.5211, -3.8046),
                Point(55.9308, -3.9848),
                Point(55.4245, -3.9132),
                Point(55.6028, -3.202),
                Point(55.6004, -3.2173),
                Point(55.6619, -2.9369),
                Point(55.6595, -2.9522),
                Point(55.6939, -2.9686),
                Point(55.8148, -2.6088),
                Point(55.8125, -2.6241),
                Point(55.8292, -2.6973),
                Point(55.8269, -2.7126),
                Point(55.8549, -2.7803),
                Point(55.8526, -2.7956),
                Point(55.8384, -3.3133),
                Point(55.836, -3.3286),
                Point(55.8787, -3.6042),
                Point(55.9284, -4.0003),
                Point(56.6386, -3.9286),
                Point(56.8258, -2.9982),
                Point(56.9474, -2.8122),
                Point(56.9452, -2.828),
                Point(56.9429, -2.8437),
                Point(56.9595, -4.1717),
                Point(57.4624, -3.5899),
                Point(57.4134, -3.9754),
                Point(55.5164, -2.088),
            ],
            "South Wales": [
                Point(51.6142, -3.1254),
                Point(51.6117, -3.1399),
                Point(51.7621, -3.2507),
                Point(51.7596, -3.2655),
                Point(51.7408, -3.5952),
                Point(51.7496, -3.5996),
                Point(51.7739, -3.4759),
                Point(51.7805, -3.4864),
                Point(51.7861, -3.4615),
                Point(51.1427, -4.1327),
                Point(51.1398, -4.1485),
                Point(51.7209, -4.238),
                Point(51.7496, -4.5499),
                Point(51.6626, -5.0192),
                Point(51.8066, -4.9411),
                Point(51.9654, -4.7578),
                Point(51.9744, -4.7628),
                Point(51.9676, -4.7616),
                Point(52.0173, -4.2),
                Point(52.0129, -4.19),
            ],
            "Devon and Cornwall": [
                Point(50.4252, -4.0251),
                Point(50.4741, -4.3303),
                Point(50.6544, -3.3889),
                Point(50.4169, -4.8064),
                Point(50.7842, -4.4293),
                Point(51.1427, -4.1327),
                Point(52.9948, -4.2152),
                Point(52.9957, -4.2456),
                Point(52.9985, -4.2297),
                Point(52.9868, -4.2414),
                Point(52.9896, -4.2258),
            ],
            "North England": [
                Point(55.4223, -1.7759),
                Point(54.8026, -1.9743),
                Point(54.8929, -2.1792),
                Point(54.8906, -2.1941),
                Point(55.5164, -2.088),
            ],
        }

        all_datasets = {**boundary_test_datasets, **typical_test_datasets}
        for description, test_case in all_datasets.items():
            with self.subTest(description):
                hull_input = HullInput(test_case)
                self.assertEqual(hull_input.points, tuple(test_case))
