import unittest
from pathlib import Path

from src.parser import Parser
from tests.unit.setup import random_size

RESOURCES = Path(__file__).resolve().parent.parent / "resources"

parser: Parser = Parser()


class TestParser(unittest.TestCase):
    def test_exception_thrown_if_csv_is_rejected(self):
        """
        ValueError should be thrown when the dataset .csv file is
        rejected for any reason.
        """
        for file in sorted((RESOURCES / "invalid_csv_files").iterdir()):
            with self.subTest(file=file.name), self.assertRaises(ValueError):
                parser.parse(file)

    def test_correct_total_of_points_generated_from_dataset(self):
        """
        After parsing, the total Point objects in HullInput should
        equal to the total records in the dataset.
        """
        expected_counts: dict[str, int] = {
            "empty.csv": 0,
            "min_size.csv": 2,
            "missing_dates.csv": 7,
            "normal.csv": 7,
            "normal_bigger.csv": 14,
            "single_point.csv": 1,
            "skip_line.csv": 7,
            "triangle.csv": 3,
            "large.csv": 600_000,
            "random.csv": random_size,
        }
        valid_files: Path = RESOURCES / "valid_csv_files"

        for name, expected in expected_counts.items():
            with self.subTest(file=name):
                path = valid_files / name
                self.assertEqual(expected, len(parser.parse(path)))

    def test_ignores_out_of_bounds_lines(self):
        """
        Should accept files with out of bounds data,
        but ignore the lines on which they occur
        """
        expected_counts: dict[str, int] = {
            "all_lines_invalid.csv": 0,
            "invalid_date.csv": 5,
            "invalid_latitude.csv": 5,
            "invalid_longitude.csv": 5,
            "multiple_invalid.csv": 3,
        }
        out_of_bounds_files: Path = RESOURCES / "out_of_bounds_csv_files"

        for name, expected in expected_counts.items():
            with self.subTest(file=name):
                path = out_of_bounds_files / name
                self.assertEqual(expected, len(parser.parse(path)))
