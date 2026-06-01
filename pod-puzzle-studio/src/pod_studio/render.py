"""Render puzzle objects onto a reportlab canvas inside a safe content box.

Each function takes the canvas, a content rectangle (x, y, w, h in points,
bottom-left origin) and a puzzle object, and draws it.  Keeping rendering
separate from generation means the same puzzle can be drawn as a play page or
(with the solution flag) as an answer-key page.
"""

from __future__ import annotations

from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen.canvas import Canvas

from .puzzles import crossword as cw
from .puzzles import dot_to_dot as dd
from .puzzles import maze as mz
from .puzzles import sudoku as sk
from .puzzles import word_search as ws

GREY = HexColor("#666666")
LIGHT = HexColor("#DDDDDD")


def _fit_square(x, y, w, h, n):
    """Largest cell size for an n×n grid centred in the box; returns (cell, ox, oy)."""
    cell = min(w, h) / n
    grid_size = cell * n
    ox = x + (w - grid_size) / 2
    oy = y + (h - grid_size) / 2
    return cell, ox, oy


# --------------------------------------------------------------------------
# Word search
# --------------------------------------------------------------------------
def word_search(c: Canvas, box, puzzle: ws.WordSearch, *, solution=False):
    x, y, w, h = box
    n = puzzle.size
    # Reserve bottom third for the word bank.
    grid_area_h = h * 0.72
    cell, ox, oy = _fit_square(x, y + (h - grid_area_h), w, grid_area_h, n)
    oy = y + h - grid_area_h + (grid_area_h - cell * n) / 2 + (h - grid_area_h)
    # Recompute cleanly: place grid in the top region.
    grid_top = y + h
    cell = min(w, grid_area_h) / n
    grid_px = cell * n
    ox = x + (w - grid_px) / 2
    oy = grid_top - grid_px

    c.setFont("Helvetica", cell * 0.55)
    for r in range(n):
        for col in range(n):
            cx = ox + col * cell + cell / 2
            cy = oy + (n - 1 - r) * cell + cell / 2
            c.setFillColor(black)
            c.drawCentredString(cx, cy - cell * 0.2, puzzle.grid[r][col])
    if solution:
        c.setLineWidth(cell * 0.18)
        c.setStrokeColor(HexColor("#FF5A5F"))
        for p in puzzle.placements:
            cells = p.cells()
            (r0, c0), (r1, c1) = cells[0], cells[-1]
            x0 = ox + c0 * cell + cell / 2
            y0 = oy + (n - 1 - r0) * cell + cell / 2
            x1 = ox + c1 * cell + cell / 2
            y1 = oy + (n - 1 - r1) * cell + cell / 2
            c.line(x0, y0, x1, y1)

    # Word bank below the grid.
    words = sorted(puzzle.words)
    bank_top = oy - cell * 0.6
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, bank_top, "WORD BANK")
    c.setFont("Helvetica", 11)
    cols = 3
    col_w = w / cols
    line_h = 16
    for i, word in enumerate(words):
        cc = i % cols
        rr = i // cols
        c.drawString(x + cc * col_w, bank_top - 18 - rr * line_h, word)


# --------------------------------------------------------------------------
# Sudoku
# --------------------------------------------------------------------------
def sudoku(c: Canvas, box, puzzle: sk.Sudoku, *, solution=False):
    x, y, w, h = box
    cell, ox, oy = _fit_square(x, y, w, h, 9)
    grid = puzzle.solution if solution else puzzle.puzzle
    # Cell digits.
    c.setFont("Helvetica", cell * 0.55)
    for r in range(9):
        for col in range(9):
            v = grid[r][col]
            if v:
                cx = ox + col * cell + cell / 2
                cy = oy + (8 - r) * cell + cell / 2 - cell * 0.2
                given = puzzle.puzzle[r][col] != 0
                c.setFillColor(black if given else GREY)
                c.drawCentredString(cx, cy, str(v))
    # Grid lines (thick every 3).
    c.setStrokeColor(black)
    for i in range(10):
        lw = 2.2 if i % 3 == 0 else 0.6
        c.setLineWidth(lw)
        c.line(ox + i * cell, oy, ox + i * cell, oy + 9 * cell)
        c.line(ox, oy + i * cell, ox + 9 * cell, oy + i * cell)


# --------------------------------------------------------------------------
# Maze
# --------------------------------------------------------------------------
def maze(c: Canvas, box, puzzle: mz.Maze, *, solution=False):
    x, y, w, h = box
    cell = min(w / puzzle.cols, h / puzzle.rows)
    grid_w = cell * puzzle.cols
    grid_h = cell * puzzle.rows
    ox = x + (w - grid_w) / 2
    oy = y + (h - grid_h) / 2
    c.setStrokeColor(black)
    c.setLineWidth(1.6)
    for gy in range(puzzle.rows):
        for gx in range(puzzle.cols):
            walls = puzzle.cells[gy][gx]
            # Page y grows upward; maze row 0 is the top.
            px = ox + gx * cell
            py = oy + (puzzle.rows - 1 - gy) * cell
            if walls & mz.N:
                c.line(px, py + cell, px + cell, py + cell)
            if walls & mz.S:
                c.line(px, py, px + cell, py)
            if walls & mz.W:
                c.line(px, py, px, py + cell)
            if walls & mz.E:
                c.line(px + cell, py, px + cell, py + cell)
    # Entrance / exit markers.
    c.setFillColor(GREY)
    c.setFont("Helvetica-Bold", min(cell, 12))
    c.drawCentredString(ox + cell / 2, oy + (puzzle.rows - 0.5) * cell - 3, "")
    if solution:
        c.setStrokeColor(HexColor("#FF5A5F"))
        c.setLineWidth(max(1.5, cell * 0.18))
        pts = []
        for gx, gy in puzzle.solution:
            cx = ox + gx * cell + cell / 2
            cy = oy + (puzzle.rows - 1 - gy) * cell + cell / 2
            pts.append((cx, cy))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            c.line(x0, y0, x1, y1)


# --------------------------------------------------------------------------
# Crossword
# --------------------------------------------------------------------------
def crossword(c: Canvas, box, puzzle: cw.Crossword, *, solution=False):
    x, y, w, h = box
    n_cols, n_rows = puzzle.cols, puzzle.rows
    # Reserve right/bottom space for clues by using ~62% of height for the grid.
    grid_area_h = h * 0.55
    cell = min(w / max(n_cols, 1), grid_area_h / max(n_rows, 1))
    grid_w = cell * n_cols
    grid_h = cell * n_rows
    ox = x + (w - grid_w) / 2
    oy = y + h - grid_h  # top-aligned

    numbers = {(e.row, e.col): e.number for e in puzzle.entries}
    for (r, col), ch in puzzle.grid.items():
        px = ox + col * cell
        py = oy + (n_rows - 1 - r) * cell
        c.setFillColor(white)
        c.setStrokeColor(black)
        c.setLineWidth(0.8)
        c.rect(px, py, cell, cell, stroke=1, fill=1)
        if (r, col) in numbers:
            c.setFillColor(black)
            c.setFont("Helvetica", cell * 0.28)
            c.drawString(px + 1.5, py + cell - cell * 0.32, str(numbers[(r, col)]))
        if solution:
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", cell * 0.55)
            c.drawCentredString(px + cell / 2, py + cell * 0.22, ch)

    # Clues.
    across = [e for e in puzzle.entries if e.horizontal]
    down = [e for e in puzzle.entries if not e.horizontal]
    clue_top = oy - 14
    c.setFillColor(black)
    col_w = w / 2

    def draw_clues(title, entries, start_x):
        cy = clue_top
        c.setFont("Helvetica-Bold", 11)
        c.drawString(start_x, cy, title)
        cy -= 15
        c.setFont("Helvetica", 8.5)
        for e in entries:
            text = f"{e.number}. {e.clue}"
            for line in _wrap(text, col_w - 6, c, 8.5):
                c.drawString(start_x, cy, line)
                cy -= 11
            cy -= 1

    draw_clues("ACROSS", across, x)
    draw_clues("DOWN", down, x + col_w)


# --------------------------------------------------------------------------
# Dot-to-dot (connect the dots) — kids 3-5
# --------------------------------------------------------------------------
def dot_to_dot(c: Canvas, box, puzzle: dd.DotToDot, *, solution=False):
    x, y, w, h = box
    # Keep the shape in a centred square so it isn't stretched.
    side = min(w, h)
    ox = x + (w - side) / 2
    oy = y + (h - side) / 2
    pts = [(ox + px * side, oy + py * side) for px, py in puzzle.points]

    if solution:
        # Show the completed outline.
        c.setStrokeColor(black)
        c.setLineWidth(2)
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            c.line(x0, y0, x1, y1)
        if puzzle.closed:
            c.line(pts[-1][0], pts[-1][1], pts[0][0], pts[0][1])

    # Dots + big numbers (always shown).
    r = max(2.5, side * 0.012)
    c.setFont("Helvetica-Bold", side * 0.045)
    for i, (px, py) in enumerate(pts, 1):
        c.setFillColor(black)
        c.circle(px, py, r, stroke=0, fill=1)
        c.setFillColor(HexColor("#FF5A5F"))
        # Offset the number so it doesn't sit under the dot.
        c.drawString(px + r + 2, py + r, str(i))

    # Gentle instruction line for little ones.
    c.setFillColor(GREY)
    c.setFont("Helvetica", 12)
    c.drawCentredString(
        x + w / 2, y + 4,
        f"Connect the dots 1 to {len(pts)} to find the {puzzle.name.lower()}!",
    )


def _wrap(text, max_w, c, font_size):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if c.stringWidth(trial, "Helvetica", font_size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines
