"""Sudoku generation with a guaranteed-unique solution.

Builds a full valid grid by randomised backtracking, then removes clues while
verifying the puzzle still has exactly one solution.  Difficulty is controlled
by how many clues we try to remove.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

Grid = list[list[int]]  # 0 == empty

DIFFICULTY_CLUES = {
    "easy": 40,
    "medium": 32,
    "hard": 26,
    "expert": 22,
}


@dataclass
class Sudoku:
    puzzle: Grid
    solution: Grid
    difficulty: str


def _full_solution(rng: random.Random) -> Grid:
    grid = [[0] * 9 for _ in range(9)]

    def candidates(r: int, c: int) -> list[int]:
        used = set(grid[r])
        used |= {grid[i][c] for i in range(9)}
        br, bc = 3 * (r // 3), 3 * (c // 3)
        used |= {grid[br + i][bc + j] for i in range(3) for j in range(3)}
        return [n for n in range(1, 10) if n not in used]

    def fill(pos: int) -> bool:
        if pos == 81:
            return True
        r, c = divmod(pos, 9)
        nums = candidates(r, c)
        rng.shuffle(nums)
        for n in nums:
            grid[r][c] = n
            if fill(pos + 1):
                return True
            grid[r][c] = 0
        return False

    fill(0)
    return grid


def _count_solutions(grid: Grid, limit: int = 2) -> int:
    """Count solutions up to ``limit`` (we only need to know if it's >1)."""
    # Find the empty cell with fewest candidates (constraint propagation-ish).
    best = None
    best_cands: list[int] | None = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                continue
            used = set(grid[r]) | {grid[i][c] for i in range(9)}
            br, bc = 3 * (r // 3), 3 * (c // 3)
            used |= {grid[br + i][bc + j] for i in range(3) for j in range(3)}
            cands = [n for n in range(1, 10) if n not in used]
            if not cands:
                return 0
            if best_cands is None or len(cands) < len(best_cands):
                best, best_cands = (r, c), cands
    if best is None:
        return 1  # no empties -> solved
    r, c = best
    total = 0
    for n in best_cands:  # type: ignore[union-attr]
        grid[r][c] = n
        total += _count_solutions(grid, limit)
        grid[r][c] = 0
        if total >= limit:
            return total
    return total


def generate(difficulty: str = "medium", *, seed: int | None = None) -> Sudoku:
    if difficulty not in DIFFICULTY_CLUES:
        raise ValueError(f"Unknown difficulty {difficulty!r}")
    rng = random.Random(seed)
    solution = _full_solution(rng)
    puzzle = [row[:] for row in solution]
    target_clues = DIFFICULTY_CLUES[difficulty]

    cells = [(r, c) for r in range(9) for c in range(9)]
    rng.shuffle(cells)
    clues = 81
    for r, c in cells:
        if clues <= target_clues:
            break
        saved = puzzle[r][c]
        puzzle[r][c] = 0
        # Removing must keep the solution unique.
        if _count_solutions([row[:] for row in puzzle]) != 1:
            puzzle[r][c] = saved  # revert
        else:
            clues -= 1

    return Sudoku(puzzle=puzzle, solution=solution, difficulty=difficulty)
