import os
import unittest

from src.parser import Parser

parser: Parser = Parser()


class TestParser(unittest.TestCase):
    def test_exception_thrown_if_csv_is_rejected(self):
        """
        ValueError should be thrown when the dataset .csv file is
        rejected for any reason.
        """
        invalid_files = os.path.join(
            os.getcwd(), "tests", "resources", "invalid csv files"
        )
        with os.scandir(invalid_files) as scan_dir:
            for file in scan_dir:
                with self.assertRaises(ValueError):
                    print(parser.parse(file))
                    parser.parse(file)

    def test_correct_total_of_points_generated_from_dataset(self):
        """
        After parsing, the total Point objects in HullInput should
        equal to the total records in the dataset.
        """
        expected_outputs = [2, 1, 7, 0, 3, 7, 7, 14]
        valid_files = os.path.join(
            os.getcwd(), "tests", "resources", "valid csv files"
        )

        with os.scandir(valid_files) as scan_dir:
            for expected, file in zip(expected_outputs, scan_dir):
                self.assertEqual(expected, len(parser.parse(file)))
