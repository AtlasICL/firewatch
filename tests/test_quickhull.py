import unittest

class TestQuickhull(unittest.TestCase):

    def test_minimum_three_coordinates_required(self):
        """
        Unit test to verify that a minimum of three coordinates are
        required to form a convex hull.
        If the coordinate total is less than 3, the appropriate
        exception should be thrown.
        """
        # TO DO

    def test_minimum_x_is_furthest_west_point(self):
        """
        Unit test to verify that the point min_x chosen by the
        algorithm is the coordinate that lies furthest west.
        """
        # TO DO

    def test_maximum_x_is_furthest_east_point(self):
        """
        Unit test to verify that the point max_x chosen by the
        algorithm is the coordinate that lies furthest east.
        """
        # TO DO

    def test_p_is_furthest_point_from_minmax_line(self):
        """
        Unit test to verify that the point p chosen by the
        algorithm is the coordinate that lies furthest from the
        straight line formed between min_x and max_x.
        """
        # TO DO

    def test_all_coordinates_lie_in_convex_hull_boundary(self):
        """
        Unit test to verify that all coordinates lie either within the
        convex hull, or on its boundary.
        """
        # TO DO                


if __name__ == "__main__":
    unittest.main()
