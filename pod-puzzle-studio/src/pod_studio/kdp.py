"""KDP print geometry.

Everything Amazon KDP cares about for a paperback interior PDF:
  * trim size (the final cut page size)
  * bleed (extra margin trimmed off, required for full-page art)
  * inside / gutter margin (grows with page count so the binding doesn't
    swallow content)
  * outside / top / bottom safe margins

All public values are in PostScript points (1 inch = 72 pt), because that is
what reportlab draws in.  Inputs from users are in inches, because that is how
KDP documents everything.

References: KDP "Format your paperback manuscript" print specs.
"""

from __future__ import annotations

from dataclasses import dataclass

INCH = 72.0  # points per inch

# The KDP trim sizes worth caring about for puzzle / activity / coloring books.
# 8.5 x 8.5 is the best-seller for coloring/activity (square, gift-friendly);
# 8.5 x 11 maximises puzzle area; 6 x 9 is the cheap-to-print novel size.
TRIM_SIZES_IN = {
    "8.5x8.5": (8.5, 8.5),
    "8.5x11": (8.5, 11.0),
    "8x10": (8.0, 10.0),
    "7x10": (7.0, 10.0),
    "6x9": (6.0, 9.0),
    "5x8": (5.0, 8.0),
}

# KDP fixed bleed amount (applies to all four... but only outer three edges in
# practice; the inside edge has no bleed).  0.125" is the spec.
BLEED_IN = 0.125


def _gutter_in(page_count: int) -> float:
    """Inside (gutter) margin in inches, per KDP's binding table.

    The more pages, the thicker the spine, the more margin the binding eats.
    """
    if page_count <= 150:
        return 0.375
    if page_count <= 300:
        return 0.5
    if page_count <= 500:
        return 0.625
    if page_count <= 700:
        return 0.75
    return 0.875


@dataclass(frozen=True)
class PageGeometry:
    """Resolved, point-based geometry for one book.

    Coordinates assume reportlab's origin (bottom-left).  ``content_*`` is the
    safe rectangle you should draw puzzles inside; ``page_*`` includes bleed.
    """

    trim_w: float
    trim_h: float
    bleed: float
    gutter: float
    outer_margin: float
    top_margin: float
    bottom_margin: float
    bleed_on: bool

    # ----- page (media) box, what the PDF is actually sized to -----
    @property
    def page_w(self) -> float:
        # Bleed adds to the two outer horizontal edges -> width grows by 1 bleed
        # (inside edge has no bleed) when bleed is on.
        return self.trim_w + (self.bleed if self.bleed_on else 0.0)

    @property
    def page_h(self) -> float:
        # Bleed adds to top and bottom -> height grows by 2 bleeds.
        return self.trim_h + (2 * self.bleed if self.bleed_on else 0.0)

    # ----- safe content rectangle (bottom-left origin) -----
    def content_box(self, *, is_right_page: bool) -> tuple[float, float, float, float]:
        """Return (x, y, width, height) of the safe drawing area.

        ``is_right_page`` (odd page number) puts the gutter on the left;
        even/left pages put the gutter on the right.  Bleed shifts the whole
        trim box up by one bleed (since bottom edge bleeds).
        """
        b = self.bleed if self.bleed_on else 0.0
        # On a right-hand page the inside edge is the left edge.
        if is_right_page:
            x = self.gutter
            inner_offset_for_bleed = 0.0  # inside (left) edge: no bleed shift
        else:
            x = self.outer_margin + b  # outer (left) edge carries the bleed
            inner_offset_for_bleed = 0.0
        width = self.trim_w - self.gutter - self.outer_margin
        y = self.bottom_margin + b
        height = self.trim_h - self.top_margin - self.bottom_margin
        return (x, y, width, height)


def resolve_geometry(
    trim: str,
    *,
    page_count: int = 100,
    bleed: bool = True,
    outer_margin_in: float = 0.375,
    top_margin_in: float = 0.375,
    bottom_margin_in: float = 0.5,
) -> PageGeometry:
    """Build :class:`PageGeometry` from a KDP trim key and page count."""
    if trim not in TRIM_SIZES_IN:
        raise ValueError(
            f"Unknown trim {trim!r}. Known: {', '.join(TRIM_SIZES_IN)}"
        )
    tw_in, th_in = TRIM_SIZES_IN[trim]
    return PageGeometry(
        trim_w=tw_in * INCH,
        trim_h=th_in * INCH,
        bleed=BLEED_IN * INCH,
        gutter=_gutter_in(page_count) * INCH,
        outer_margin=outer_margin_in * INCH,
        top_margin=top_margin_in * INCH,
        bottom_margin=bottom_margin_in * INCH,
        bleed_on=bleed,
    )
