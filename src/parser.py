import csv
from datetime import datetime as dt
from pathlib import Path

from src.point import Point


class Parser:
    """Responsible for parsing csv fire data."""

    @staticmethod
    def parse(file: Path) -> tuple[Point, ...]:
        """
        Parses the given csv file, and returns a tuple of `Point`
        objects parsed from the data.

        Args:
            file: file to parse

        Returns:
            Tuple of `Point` objects parsed from the file.

        Throws:
            ValueError if the file was not able to be parsed for any
            reason.
        """
        try:
            with open(file, mode="r", encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
                return tuple(
                    # Expect row[0] = latitude, row[1] = longitude
                    Point(x=float(row[0]), y=float(row[1]))
                    for row in reader
                    if row
                    and (  # Latitude
                        float(row[0]) <= 90 and float(row[0]) >= -90
                    )
                    and (  # Longitude
                        float(row[1]) <= 180 and float(row[1]) >= -180
                    )
                    and (
                        len(row) < 3
                        or (
                            (  # Date format: dd/mm/yyyy
                                dt.strptime(row[2], "%d/%m/%Y")
                                >= dt(2000, 10, 1)
                            )
                            and (dt.strptime(row[2], "%d/%m/%Y") <= dt.now())
                        )
                    )
                )
        except Exception as e:
            raise ValueError(f"Failed to parse CSV file: {e}")
