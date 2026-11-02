import unittest

from src.parser import Parser
from src.point import HullInput
from src.quickhull import quickhull
from tests.hull_checks import HullTestCase
from tests.unit.setup import LARGE_FILE_PATH, setup, teardown


def setUpModule():
    """
    Setup function provided by unittest allows our setup logic to be
    run before any tests in this file are executed.
    """
    setup()


def tearDownModule():
    """
    Teardown function provided by unittest allows our teardown logic to
    be run after all tests in this file have completed.
    """
    teardown()


class TestHullScale(HullTestCase):
    def test_algorithm_remains_functional_under_large_seeded_load(self):
        """
        Ensures that the quickhull algorithm can process an input size
        of 600,000 seeded random points.
        If the assertion returns true, then no exception was thrown by
        the algorithm under the input load.
        """
        input_points = Parser.parse(LARGE_FILE_PATH)
        self.assertIsNotNone(quickhull(HullInput(input_points)))


if __name__ == "__main__":
    unittest.main()
