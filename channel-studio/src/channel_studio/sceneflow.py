"""Scene-script export for auto-assembly tools (Fliki / Pictory / InVideo).

Those tools build a finished video from a *scene list*: each scene = a line of
narration + a stock-footage search keyword + optional on-screen text. They then
auto-fetch B-roll, generate the AI voice, and burn captions — no manual editing.

This module converts a written script into that scene format and renders it as:
  * a clean Markdown storyboard (human review), and
  * a CSV (paste/import into the auto-tool).

Keeping narration in <=~22-word scenes matches how these tools chunk footage
(one clip per sentence-ish), which yields the most natural auto-edit.
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass


@dataclass
class Scene:
    index: int
    narration: str
    broll_keyword: str
    on_screen_text: str = ""
    kind: str = "broll"  # broll | chart | text


def _split_sentences(text: str) -> list[str]:
    # Simple sentence splitter; good enough for narration chunking.
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


# Keyword hints: map common finance terms to good stock-footage search words,
# so the auto-tool pulls relevant B-roll instead of random clips.
_KEYWORD_HINTS = {
    "index fund": "stock market graph",
    "compound": "growth chart animation",
    "invest": "investing app phone",
    "save": "piggy bank savings",
    "budget": "person budgeting laptop",
    "retire": "happy retired couple",
    "market": "stock exchange screen",
    "money": "cash money counting",
    "interest": "rising line graph",
    "credit": "credit card payment",
    "debt": "bills paperwork stress",
    "wealth": "luxury city skyline",
    "tax": "tax documents desk",
    "rights": "courthouse building",
    "law": "law books gavel",
    "side hustle": "person working laptop cafe",
}


def _keyword_for(sentence: str, fallback: str = "business office b-roll"
                 ) -> tuple[str, str]:
    low = sentence.lower()
    for term, kw in _KEYWORD_HINTS.items():
        if term in low:
            kind = "chart" if any(w in kw for w in ("graph", "chart")) else "broll"
            return kw, kind
    # Fallback: reuse the segment's topic keyword (passed in) rather than a
    # random long word — keeps B-roll on-theme instead of literal.
    return fallback, "broll"


def _on_screen_text(sentence: str) -> str:
    """Surface a number/percentage as an on-screen emphasis if present."""
    m = re.search(r"\$?\d[\d,\.]*%?", sentence)
    return m.group(0) if m else ""


def _segment_topic_keyword(seg_text: str) -> str:
    """Pick a representative on-theme keyword for a whole segment, used as the
    fallback B-roll for its plainer sentences."""
    for term, kw in _KEYWORD_HINTS.items():
        if term in seg_text.lower():
            return kw if not any(w in kw for w in ("graph", "chart")) \
                else "finance business b-roll"
    return "business office b-roll"


def to_scenes(narration_by_segment: list[str]) -> list[Scene]:
    """Flatten written segment prose into auto-tool scenes."""
    scenes: list[Scene] = []
    i = 1
    for seg_text in narration_by_segment:
        seg_fallback = _segment_topic_keyword(seg_text)
        for sentence in _split_sentences(seg_text):
            kw, kind = _keyword_for(sentence, fallback=seg_fallback)
            scenes.append(Scene(
                index=i,
                narration=sentence,
                broll_keyword=kw,
                on_screen_text=_on_screen_text(sentence),
                kind=kind,
            ))
            i += 1
    return scenes


def to_markdown(title: str, scenes: list[Scene]) -> str:
    out = [f"# Scene Script — {title}\n",
           f"_{len(scenes)} scenes · paste into Fliki/Pictory, or use the CSV._\n"]
    for s in scenes:
        out.append(
            f"**Scene {s.index}** ({s.kind})\n"
            f"- 🎙️ {s.narration}\n"
            f"- 🎞️ B-roll: `{s.broll_keyword}`"
            + (f"\n- 🔤 On-screen: **{s.on_screen_text}**" if s.on_screen_text else "")
            + "\n"
        )
    return "\n".join(out)


def to_csv(scenes: list[Scene]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["scene", "narration", "broll_keyword", "on_screen_text", "kind"])
    for s in scenes:
        w.writerow([s.index, s.narration, s.broll_keyword, s.on_screen_text, s.kind])
    return buf.getvalue()
