import csv
import os
import random as r
import unittest
from pathlib import Path

from src.parser import Parser

RESOURCES = Path(__file__).resolve().parent.parent / "resources"

parser: Parser = Parser()
random_size = r.randint(0, 100)


class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Initialises large and random files for a test run
        """

        large_file_path: str = RESOURCES / "valid_csv_files" / "large.csv"
        random_file_path: str = RESOURCES / "valid_csv_files" / "random.csv"

        with (
            open(large_file_path, "w") as large_file,
            open(random_file_path, "w") as random_file,
        ):
            large_writer, random_writer = (
                csv.writer(large_file),
                csv.writer(random_file),
            )
            for line in range(600_000):  # 10MB
                large_writer.writerow(
                    [
                        "50",
                        "50",
                        "01/09/2022",
                    ]
                )

            for line in range(random_size):
                long, lat = r.randint(-180, 180), r.randint(-90, 90)
                (
                    day,
                    month,
                    year,
                ) = (r.randint(1, 28), r.randint(1, 12), r.randint(2001, 2025))

                random_writer.writerow([lat, long, f"{day}/{month}/{year}"])

    @classmethod
    def tearDownClass(cls):
        """
        Deletes large file at the end of a test run to save space
        """
        os.remove(RESOURCES / "valid_csv_files" / "large.csv")

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
