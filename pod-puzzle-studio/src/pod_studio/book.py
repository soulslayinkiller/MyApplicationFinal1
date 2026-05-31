"""Assemble a full, KDP-ready puzzle/activity book interior PDF.

A book is a sequence of *sections*, each section a run of pages of one puzzle
type.  We render the play pages up front and collect solutions, then emit an
answer-key section at the back (standard activity-book layout).  Page geometry
(trim, bleed, gutter) comes from :mod:`kdp`; rendering from :mod:`render` and
:mod:`coloring`.

The assembler also emits a Higgsfield prompt manifest so the coloring pages and
the funnel Shorts can be generated with a human-in-the-loop credit check.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from reportlab.lib.colors import HexColor, black
from reportlab.pdfgen.canvas import Canvas

from . import coloring as coloring_mod
from . import higgsfield as hf
from . import render
from .kdp import PageGeometry, resolve_geometry
from .puzzles import crossword as cw
from .puzzles import maze as mz
from .puzzles import sudoku as sk
from .puzzles import word_search as ws
from .themes import Theme

ACCENT = HexColor("#FF5A5F")


@dataclass
class Section:
    type: str                     # word_search|sudoku|maze|crossword|coloring
    count: int = 4
    options: dict = field(default_factory=dict)


@dataclass
class BookSpec:
    title: str
    subtitle: str
    author: str
    trim: str
    theme: Theme
    sections: list[Section]
    shop_url: str = "your-shop-url.etsy.com"
    bleed: bool = True


class _Pager:
    """Tracks the current page number so we can flip gutter side & number pages."""

    def __init__(self, canvas: Canvas, geo: PageGeometry):
        self.c = canvas
        self.geo = geo
        self.page = 0

    def new_page(self) -> tuple[float, float, float, float]:
        if self.page > 0:
            self.c.showPage()
        self.page += 1
        self.c.setPageSize((self.geo.page_w, self.geo.page_h))
        is_right = self.page % 2 == 1
        return self.geo.content_box(is_right_page=is_right)

    def footer(self, box):
        x, y, w, h = box
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(HexColor("#999999"))
        self.c.drawCentredString(x + w / 2, y - 22, str(self.page))


def _title_for(section_type: str) -> str:
    return {
        "word_search": "Word Search",
        "sudoku": "Sudoku",
        "maze": "Maze",
        "crossword": "Crossword",
        "coloring": "Color & Relax",
    }.get(section_type, section_type.title())


def build(spec: BookSpec, out_path: str, *, page_count_estimate: int = 100,
          art_dir: str | None = None, seed: int = 7) -> dict:
    geo = resolve_geometry(spec.trim, page_count=page_count_estimate, bleed=spec.bleed)
    c = Canvas(out_path, pagesize=(geo.page_w, geo.page_h))
    c.setTitle(spec.title)
    c.setAuthor(spec.author)
    pager = _Pager(c, geo)

    art_dir = art_dir or os.path.join(os.path.dirname(out_path), "assets", "art")
    image_prompts: list[hf.ImagePrompt] = []
    shorts: list[hf.ShortPlan] = []

    # ---- Front matter ----
    _title_page(c, pager, spec)
    _belongs_page(c, pager, spec)

    solutions: list[tuple[str, object]] = []  # (type, puzzle) for answer key
    puzzle_seed = seed

    for section in spec.sections:
        for i in range(section.count):
            box = pager.new_page()
            _page_header(c, box, _title_for(section.type), i + 1)
            inner = _shrink_top(box, 40)
            puzzle_seed += 1

            if section.type == "word_search":
                size = section.options.get("size", 15)
                p = ws.generate(spec.theme.words, size=size, seed=puzzle_seed)
                render.word_search(c, inner, p)
                solutions.append(("word_search", p))
            elif section.type == "sudoku":
                diff = section.options.get("difficulty", "medium")
                p = sk.generate(diff, seed=puzzle_seed)
                render.sudoku(c, inner, p)
                solutions.append(("sudoku", p))
            elif section.type == "maze":
                dim = section.options.get("size", 18)
                p = mz.generate(dim, dim, seed=puzzle_seed)
                render.maze(c, inner, p)
                solutions.append(("maze", p))
            elif section.type == "crossword":
                p = cw.generate(spec.theme.crossword)
                render.crossword(c, inner, p)
                solutions.append(("crossword", p))
            elif section.type == "coloring":
                subj = spec.theme.coloring_subjects[
                    i % len(spec.theme.coloring_subjects)
                ]
                affirm = (
                    spec.theme.affirmations[i % len(spec.theme.affirmations)]
                    if spec.theme.affirmations else None
                )
                page_id = f"coloring-{spec.theme.key}-{i+1:02d}"
                prompt = hf.line_art_prompt(page_id, subj, art_dir)
                image_prompts.append(prompt)
                art = prompt.art_path
                coloring_mod.coloring_page(
                    c, inner,
                    image_path=art if os.path.exists(art) else None,
                    caption=affirm,
                    prompt_hint=subj,
                )
            else:
                raise ValueError(f"Unknown section type {section.type!r}")
            pager.footer(box)

    # ---- Answer key ----
    if solutions:
        box = pager.new_page()
        _page_header(c, box, "Answer Key", None)
        pager.footer(box)
        for idx, (stype, puzzle) in enumerate(solutions, 1):
            box = pager.new_page()
            _page_header(c, box, f"Solution {idx}", None)
            inner = _shrink_top(box, 40)
            if stype == "word_search":
                render.word_search(c, inner, puzzle, solution=True)
            elif stype == "sudoku":
                render.sudoku(c, inner, puzzle, solution=True)
            elif stype == "maze":
                render.maze(c, inner, puzzle, solution=True)
            elif stype == "crossword":
                render.crossword(c, inner, puzzle, solution=True)
            pager.footer(box)

    # ---- Back matter: shop CTA ----
    box = pager.new_page()
    _cta_page(c, box, spec)

    c.showPage()
    c.save()

    # ---- Funnel Shorts manifest ----
    for j in range(3):
        subj = spec.theme.coloring_subjects[j % len(spec.theme.coloring_subjects)]
        shorts.append(hf.short_plan(j + 1, spec.theme.title, subj, spec.shop_url))

    manifest_path = os.path.join(
        os.path.dirname(out_path), "assets", "prompts.json"
    )
    hf.write_manifest(manifest_path, image_prompts, shorts)

    return {
        "out_path": out_path,
        "pages": pager.page,
        "image_prompts": len(image_prompts),
        "shorts": len(shorts),
        "manifest": manifest_path,
    }


# --------------------------------------------------------------------------
# Page furniture
# --------------------------------------------------------------------------
def _shrink_top(box, amount):
    x, y, w, h = box
    return (x, y, w, h - amount)


def _page_header(c, box, title, index):
    x, y, w, h = box
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 18)
    label = f"{title}" if index is None else f"{title}  #{index}"
    c.drawString(x, y + h - 24, label)
    c.setStrokeColor(HexColor("#EEEEEE"))
    c.setLineWidth(1)
    c.line(x, y + h - 32, x + w, y + h - 32)


def _title_page(c, pager, spec):
    box = pager.new_page()
    x, y, w, h = box
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 30)
    for i, line in enumerate(_wrap_title(spec.title)):
        c.drawCentredString(x + w / 2, y + h * 0.62 - i * 34, line)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Oblique", 15)
    c.drawCentredString(x + w / 2, y + h * 0.5, spec.subtitle)
    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica", 12)
    c.drawCentredString(x + w / 2, y + h * 0.2, spec.author)


def _belongs_page(c, pager, spec):
    box = pager.new_page()
    x, y, w, h = box
    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(x + w / 2, y + h * 0.6, "This book belongs to")
    c.setStrokeColor(HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.line(x + w * 0.2, y + h * 0.52, x + w * 0.8, y + h * 0.52)


def _cta_page(c, box, spec):
    x, y, w, h = box
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(x + w / 2, y + h * 0.6, "Loved this book?")
    c.setFillColor(black)
    c.setFont("Helvetica", 13)
    c.drawCentredString(
        x + w / 2, y + h * 0.5,
        "A quick review helps other moms find it — thank you!",
    )
    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica", 12)
    c.drawCentredString(x + w / 2, y + h * 0.4, f"More books: {spec.shop_url}")


def _wrap_title(title, max_chars=18):
    words = title.split()
    lines, cur = [], ""
    for word in words:
        if len(cur + " " + word) <= max_chars:
            cur = (cur + " " + word).strip()
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _wrap_title_helper():  # pragma: no cover
    pass
