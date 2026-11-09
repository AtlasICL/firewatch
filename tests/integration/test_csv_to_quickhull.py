from pathlib import Path

from src.parser import Parser
from src.point import HullInput, Point
from src.quickhull import quickhull
from tests.hull_checks import HullTestCase

RESOURCES = Path(__file__).resolve().parent.parent / "resources"

parser: Parser = Parser()
valid_files: Path = RESOURCES / "valid_csv_files"
out_of_bounds_files: Path = RESOURCES / "out_of_bounds_csv_files"


class TestCsvToQuickhull(HullTestCase):
    def test_quickhull_calculated_correctly_for_valid_csv_files(self):
        """
        The quickhull for a set of points in a valid CSV file should be
        calculated correctly.
        """
        expected_outputs: dict[str, list[Point]] = {
            "min_size.csv": [Point(54.3561, -0.5948), Point(54.3657, -0.6007)],
            "normal.csv": [
                Point(51.5212, -3.6538),
                Point(51.5231, -3.6689),
                Point(54.8854, -6.7712),
                Point(55.5915, -3.6387),
                Point(53.5690, -0.5875),
            ],
            "skip_line.csv": [
                Point(51.5212, -3.6538),
                Point(51.5231, -3.6689),
                Point(54.8854, -6.7712),
                Point(55.5915, -3.6387),
                Point(53.5690, -0.5875),
            ],
            "triangle.csv": [
                Point(53.9952, -0.3921),
                Point(53.9859, -0.3971),
                Point(53.9485, -0.4172),
            ],
        }
        for name, expected_quickhull in expected_outputs.items():
            with self.subTest(file=name):
                path = valid_files / name
                self.assert_same_cycle(
                    expected_quickhull,
                    quickhull(HullInput(parser.parse(path))),
                )

    def test_quickhull_calculated_correctly_for_boundary_csv_files(self):
        """
        The quickhull for a set of points in a CSV file containing data
        of valid and invalid formats should be calculated correctly for
        the data of a valid format.
        """
        expected_outputs: dict[str, int] = {
            "invalid_latitude.csv": [
                Point(51.5212, -3.6538),
                Point(51.5231, -3.6689),
                Point(54.8854, -6.7712),
                Point(55.5915, -3.6387),
                Point(53.5708, -0.6045),
            ],
            "invalid_longitude.csv": [
                Point(51.5212, -3.6538),
                Point(55.5915, -3.6387),
                Point(53.5690, -0.5875),
            ],
            "multiple_invalid.csv": [
                Point(51.5231, -3.6689),
                Point(53.5676, -0.5981),
                Point(53.5690, -0.5875),
            ],
        }
        for name, expected_quickhull in expected_outputs.items():
            with self.subTest(file=name):
                path = out_of_bounds_files / name
                self.assert_same_cycle(
                    expected_quickhull,
                    quickhull(HullInput(parser.parse(path))),
                )
