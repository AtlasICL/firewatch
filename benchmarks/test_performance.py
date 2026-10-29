import random as r

import unittest
from benchmarks.benchmark_timing import benchmark

from scipy.spatial import ConvexHull

from src.point import HullInput, Point
from src.quickhull import quickhull


def points_to_tuple(points: list[Point]):
    return list(map(lambda p: (p.x, p.y), points))


class TestPerformance(unittest.TestCase):
    def test_our_performance_on_average_input_size(self):
        input_points: tuple[Point, ...] = []
        for x in range(10):
            for y in range(10):
                input_points.append(Point(x, y))

        tuple_input = points_to_tuple(input_points)
        benchmark(ConvexHull, tuple_input)

    def test_scipy_performance_on_average_input_size(self):
        input_points: tuple[Point, ...] = []
        for x in range(10):
            for y in range(10):
                input_points.append(Point(x, y))

        hull_input = HullInput(input_points)
        benchmark(quickhull, hull_input)


    def test_our_performance_on_large_input_size(self):
        input_points: tuple[Point, ...] = []
        for x in range(100):
            for y in range(100):
                input_points.append(Point(x, y))

        tuple_input = points_to_tuple(input_points)
        benchmark(ConvexHull, tuple_input)


    def test_scipy_performance_on_large_input_size(self):
        input_points: tuple[Point, ...] = []
        for x in range(100):
            for y in range(100):
                input_points.append(Point(x, y))

        hull_input = HullInput(input_points)
        benchmark(quickhull, hull_input)


    def test_our_performance_on_random_inputs(self):
        input_points: tuple[Point, ...] = []
        for p in range(100):
            x, y = r.randint(-180, 180), r.randint(-90, 90)
            input_points.append(Point(x, y))

        tuple_input = points_to_tuple(input_points)
        benchmark(ConvexHull, tuple_input)


    def test_scipy_performance_on_random_inputs(self):
        input_points: tuple[Point, ...] = []
        for p in range(100):
            x, y = r.randint(-90, 90), r.randint(-180, 180)
            input_points.append(Point(x, y))

        hull_input = HullInput(input_points)
        benchmark(quickhull, hull_input)
