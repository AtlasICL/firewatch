import csv
import random as r
from pathlib import Path

RESOURCES = Path(__file__).resolve().parent.parent / "resources"
LARGE_FILE_PATH: Path = RESOURCES / "valid_csv_files" / "large.csv"
RANDOM_FILE_PATH: Path = RESOURCES / "valid_csv_files" / "random.csv"
random_size = r.randint(0, 100)


def setup():
    with (
        open(LARGE_FILE_PATH, "w") as large_file,
        open(RANDOM_FILE_PATH, "w") as random_file,
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


def teardown():
    """
    Deletes the generated files at the end of a test run, so they
    don't take up space or show up as changes in git.
    """
    LARGE_FILE_PATH.unlink(missing_ok=True)
    RANDOM_FILE_PATH.unlink(missing_ok=True)
