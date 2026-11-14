import csv
import random as r
from pathlib import Path

LARGE_FILE_PATH = (
    Path(__file__).resolve().parent.parent
    / "resources"
    / "valid_csv_files"
    / "large.csv"
)


def setup():
    """
    Instantiates the file path for the large CSV, and generates 600,000
    points to be stored using a seeded random.
    """
    rng = r.Random(42)
    with (
        open(LARGE_FILE_PATH, "w") as large_file,
    ):
        large_writer = csv.writer(large_file)
        for line in range(600_000):  # 10MB
            long, lat = rng.randint(-180, 180), rng.randint(-90, 90)

            large_writer.writerow([lat, long])


def teardown():
    """
    Deletes the generated files at the end of a test run, so they
    don't take up space or show up as changes in git.
    """
    LARGE_FILE_PATH.unlink(missing_ok=True)
