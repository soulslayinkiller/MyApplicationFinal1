"""Bridge to the Higgsfield pipeline.

This module does NOT call the Higgsfield API directly (generation is driven
through the MCP tools in your assistant session, so a credit/unlimited check
always happens with a human in the loop).  Instead it produces the *prompt
manifest* that feeds that pipeline: for every coloring page and every Short,
it writes the exact image/video prompt, the recommended model, and the target
aspect ratio.

Workflow:
  1. ``pod-studio build`` writes ``assets/prompts.json`` alongside the book.
  2. You (or the assistant) feed those prompts to Higgsfield image models
     (Nano Banana / Seedream / Flux — unlimited-eligible) to make line art.
  3. Drop the returned PNGs into ``assets/art/<id>.png`` and rebuild: the
     placeholders become real coloring pages.
  4. The Shorts manifest lists the page-flip / ASMR clips to make with Kling
     3.0 (the only unlimited-eligible video model on the 7-Day pack).
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass

# Recommended models per task, with the honest "is this unlimited on Plus?"
# flag so you always know whether a step costs credits.
MODEL_GUIDE = {
    "line_art": {
        "model": "nano_banana",
        "unlimited_on_plus": "365-day add-on",
        "why": "Fast, clean bold-line art; unlimited-eligible so mass-produce freely.",
    },
    "cover_art": {
        "model": "seedream_4_5",
        "unlimited_on_plus": "365-day add-on",
        "why": "High-res detailed illustration for the front cover.",
    },
    "short_background": {
        "model": "seedream_5_lite",
        "unlimited_on_plus": "365-day add-on",
        "why": "Aesthetic vertical stills for Short backgrounds.",
    },
    "short_video": {
        "model": "kling3_0",
        "unlimited_on_plus": "7-day add-on only",
        "why": "Only video model that goes unlimited on Plus (720p/5s).",
    },
}

# A reusable line-art style suffix that keeps a coloring book consistent and
# KDP-friendly (pure black line on white, no greyscale fills which print muddy).
LINE_ART_STYLE = (
    "black and white line art, bold clean outlines, thick lines, no shading, "
    "no grayscale, no color fill, pure white background, coloring book page, "
    "high contrast, printable, centered composition"
)


@dataclass
class ImagePrompt:
    id: str
    kind: str            # "line_art" | "cover_art" | "short_background"
    prompt: str
    aspect_ratio: str
    model: str
    unlimited_on_plus: str
    art_path: str        # where the returned PNG should be dropped


@dataclass
class ShortPlan:
    id: str
    hook: str            # on-screen opening line (first 1.5s)
    script: str          # voiceover / caption beats
    visual: str          # what the clip shows
    cta: str             # call to action -> the shop
    model: str
    unlimited_on_plus: str
    aspect_ratio: str = "9:16"


def line_art_prompt(page_id: str, subject: str, art_dir: str) -> ImagePrompt:
    g = MODEL_GUIDE["line_art"]
    return ImagePrompt(
        id=page_id,
        kind="line_art",
        prompt=f"{subject}, {LINE_ART_STYLE}",
        aspect_ratio="3:4",  # close to 8.5x8.5/portrait page; safe for trim
        model=g["model"],
        unlimited_on_plus=g["unlimited_on_plus"],
        art_path=os.path.join(art_dir, f"{page_id}.png"),
    )


def cover_prompt(book_slug: str, theme_desc: str, art_dir: str) -> ImagePrompt:
    g = MODEL_GUIDE["cover_art"]
    return ImagePrompt(
        id=f"{book_slug}-cover",
        kind="cover_art",
        prompt=(
            f"book cover illustration, {theme_desc}, warm inviting, cozy, "
            "soft palette, room for title text at top, professional KDP cover"
        ),
        aspect_ratio="3:4",
        model=g["model"],
        unlimited_on_plus=g["unlimited_on_plus"],
        art_path=os.path.join(art_dir, f"{book_slug}-cover.png"),
    )


def short_plan(idx: int, theme: str, sample_subject: str, shop_url: str) -> ShortPlan:
    """A page-flip / ASMR Short that demos the product and funnels to the shop."""
    g = MODEL_GUIDE["short_video"]
    return ShortPlan(
        id=f"short-{idx:02d}",
        hook="POV: 10 quiet minutes that are just for you 🤍",
        script=(
            f"Beat 1 (0-1.5s): hook text over a {sample_subject} page slowly "
            f"filling with color.\n"
            f"Beat 2 (1.5-5s): satisfying color-fill ASMR, soft marker sounds.\n"
            f"Beat 3 (caption): 'Bold & easy {theme} coloring — made for tired moms.'"
        ),
        visual=(
            f"vertical close-up of a {sample_subject} coloring page being "
            "filled in, warm lighting, hands optional, oddly-satisfying pacing"
        ),
        cta=f"Full book in bio → {shop_url}",
        model=g["model"],
        unlimited_on_plus=g["unlimited_on_plus"],
    )


def write_manifest(path: str, images: list[ImagePrompt], shorts: list[ShortPlan]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "model_guide": MODEL_GUIDE,
        "images": [asdict(i) for i in images],
        "shorts": [asdict(s) for s in shorts],
        "instructions": (
            "Feed each image prompt to the listed Higgsfield model via the MCP "
            "generate_image tool, then save the PNG to its art_path and rebuild "
            "the book. For shorts, use generate_video with the listed model."
        ),
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path
