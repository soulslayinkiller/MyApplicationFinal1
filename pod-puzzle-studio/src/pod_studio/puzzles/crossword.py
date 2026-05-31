"""Criss-cross / interlocking crossword generation.

This is the "fill-in" style crossword common in activity books: words are
placed so they interlock at shared letters, then numbered clues are produced
for Across and Down.  It is greedy (place longest words first, intersect where
possible) which is fast and reliably produces a connected grid, though not a
symmetric NYT-style grid.

Input is a list of (answer, clue) pairs so the same engine themes to any niche.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Entry:
    answer: str
    clue: str
    row: int
    col: int
    horizontal: bool
    number: int = 0

    def cells(self) -> list[tuple[int, int]]:
        return [
            (self.row + (0 if self.horizontal else i),
             self.col + (i if self.horizontal else 0))
            for i in range(len(self.answer))
        ]


@dataclass
class Crossword:
    grid: dict[tuple[int, int], str]  # (row, col) -> letter
    entries: list[Entry]
    rows: int
    cols: int
    min_row: int
    min_col: int
    placed: list[str] = field(default_factory=list)
    unplaced: list[str] = field(default_factory=list)


def _normalise(answer: str) -> str:
    return "".join(ch for ch in answer.upper() if ch.isalpha())


def generate(pairs: list[tuple[str, str]]) -> Crossword:
    """Build an interlocking crossword from (answer, clue) pairs."""
    cleaned = []
    seen = set()
    for answer, clue in pairs:
        a = _normalise(answer)
        if a and a not in seen and len(a) >= 2:
            cleaned.append((a, clue))
            seen.add(a)
    cleaned.sort(key=lambda p: len(p[0]), reverse=True)

    grid: dict[tuple[int, int], str] = {}
    entries: list[Entry] = []
    unplaced: list[str] = []

    def can_place(word: str, row: int, col: int, horizontal: bool) -> int | None:
        """Return an intersection score if placeable, else None.

        Enforces that new letters don't collide and that we don't accidentally
        run words together side-by-side (basic adjacency rules).
        """
        score = 0
        for i, ch in enumerate(word):
            r = row + (0 if horizontal else i)
            c = col + (i if horizontal else 0)
            cur = grid.get((r, c))
            if cur is not None:
                if cur != ch:
                    return None
                score += 1  # a real crossing
            else:
                # The cell must be empty AND its perpendicular neighbours empty,
                # otherwise we create an unintended adjacent word.
                if horizontal:
                    if grid.get((r - 1, c)) or grid.get((r + 1, c)):
                        return None
                else:
                    if grid.get((r, c - 1)) or grid.get((r, c + 1)):
                        return None
        # Ends must not butt directly against another letter.
        before = (row, col - 1) if horizontal else (row - 1, col)
        after = (
            (row, col + len(word)) if horizontal else (row + len(word), col)
        )
        if grid.get(before) or grid.get(after):
            return None
        return score

    # Place the first (longest) word at the origin, horizontal.
    if not cleaned:
        return Crossword({}, [], 0, 0, 0, 0)
    first_answer, first_clue = cleaned[0]
    for i, ch in enumerate(first_answer):
        grid[(0, i)] = ch
    entries.append(Entry(first_answer, first_clue, 0, 0, True))

    for answer, clue in cleaned[1:]:
        best: tuple[int, int, int, bool] | None = None  # score, row, col, horiz
        # Try to intersect with every placed letter.
        for i, ch in enumerate(answer):
            for (gr, gc), gch in list(grid.items()):
                if gch != ch:
                    continue
                # Place vertically so it crosses a horizontal cell (and v.v.).
                # Vertical placement: word runs down, crossing at (gr, gc).
                row, col, horizontal = gr - i, gc, False
                s = can_place(answer, row, col, horizontal)
                if s and (best is None or s > best[0]):
                    best = (s, row, col, horizontal)
                # Horizontal placement crossing a vertical cell.
                row, col, horizontal = gr, gc - i, True
                s = can_place(answer, row, col, horizontal)
                if s and (best is None or s > best[0]):
                    best = (s, row, col, horizontal)
        if best is None:
            unplaced.append(answer)
            continue
        _, row, col, horizontal = best
        for i, ch in enumerate(answer):
            r = row + (0 if horizontal else i)
            c = col + (i if horizontal else 0)
            grid[(r, c)] = ch
        entries.append(Entry(answer, clue, row, col, horizontal))

    # Normalise coordinates to start at 0,0 and number the entries.
    rows_ = [r for r, _ in grid]
    cols_ = [c for _, c in grid]
    min_r, min_c = min(rows_), min(cols_)
    shifted: dict[tuple[int, int], str] = {}
    for (r, c), ch in grid.items():
        shifted[(r - min_r, c - min_c)] = ch
    for e in entries:
        e.row -= min_r
        e.col -= min_c

    # Number cells: a cell gets a number if it starts an across and/or down word.
    starts = sorted({(e.row, e.col) for e in entries})
    numbering = {cell: n + 1 for n, cell in enumerate(starts)}
    for e in entries:
        e.number = numbering[(e.row, e.col)]

    height = max(r for r, _ in shifted) + 1
    width = max(c for _, c in shifted) + 1
    return Crossword(
        grid=shifted,
        entries=sorted(entries, key=lambda e: (e.number, not e.horizontal)),
        rows=height,
        cols=width,
        min_row=0,
        min_col=0,
        placed=[e.answer for e in entries],
        unplaced=unplaced,
    )
