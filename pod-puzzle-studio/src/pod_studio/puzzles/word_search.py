"""Word-search puzzle generation.

Pure-Python, no external puzzle libraries.  A puzzle is themed entirely by the
word list you pass in, which is what makes the whole studio niche-agnostic:
swap "SELFCARE, BUBBLEBATH, BOUNDARIES, ..." for any other niche and the same
engine produces a publishable puzzle.
"""

from __future__ import annotations

import random
import string
from dataclasses import dataclass, field

# 8 directions: (dx, dy).  Includes diagonals and reverse for harder grids.
_DIRECTIONS = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (-1, -1), (1, -1), (-1, 1),
]


@dataclass
class Placement:
    word: str
    row: int
    col: int
    dr: int
    dc: int

    def cells(self) -> list[tuple[int, int]]:
        return [(self.row + i * self.dr, self.col + i * self.dc)
                for i in range(len(self.word))]


@dataclass
class WordSearch:
    size: int
    grid: list[list[str]]
    placements: list[Placement]
    words: list[str]
    unplaced: list[str] = field(default_factory=list)


def _normalise(word: str) -> str:
    return "".join(ch for ch in word.upper() if ch.isalpha())


def generate(
    words: list[str],
    *,
    size: int = 15,
    allow_diagonal: bool = True,
    allow_reverse: bool = True,
    seed: int | None = None,
) -> WordSearch:
    """Generate a word-search grid containing as many of ``words`` as fit.

    Words too long for the grid, or that cannot be placed after many attempts,
    are reported in :attr:`WordSearch.unplaced` rather than raising — callers
    can decide whether to shrink the list or grow the grid.
    """
    rng = random.Random(seed)
    clean = []
    seen = set()
    for w in words:
        n = _normalise(w)
        if n and n not in seen and len(n) <= size:
            clean.append(n)
            seen.add(n)
    # Place longest first: they are the hardest to fit.
    clean.sort(key=len, reverse=True)

    dirs = list(_DIRECTIONS)
    if not allow_diagonal:
        dirs = [(dx, dy) for dx, dy in dirs if dx == 0 or dy == 0]
    if not allow_reverse:
        dirs = [(dx, dy) for dx, dy in dirs if (dx, dy) in [(1, 0), (0, 1), (1, 1), (1, -1)]]

    grid: list[list[str | None]] = [[None] * size for _ in range(size)]
    placements: list[Placement] = []
    unplaced: list[str] = []

    def fits(word: str, r: int, c: int, dr: int, dc: int) -> bool:
        for i, ch in enumerate(word):
            rr, cc = r + i * dr, c + i * dc
            if not (0 <= rr < size and 0 <= cc < size):
                return False
            existing = grid[rr][cc]
            if existing is not None and existing != ch:
                return False
        return True

    for word in clean:
        placed = False
        for _ in range(200):  # attempts per word
            dr, dc = rng.choice(dirs)
            r = rng.randrange(size)
            c = rng.randrange(size)
            if fits(word, r, c, dr, dc):
                for i, ch in enumerate(word):
                    grid[r + i * dr][c + i * dc] = ch
                placements.append(Placement(word, r, c, dr, dc))
                placed = True
                break
        if not placed:
            unplaced.append(word)

    # Fill blanks with random letters.
    for r in range(size):
        for c in range(size):
            if grid[r][c] is None:
                grid[r][c] = rng.choice(string.ascii_uppercase)

    return WordSearch(
        size=size,
        grid=[[c for c in row] for row in grid],  # type: ignore[misc]
        placements=placements,
        words=[p.word for p in placements],
        unplaced=unplaced,
    )
