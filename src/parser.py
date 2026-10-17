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

        with open(file, "r"):
            try:
                df = pandas.read_csv(
                    file,
                    header=None,
                    names=["x", "y", "date"],
                    # We don't currently have a use for date, but
                    # potentially we will incorporate time series into
                    # the product.
                )

                return tuple(
                    Point(x=row.x, y=row.y)
                    for row in df.itertuples(index=False)
                )

            except Exception as e:
                raise ValueError(f"Failed to parse CSV file: {e}") from e
