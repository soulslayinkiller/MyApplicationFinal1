"""Flat-cartoon visual style for faceless explainer videos.

Targets the "clean flat 2D illustration" look (think modern flat-design
explainer cartoons): simple rounded characters, bold flat color fills, minimal
shading, a consistent limited palette, plain backgrounds. Generated as still
images by a Higgsfield image model (Seedream / Flux do flat-vector well), then
dropped into the auto-edit tool with light motion (slow zoom / slide).

The goal is a *consistent* set across a whole video, so every prompt shares one
style suffix and one palette — that consistency is what makes a channel look
"branded" instead of like random clip-art.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# One shared style suffix appended to every scene so the whole video matches.
# Tuned toward the flat-design explainer look the user referenced.
FLAT_STYLE_SUFFIX = (
    "flat 2D vector illustration, modern flat design, bold simple shapes, "
    "clean thick outlines, minimal flat shading, simple rounded cartoon "
    "characters, limited color palette of teal blue, warm orange and soft "
    "cream, plain uncluttered background, vector art, professional explainer "
    "video style, 16:9 wide composition, high quality"
)

# Things to explicitly avoid so frames stay on-style and print/encode cleanly.
NEGATIVE = (
    "photorealistic, 3D render, realistic photo, gradients everywhere, "
    "cluttered, busy background, text, watermark, logo, extra fingers"
)


@dataclass
class ScenePrompt:
    index: int
    narration: str
    image_prompt: str
    aspect_ratio: str = "16:9"


# Map narration cues -> a concrete *visual scene* to draw, so the image shows an
# action/scene (like the reference channel) instead of an abstract concept.
# Each value is the subject half of the prompt; the style suffix is appended.
# ORDER MATTERS: more specific concepts (fees, panic, subscribe) are listed
# before the generic "money" catch-all, since the first matching rule wins and
# words like "dollars" appear in almost every finance sentence.
_SCENE_HINTS = [
    (r"fee|expense ratio|percent|\d+%",
     "a cartoon person watching tiny coins leak out of a small hole in a "
     "money bag, a magnifying glass highlighting the leak"),
    (r"panic|sell|crash|fear|market drop|pull (your )?money out|nervous",
     "a cartoon person looking nervous at a red downward stock arrow on a "
     "phone, then a calmer version of the person sitting still and relaxed"),
    (r"subscribe|next week|do your own research|not financial advice",
     "a friendly cartoon person waving next to a large red subscribe button "
     "and a bell icon"),
    (r"diversif|bankrupt|risk|fail|eggs",
     "a cartoon person calmly holding many small eggs in different baskets, "
     "one basket cracked but the person still smiling"),
    (r"index fund|basket|500 compan|s&p|companies|own a sliver",
     "a cartoon shopping basket filled with many tiny labelled company "
     "buildings, a smiling person holding it"),
    (r"open an account|brokerage|automatic|every month|set up|app",
     "a cartoon person setting up an app on a phone with a recurring calendar "
     "icon, a small plant growing out of the phone"),
    (r"chart|grow|growth|compound|rocket|500,?000|half a million|million",
     "a big rising green line chart on a wall, a cheerful cartoon person "
     "pointing up at it, a small rocket at the end of the line"),
    (r"early|twenties|forties|decade|timeline|forty years",
     "two cartoon people on a timeline path, one starting early near a small "
     "seedling, one starting later, the early one beside a big tree"),
    (r"\$?\d+0|dollars|money|cash|wealth|rich",
     "a friendly cartoon person happily holding a stack of money, small upward "
     "arrow and coins floating around them"),
]

_DEFAULT_SCENE = (
    "a friendly cartoon person explaining an idea, a simple thought bubble "
    "above them with a coin or chart icon"
)


def _subject_for(narration: str) -> str:
    low = narration.lower()
    for pattern, subject in _SCENE_HINTS:
        if re.search(pattern, low):
            return subject
    return _DEFAULT_SCENE


def build_scene_prompts(narration_sentences: list[str]) -> list[ScenePrompt]:
    """Turn each narration sentence into a flat-style image prompt."""
    prompts: list[ScenePrompt] = []
    for i, sentence in enumerate(narration_sentences, 1):
        subject = _subject_for(sentence)
        prompts.append(ScenePrompt(
            index=i,
            narration=sentence,
            image_prompt=f"{subject}, {FLAT_STYLE_SUFFIX}",
        ))
    return prompts


def consistency_note() -> str:
    return (
        "All prompts share FLAT_STYLE_SUFFIX (same palette + style) so the whole "
        "video looks like one branded set. Generate with a Higgsfield image "
        "model (seedream_v4_5 or flux for crisp flat vector). Keep the same "
        "model + suffix across every video on the channel for a consistent brand."
    )
