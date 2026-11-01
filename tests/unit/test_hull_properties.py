import math
import random
import unittest

from src.point import HullInput, Point
from src.quickhull import quickhull
from tests.hull_checks import HullTestCase


class TestHullMetamorphic(HullTestCase):
    """
    Changes the input in ways that should change the output, and verify
    that we got the expected change in the output.
    (Or change the input in a way that shouldn't change the output, and
    verify that it doesn't).
    """

    """
    Worked example matching the explanatory diagrams in
    `../../img/example_output/`.
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

    def test_spawn_new_point_on_hull_boundary(self):
        """
        Create a convex hull from a given set of points, spawn a new
        point which should sit on the hull's boundary, and ensure that
        it does so after regeneration.
        """
        original_points_with_extra_point = self.points.copy()
        original_points_with_extra_point.append(Point(0.5, -2))
        expected_hull = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
            Point(0.5, -2),
        ]
        self.assert_same_cycle(
            expected_hull,
            quickhull(HullInput(original_points_with_extra_point)),
        )

    def test_spawn_new_point_inside_convex_hull(self):
        """
        Create a convex hull from a given set of points, spawn a new
        point which should sit inside the hull, and ensure that
        the boundary is not impacted by this change.
        """
        original_points_with_extra_point = self.points.copy()
        original_points_with_extra_point.append(Point(-3.5, 3.5))
        self.assert_same_cycle(
            quickhull(HullInput(self.points)),
            quickhull(HullInput(original_points_with_extra_point)),
        )

    def test_move_boundary_point_to_change_hull_sequence(self):
        """
        Create a convex hull from a given set of points, move a
        point on the boundary which should change the order of points on
        the hull, and ensure that this is evident after regeneration.
        """
        new_a = Point(5, 6)
        original_points_with_moved_point = [
            point for point in self.points if point != self.a
        ] + [new_a]
        expected_hull = [
            self.b,
            self.c,
            self.d,
            new_a,
            self.f,
            self.g,
            self.h,
            Point(1, -1),
        ]
        self.assert_same_cycle(
            expected_hull,
            quickhull(HullInput(original_points_with_moved_point)),
        )

    def test_move_boundary_point_to_preserve_hull_sequence(self):
        """
        Create a convex hull from a given set of points, move a
        point on the boundary which should preserve the order of points
        on the hull, and ensure that this is evident after regeneration.
        """
        new_a = Point(0, -2)
        original_points_with_moved_point = [
            point for point in self.points if point != self.a
        ] + [new_a]
        expected_hull = [
            new_a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
        ]
        self.assert_same_cycle(
            expected_hull,
            quickhull(HullInput(original_points_with_moved_point)),
        )

    def test_remove_boundary_point(self):
        """
        Create a convex hull from a given set of points, remove a
        point on the boundary, and ensure that the new convex hull is
        regenerated correctly.
        """
        original_points_with_removed_point = [
            point for point in self.points if point != self.c
        ]
        expected_hull = [
            self.a,
            self.b,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
        ]
        self.assert_same_cycle(
            expected_hull,
            quickhull(HullInput(original_points_with_removed_point)),
        )

    def test_delete_contained_point(self):
        """
        Create a convex hull from a given set of points, remove a
        point contained inside the hull's area, and ensure that the
        convex hull has not changed as a result.
        """
        original_points_with_removed_point = [
            point for point in self.points if point != Point(-1, 4.5)
        ]
        self.assert_same_cycle(
            quickhull(HullInput(self.points)),
            quickhull(HullInput(original_points_with_removed_point)),
        )

    def test_translate_graph(self):
        """
        Create a convex hull from a given set of points, translate the
        entire graph in several variations, and ensure that the convex
        hull cycle does not change with each.
        """
        translated_datasets: dict[str, list[Point]] = {
            "translate only x right": [
                Point(point.x + 10, point.y) for point in self.points
            ],
            "translate only x left": [
                Point(point.x - 10, point.y) for point in self.points
            ],
            "translate only y up": [
                Point(point.x, point.y + 10) for point in self.points
            ],
            "translate only y down": [
                Point(point.x, point.y - 10) for point in self.points
            ],
            "translate x right and y up": [
                Point(point.x + 10, point.y + 10) for point in self.points
            ],
            "translate x right and y down": [
                Point(point.x + 10, point.y - 10) for point in self.points
            ],
            "translate x left and y up": [
                Point(point.x - 10, point.y + 10) for point in self.points
            ],
            "translate x left and y down": [
                Point(point.x - 10, point.y - 10) for point in self.points
            ],
        }
        base_expected_hull = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
        ]
        expected_hulls: dict[str, list[Point]] = {
            "translate only x right": [
                Point(point.x + 10, point.y) for point in base_expected_hull
            ],
            "translate only x left": [
                Point(point.x - 10, point.y) for point in base_expected_hull
            ],
            "translate only y up": [
                Point(point.x, point.y + 10) for point in base_expected_hull
            ],
            "translate only y down": [
                Point(point.x, point.y - 10) for point in base_expected_hull
            ],
            "translate x right and y up": [
                Point(point.x + 10, point.y + 10)
                for point in base_expected_hull
            ],
            "translate x right and y down": [
                Point(point.x + 10, point.y - 10)
                for point in base_expected_hull
            ],
            "translate x left and y up": [
                Point(point.x - 10, point.y + 10)
                for point in base_expected_hull
            ],
            "translate x left and y down": [
                Point(point.x - 10, point.y - 10)
                for point in base_expected_hull
            ],
        }
        for description, translated_points in translated_datasets.items():
            with self.subTest(translation=description):
                self.assert_same_cycle(
                    expected_hulls[description],
                    quickhull(HullInput(translated_points)),
                )

    def test_reflect_graph(self):
        """
        Create a convex hull from a given set of points, reflect the
        entire graph in several variations, and ensure that the convex
        hull cycle does not change with each.
        """
        reflected_datasets: dict[str, list[Point]] = {
            "reflect in x": [
                Point(point.x * -1, point.y) for point in self.points
            ],
            "reflect in y": [
                Point(point.x, point.y * -1) for point in self.points
            ],
            "reflect in x and y": [
                Point(point.x * -1, point.y * -1) for point in self.points
            ],
        }
        base_expected_hull = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
        ]
        expected_hulls: dict[str, list[Point]] = {
            "reflect in x": [
                Point(point.x * -1, point.y) for point in base_expected_hull
            ],
            "reflect in y": [
                Point(point.x, point.y * -1) for point in base_expected_hull
            ],
            "reflect in x and y": [
                Point(point.x * -1, point.y * -1)
                for point in base_expected_hull
            ],
        }
        for description, reflected_points in reflected_datasets.items():
            with self.subTest(translation=description):
                self.assert_same_cycle(
                    expected_hulls[description],
                    quickhull(HullInput(reflected_points)),
                )

    def test_scale_graph(self):
        """
        Create a convex hull from a given set of points, scale the
        entire graph in several variations, and ensure that the convex
        hull cycle does not change with each.
        """
        scaled_datasets: dict[str, list[Point]] = {
            "scale only x up": [
                Point(point.x * 2, point.y) for point in self.points
            ],
            "scale only x down": [
                Point(point.x * 0.5, point.y) for point in self.points
            ],
            "scale only y up": [
                Point(point.x, point.y * 2) for point in self.points
            ],
            "scale only y down": [
                Point(point.x, point.y * 0.5) for point in self.points
            ],
            "scale x up and y up": [
                Point(point.x * 2, point.y * 2) for point in self.points
            ],
            "scale x up and y down": [
                Point(point.x * 2, point.y * 0.5) for point in self.points
            ],
            "scale x down and y up": [
                Point(point.x * 0.5, point.y * 2) for point in self.points
            ],
            "scale x down and y down": [
                Point(point.x * 0.5, point.y * 0.5) for point in self.points
            ],
        }
        base_expected_hull = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
        ]
        expected_hulls: dict[str, list[Point]] = {
            "scale only x up": [
                Point(point.x * 2, point.y) for point in base_expected_hull
            ],
            "scale only x down": [
                Point(point.x * 0.5, point.y) for point in base_expected_hull
            ],
            "scale only y up": [
                Point(point.x, point.y * 2) for point in base_expected_hull
            ],
            "scale only y down": [
                Point(point.x, point.y * 0.5) for point in base_expected_hull
            ],
            "scale x up and y up": [
                Point(point.x * 2, point.y * 2) for point in base_expected_hull
            ],
            "scale x up and y down": [
                Point(point.x * 2, point.y * 0.5)
                for point in base_expected_hull
            ],
            "scale x down and y up": [
                Point(point.x * 0.5, point.y * 2)
                for point in base_expected_hull
            ],
            "scale x down and y down": [
                Point(point.x * 0.5, point.y * 0.5)
                for point in base_expected_hull
            ],
        }
        for description, scaled_points in scaled_datasets.items():
            with self.subTest(translation=description):
                self.assert_same_cycle(
                    expected_hulls[description],
                    quickhull(HullInput(scaled_points)),
                )

    def test_rotate_graph(self):
        """
        Create a convex hull from a given set of points, rotate the
        entire graph 90 degrees, and ensure that the convex hull cycle
        has not changed as a result.
        """
        rotated_points = [
            Point(
                point.x * math.cos(0) + point.y * math.sin(0),
                point.y * math.cos(0) - point.x * math.sin(0),
            )
            for point in self.points
        ]
        expected_hull = [
            Point(
                self.a.x * math.cos(0) + self.a.y * math.sin(0),
                self.a.y * math.cos(0) - self.a.x * math.sin(0),
            ),
            Point(
                self.b.x * math.cos(0) + self.b.y * math.sin(0),
                self.b.y * math.cos(0) - self.b.x * math.sin(0),
            ),
            Point(
                self.c.x * math.cos(0) + self.c.y * math.sin(0),
                self.c.y * math.cos(0) - self.c.x * math.sin(0),
            ),
            Point(
                self.d.x * math.cos(0) + self.d.y * math.sin(0),
                self.d.y * math.cos(0) - self.d.x * math.sin(0),
            ),
            Point(
                self.e.x * math.cos(0) + self.e.y * math.sin(0),
                self.e.y * math.cos(0) - self.e.x * math.sin(0),
            ),
            Point(
                self.f.x * math.cos(0) + self.f.y * math.sin(0),
                self.f.y * math.cos(0) - self.f.x * math.sin(0),
            ),
            Point(
                self.g.x * math.cos(0) + self.g.y * math.sin(0),
                self.g.y * math.cos(0) - self.g.x * math.sin(0),
            ),
            Point(
                self.h.x * math.cos(0) + self.h.y * math.sin(0),
                self.h.y * math.cos(0) - self.h.x * math.sin(0),
            ),
        ]
        self.assert_same_cycle(
            expected_hull,
            quickhull(HullInput(rotated_points)),
        )

    def test_shuffling_hull_input_returns_same_convex_hull_sequence(self):
        """
        Create a convex hull from a given set of points, use the
        Fisher-Yates shuffling algorithm to re-order the list of points,
        and ensure that the convex hull has not changed as a result.
        """
        original_points_shuffled = self.points.copy()
        for i in range(len(original_points_shuffled) - 1, 0, -1):
            j = random.randint(0, i)
            original_points_shuffled[i], original_points_shuffled[j] = (
                original_points_shuffled[j],
                original_points_shuffled[i],
            )
        self.assert_same_cycle(
            quickhull(HullInput(self.points)),
            quickhull(HullInput(original_points_shuffled)),
        )


if __name__ == "__main__":
    unittest.main()
