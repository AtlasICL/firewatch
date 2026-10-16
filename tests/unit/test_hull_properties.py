import unittest

from tests.resources.hull_checks import HullTestCase


class TestHullMetamorphic(HullTestCase):
    """
    Changes the input in ways that should change the output, and verify
    that we got the expected change in the output.
    (Or change the input in a way that shouldn't change the output, and
    verify that it doesn't).
    """

    pass


class TestHullAgainstReference(HullTestCase):
    """Compares quickhull with an external convex hull algorithm."""

    pass


if __name__ == "__main__":
    unittest.main()
