"""Coloring / activity page layout.

A coloring page is mostly a single full-area line-art image plus an optional
affirmation caption.  The art itself is produced by an image model (Higgsfield
Nano Banana / Seedream / Flux — all unlimited-eligible on Plus).  This module
lays that art out onto a print-safe page, OR, when no image is supplied yet,
draws a labelled placeholder box so the interior is reviewable before any
credits/art are spent.
"""

from __future__ import annotations

import os

from reportlab.lib.colors import HexColor, black
from reportlab.pdfgen.canvas import Canvas

ACCENT = HexColor("#FF5A5F")
PLACEHOLDER_BG = HexColor("#FAFAFA")
PLACEHOLDER_LINE = HexColor("#CCCCCC")


def coloring_page(
    c: Canvas,
    box,
    *,
    image_path: str | None = None,
    caption: str | None = None,
    prompt_hint: str | None = None,
):
    """Draw one coloring page into ``box`` (x, y, w, h, bottom-left origin)."""
    x, y, w, h = box
    caption_h = 26 if caption else 0
    art_x, art_y, art_w, art_h = x, y + caption_h, w, h - caption_h

    if image_path and os.path.exists(image_path):
        # Fit the image into the art area, preserving aspect ratio, centred.
        from reportlab.lib.utils import ImageReader

        img = ImageReader(image_path)
        iw, ih = img.getSize()
        scale = min(art_w / iw, art_h / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(
            img,
            art_x + (art_w - dw) / 2,
            art_y + (art_h - dh) / 2,
            width=dw,
            height=dh,
            preserveAspectRatio=True,
            mask="auto",
        )
    else:
        # Placeholder so the book is reviewable before art exists.
        c.setFillColor(PLACEHOLDER_BG)
        c.setStrokeColor(PLACEHOLDER_LINE)
        c.setLineWidth(1)
        c.setDash(6, 4)
        c.rect(art_x, art_y, art_w, art_h, stroke=1, fill=1)
        c.setDash()
        c.setFillColor(HexColor("#999999"))
        c.setFont("Helvetica-Oblique", 11)
        c.drawCentredString(
            art_x + art_w / 2, art_y + art_h / 2 + 8, "[ coloring art goes here ]"
        )
        if prompt_hint:
            c.setFont("Helvetica", 8)
            from .render import _wrap

            cy = art_y + art_h / 2 - 8
            for line in _wrap(f"prompt: {prompt_hint}", art_w - 40, c, 8):
                c.drawCentredString(art_x + art_w / 2, cy, line)
                cy -= 10

    if caption:
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x + w / 2, y + 6, caption)
