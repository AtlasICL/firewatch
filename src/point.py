from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Point:
    """Represents a given point with its `x` and `y` coordinates."""

    x: float
    y: float

    def __init__(self, x=None, y=None):
        if x is None or y is None:
            raise ValueError("Requires an x and y value")

        if not (isinstance(x, float) or isinstance(x, int)) or not (
            isinstance(y, float) or isinstance(y, int)
        ):
            raise ValueError("x and y must be numerical")

        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)


@dataclass(frozen=True, slots=True)
class HullInput:
    """Represents an iterable of at least 2 distinct `Point` objects."""

    points: tuple[Point, ...]

    def __init__(self, points: Iterable[Point]):

        points = tuple(points)
        try:
            if len(set(points)) < 2:
                raise ValueError("At least 2 distinct points required")
        except AttributeError:
            raise ValueError("Invalid set of points")

        object.__setattr__(self, "points", points)
