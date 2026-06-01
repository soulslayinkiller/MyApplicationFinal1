"""Long-form faceless video script structuring.

Optimised for AdSense, where the money is in *watch time past 8 minutes*
(unlocks multiple mid-roll ads) and strong retention. This module turns a topic
+ a set of talking points into a structured, timed script skeleton with:

  * a 0-15s hook (retention make-or-break),
  * an open loop / "stay to the end" promise,
  * 4-7 content segments with natural mid-roll ad break markers,
  * a recap + CTA (subscribe) outro.

It does NOT write the prose for you with an LLM here (no API key assumed); it
produces the *scaffold* and the exact per-segment LLM prompts so a human-in-the
-loop Claude/ChatGPT pass fills each beat. This keeps "creative input" in the
loop, which is what YouTube's 2026 anti-mass-production policy requires.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Target ~130 spoken words per minute (calm explainer pace).
WORDS_PER_MINUTE = 130
# Put a mid-roll marker roughly every this-many seconds after the 8-min mark.
MIDROLL_SPACING_S = 180


@dataclass
class Segment:
    heading: str
    target_seconds: int
    talking_points: list[str]
    llm_prompt: str = ""

    @property
    def target_words(self) -> int:
        return round(self.target_seconds / 60 * WORDS_PER_MINUTE)


@dataclass
class Script:
    topic: str
    angle: str
    hook: str
    promise: str
    segments: list[Segment]
    outro_cta: str
    disclaimer: str = ""
    midroll_marks: list[int] = field(default_factory=list)  # seconds

    @property
    def total_seconds(self) -> int:
        return sum(s.target_seconds for s in self.segments) + 30  # +hook/outro

    @property
    def total_words(self) -> int:
        return sum(s.target_words for s in self.segments)


def _midroll_marks(segments: list[Segment]) -> list[int]:
    """Compute mid-roll break seconds: only after 8:00, spaced out, on segment
    boundaries (so an ad never interrupts a sentence)."""
    marks = []
    elapsed = 15  # hook
    next_eligible = 8 * 60
    for seg in segments:
        elapsed += seg.target_seconds
        if elapsed >= next_eligible:
            marks.append(elapsed)
            next_eligible = elapsed + MIDROLL_SPACING_S
    return marks


def build(
    topic: str,
    angle: str,
    points: list[str],
    *,
    disclaimer: str = "",
    target_minutes: int = 10,
) -> Script:
    """Build a long-form script scaffold from a topic and bullet talking points.

    Points are distributed across segments; each gets an LLM prompt so the prose
    pass is one paste away. Total runtime is steered toward ``target_minutes``
    (kept >= 8 so mid-rolls unlock).
    """
    target_minutes = max(8, target_minutes)
    # Reserve ~20s hook + ~25s outro; split the rest across content segments.
    content_s = target_minutes * 60 - 45
    n_segments = max(4, min(7, len(points)))
    per = content_s // n_segments

    # Chunk the points roughly evenly across segments.
    segments: list[Segment] = []
    for i in range(n_segments):
        chunk = points[i::n_segments] or [f"Key idea {i+1} about {topic}"]
        heading = chunk[0][:60]
        seg = Segment(
            heading=heading,
            target_seconds=per,
            talking_points=chunk,
            llm_prompt=(
                f"Write ~{round(per/60*WORDS_PER_MINUTE)} words of clear, "
                f"engaging faceless-narration script for a segment titled "
                f"'{heading}' in a video about '{topic}' ({angle}). Cover these "
                f"points conversationally, use concrete examples and numbers, "
                f"keep one open loop to the next segment, and avoid specific "
                f"buy/sell advice. Points: {', '.join(chunk)}."
            ),
        )
        segments.append(seg)

    hook = (
        f"[0:00-0:15 HOOK] Open with a surprising stat or bold claim about "
        f"{topic}. No intro, no 'hey guys' — earn the next 10 seconds."
    )
    promise = (
        f"[0:15-0:30 PROMISE] Tell viewers exactly what they'll be able to do "
        f"by the end, and tease the most valuable segment to create an open loop."
    )
    outro = (
        "[OUTRO] One-line recap of the payoff, then a specific subscribe ask "
        "tied to a future video ('next week: ...'). End screen 2 video picks."
    )

    return Script(
        topic=topic,
        angle=angle,
        hook=hook,
        promise=promise,
        segments=segments,
        outro_cta=outro,
        disclaimer=disclaimer,
        midroll_marks=_midroll_marks(segments),
    )
