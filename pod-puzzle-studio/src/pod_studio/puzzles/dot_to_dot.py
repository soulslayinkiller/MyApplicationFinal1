"""Dot-to-dot (connect-the-dots) generation.

Aimed at the kids 3-5 activity-book niche: low dot counts (counting practice),
big clear numbers, simple recognizable shapes.  A shape is just an ordered list
of (x, y) points in a 0..1 unit square; the renderer scales it to the page,
drops a numbered dot at each point, and (optionally) shows faint guide lines.

Shapes are data, so adding "rocket", "puppy", etc. is a dict entry, not code.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DotToDot:
    name: str
    points: list[tuple[float, float]]  # ordered, unit square (0..1)
    closed: bool = True                # connect last dot back to first


# A small starter library of toddler-friendly shapes.  Points are listed in the
# order a child connects them.  Kept low-count (<= ~16) for ages 3-5.
SHAPES: dict[str, DotToDot] = {
    "star": DotToDot(
        "Star",
        [
            (0.50, 0.95), (0.61, 0.62), (0.95, 0.62), (0.68, 0.40),
            (0.79, 0.07), (0.50, 0.28), (0.21, 0.07), (0.32, 0.40),
            (0.05, 0.62), (0.39, 0.62),
        ],
    ),
    "house": DotToDot(
        "House",
        [
            (0.20, 0.05), (0.80, 0.05), (0.80, 0.55), (0.90, 0.55),
            (0.50, 0.90), (0.10, 0.55), (0.20, 0.55),
        ],
    ),
    "truck": DotToDot(
        "Dump Truck",
        [
            (0.08, 0.25), (0.55, 0.25), (0.58, 0.50), (0.72, 0.50),
            (0.80, 0.32), (0.92, 0.32), (0.92, 0.25), (0.95, 0.25),
            (0.95, 0.12), (0.08, 0.12),
        ],
        closed=True,
    ),
    "boat": DotToDot(
        "Sailboat",
        [
            (0.15, 0.30), (0.85, 0.30), (0.70, 0.15), (0.30, 0.15),
            (0.15, 0.30), (0.50, 0.30), (0.50, 0.90), (0.85, 0.45),
            (0.50, 0.45),
        ],
        closed=False,
    ),
    "fish": DotToDot(
        "Fish",
        [
            (0.20, 0.50), (0.45, 0.72), (0.70, 0.60), (0.85, 0.72),
            (0.80, 0.50), (0.85, 0.28), (0.70, 0.40), (0.45, 0.28),
        ],
    ),
    "heart": DotToDot(
        "Heart",
        [
            (0.50, 0.25), (0.18, 0.55), (0.20, 0.78), (0.38, 0.85),
            (0.50, 0.72), (0.62, 0.85), (0.80, 0.78), (0.82, 0.55),
        ],
    ),
}


def get(name: str) -> DotToDot:
    if name not in SHAPES:
        raise ValueError(f"Unknown shape {name!r}. Known: {', '.join(SHAPES)}")
    return SHAPES[name]


def by_index(i: int) -> DotToDot:
    """Cycle through the shape library by index (for filling a section)."""
    keys = list(SHAPES)
    return SHAPES[keys[i % len(keys)]]
