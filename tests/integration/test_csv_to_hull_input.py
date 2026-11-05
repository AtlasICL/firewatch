import unittest
from pathlib import Path

from src.parser import Parser
from src.point import HullInput

RESOURCES = Path(__file__).resolve().parent.parent / "resources"

parser: Parser = Parser()
valid_files: Path = RESOURCES / "valid_csv_files"
out_of_bounds_files: Path = RESOURCES / "out_of_bounds_csv_files"


class TestCsvToHullInput(unittest.TestCase):
    def test_hull_input_rejects_less_than_two_points_for_valid_csv(self):
        """
        Although a CSV file with less than two distinct points may be of
        valid format, it should be rejected by HullInput.
        """
        expected_outputs: dict[str, int] = {
            "empty.csv": 0,
            "single_point.csv": 1,
        }
        for name, expected_length in expected_outputs.items():
            with self.subTest(file=name):
                path = valid_files / name
                with self.assertRaises(ValueError):
                    HullInput(parser.parse(path)).points

    def test_hull_input_is_of_correct_length_for_valid_csv_files(self):
        """
        The HullInput iterable should be of length x, where x is the
        number of lines in the CSV file.
        """
        expected_outputs: dict[str, int] = {
            "min_size.csv": 2,
            "missing_dates.csv": 7,
            "normal.csv": 7,
            "normal_bigger.csv": 14,
            "skip_line.csv": 7,
            "triangle.csv": 3,
        }
        for name, expected_length in expected_outputs.items():
            with self.subTest(file=name):
                path = valid_files / name
                self.assertEqual(
                    expected_length, len(HullInput(parser.parse(path)).points)
                )

    def test_hull_input_rejects_less_than_two_points_for_boundary_csv(self):
        """
        Although a CSV file may contain two or more distinct points, it
        should be rejected by HullInput if there are less than two
        distinct points of a valid format.
        """
        expected_outputs: dict[str, int] = {
            "all_lines_invalid.csv": 0,
        }
        for name, expected_length in expected_outputs.items():
            with self.subTest(file=name):
                path = out_of_bounds_files / name
                with self.assertRaises(ValueError):
                    HullInput(parser.parse(path)).points

    def test_hull_input_is_of_correct_length_for_boundary_csv_files(self):
        """
        The HullInput iterable should be of length x, where x is the
        number of valid format lines in the CSV file. Lines of an
        invalid format should be ignored.
        """
        expected_outputs: dict[str, int] = {
            "invalid_date.csv": 5,
            "invalid_latitude.csv": 5,
            "invalid_longitude.csv": 5,
            "multiple_invalid.csv": 3,
        }
        for name, expected_length in expected_outputs.items():
            with self.subTest(file=name):
                path = out_of_bounds_files / name
                self.assertEqual(
                    expected_length, len(HullInput(parser.parse(path)).points)
                )
