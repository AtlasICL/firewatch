import csv
import os
import random as r
from pathlib import Path

RESOURCES = Path(__file__).resolve().parent.parent / "resources"
random_size = r.randint(0, 100)


def setup():

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


def teardown():
    """
    Deletes large file at the end of a test run to save space
    """
    os.remove(RESOURCES / "valid_csv_files" / "large.csv")
