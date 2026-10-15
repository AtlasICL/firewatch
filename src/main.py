from pathlib import Path

from src.parser import Parser
from src.point import HullInput, Point
from src.quickhull import quickhull


def main():

    # Grab the raw data from the csv.
    input_points: tuple[Point, ...] = Parser.parse(
        Path("data/example_coordinates.csv")
    )

    # Transform into HullInput validated type.
    quickhull_input: HullInput = HullInput(input_points)

    # Calculate the convex hull using our quickhull algorithm.
    convex_hull: list[Point] = quickhull(quickhull_input)

    # Print the subset of points making up the convex hull.
    print("Convex hull points:\n")
    for p in convex_hull:
        print(f"x = {p.x}  |  y = {p.y}")


if __name__ == "__main__":
    main()
