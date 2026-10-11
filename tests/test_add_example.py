import unittest

from src.main import add


class TestAdd(unittest.TestCase):
    """Example test case."""

    def test_add_works_on_positive_ints(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_works_on_negative_ints(self):
        self.assertEqual(add(-2, -3), -5)


if __name__ == "__main__":
    unittest.main()
