from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Point:
    """Represents a given point with its `x` and `y` coordinates."""

    x: float
    y: float

    def __post_init__(self):
        for name, value in (("x", self.x), ("y", self.y)):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be numerical")


@dataclass(frozen=True, slots=True)
class HullInput:
    """Represents an iterable of at least 2 distinct `Point` objects."""

    points: tuple[Point, ...]

    def __init__(self, points: Iterable[Point]):

        points = tuple(points)
        if len(set(points)) < 2:
            raise ValueError("At least 2 distinct points required")

        object.__setattr__(self, "points", points)
