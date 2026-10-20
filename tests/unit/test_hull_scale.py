import random
import unittest

from src.point import HullInput, Point
from src.quickhull import quickhull
from tests.hull_checks import HullTestCase


class TestHullScale(HullTestCase):
    """
    Checks quickhull copes with large inputs. Keep the sizes modest so
    `just test` stays fast.
    """

    # NOTE: Modify to process input from CSV file once JW commits.
    def test_with_large_seeded_random_input(self):
        """
        Ensures that the quickhull algorithm can process an input size
        of 1000 seeded random points.
        """
        input_points: tuple[Point, ...] = []
        random.seed(42)
        for _ in range(1000):
            input_points.append(
                Point(random.randint(0, 100), random.randint(0, 100))
            )
        quickhull_input: HullInput = HullInput(input_points)
        convex_hull: list[Point] = quickhull(quickhull_input)
        HullTestCase.assert_is_convex_hull_of(self, input_points, convex_hull)

    # NOTE: Modify to process input from CSV file once JW commits.
    def test_with_huge_input_size(self):
        """
        Ensures that the quickhull algorithm can process an input size
        of 10,000 non-random points.
        """
        input_points: tuple[Point, ...] = []
        for x in range(100):
            for y in range(100):
                input_points.append(Point(x, y))
        quickhull_input: HullInput = HullInput(input_points)
        convex_hull: list[Point] = quickhull(quickhull_input)
        HullTestCase.assert_is_convex_hull_of(self, input_points, convex_hull)


if __name__ == "__main__":
    unittest.main()
