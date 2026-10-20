import unittest
from time import perf_counter

from scipy.spatial import ConvexHull

from src.point import HullInput, Point
from src.quickhull import quickhull
from tests.hull_checks import HullTestCase


def points_to_tuple(points: list[Point]):
    return list(map(lambda p: (p.x, p.y), points))


class TestHullKnownCases(HullTestCase):
    def test_performance_comparison_on_large_input_size(self):
        input_points: tuple[Point, ...] = []
        for x in range(100):
            for y in range(100):
                input_points.append(Point(x, y))

        start_ours = perf_counter()
        quickhull(HullInput(input_points))
        end_ours = perf_counter()
        our_time = end_ours - start_ours

        start_theirs = perf_counter()
        ConvexHull(points_to_tuple(input_points))
        end_theirs = perf_counter()
        their_time = end_theirs - start_theirs

        faster = "Our" if our_time > their_time else "their"
        print(f"Our Performance: {our_time}, SciPy Performance: {their_time}")
        print(f"{faster} hull was faster by {abs(our_time - their_time)}")


if __name__ == "__main__":
    unittest.main()
