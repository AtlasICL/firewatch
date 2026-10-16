import unittest

from tests.resources.hull_checks import HullTestCase


class TestHullScale(HullTestCase):
    """
    Checks quickhull copes with large inputs. Keep the sizes modest so
    `just test` stays fast.
    """

    def test_with_large_seeded_random_input(self):
        self.skipTest("TODO")

    def test_with_huge_input_size(self):
        self.skipTest("TODO")


if __name__ == "__main__":
    unittest.main()
