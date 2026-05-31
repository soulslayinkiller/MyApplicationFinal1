"""Maze generation via randomised depth-first search (recursive backtracker).

Produces a "perfect" maze (exactly one path between any two cells), which is
the classic activity-book maze.  Entrance is top-left, exit is bottom-right.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

# Wall bitmask per cell: which of the 4 walls are still standing.
N, S, E, W = 1, 2, 4, 8
_DX = {E: 1, W: -1, N: 0, S: 0}
_DY = {N: -1, S: 1, E: 0, W: 0}
_OPP = {N: S, S: N, E: W, W: E}


@dataclass
class Maze:
    cols: int
    rows: int
    # cells[y][x] is a bitmask of walls that are PRESENT.
    cells: list[list[int]]
    # solution path as list of (x, y) from entrance to exit.
    solution: list[tuple[int, int]]


def generate(cols: int = 20, rows: int = 20, *, seed: int | None = None) -> Maze:
    rng = random.Random(seed)
    cells = [[N | S | E | W for _ in range(cols)] for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]

    # Carve with an explicit stack to avoid recursion limits on big mazes.
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        x, y = stack[-1]
        neighbours = []
        for direction in (N, S, E, W):
            nx, ny = x + _DX[direction], y + _DY[direction]
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                neighbours.append((direction, nx, ny))
        if not neighbours:
            stack.pop()
            continue
        direction, nx, ny = rng.choice(neighbours)
        cells[y][x] &= ~direction            # knock down wall here
        cells[ny][nx] &= ~_OPP[direction]    # and on the neighbour
        visited[ny][nx] = True
        stack.append((nx, ny))

    solution = _solve(cells, cols, rows)
    return Maze(cols=cols, rows=rows, cells=cells, solution=solution)


def _solve(cells, cols, rows) -> list[tuple[int, int]]:
    """BFS from (0,0) to (cols-1, rows-1) through carved passages."""
    from collections import deque

    start, goal = (0, 0), (cols - 1, rows - 1)
    prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    q = deque([start])
    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            break
        for direction in (N, S, E, W):
            if cells[y][x] & direction:
                continue  # wall present -> can't pass
            nx, ny = x + _DX[direction], y + _DY[direction]
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in prev:
                prev[(nx, ny)] = (x, y)
                q.append((nx, ny))
    # Reconstruct.
    path: list[tuple[int, int]] = []
    node: tuple[int, int] | None = goal
    while node is not None:
        path.append(node)
        node = prev.get(node)
    path.reverse()
    return path
