"""Per-video production plan: voiceover, visuals, assembly, and upload metadata.

Turns a structured Script (from script.py) into a concrete production brief: the
AI-voice settings, a shot/visual list timed to the segments, SEO upload metadata,
and the ordered tool steps. Designed around the cheap faceless long-form stack
(AI script + AI voice + charts/stock B-roll), NOT generative video — because for
high-RPM explainer content, clear charts beat cinematic clips.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .niches import Niche
from .script import Script


@dataclass
class VoicePlan:
    provider: str = "ElevenLabs"
    voice_style: str = "calm, authoritative, friendly explainer"
    model: str = "eleven_v3"
    words: int = 0
    est_minutes: float = 0.0


@dataclass
class VisualCue:
    at_seconds: int
    duration_s: int
    kind: str           # chart | text_overlay | stock_broll | screen_record
    description: str


@dataclass
class UploadMeta:
    title: str
    description: str
    tags: list[str]
    thumbnail_brief: str


@dataclass
class ProductionBrief:
    niche: str
    title: str
    voice: VoicePlan
    visuals: list[VisualCue]
    upload: UploadMeta
    midroll_marks: list[int]
    steps: list[str]
    disclaimer: str


def _visuals_for(script: Script, niche: Niche) -> list[VisualCue]:
    cues: list[VisualCue] = []
    t = 15  # after hook
    # Hook gets an attention-grabbing chart/number.
    cues.append(VisualCue(0, 15, "text_overlay",
                          f"Bold hook stat about {script.topic}, big number on screen"))
    for seg in script.segments:
        # Alternate chart / b-roll to keep it visually moving.
        kind = "chart" if "finance" in niche.key or len(cues) % 2 else "stock_broll"
        cues.append(VisualCue(
            t, seg.target_seconds, kind,
            f"{niche.visual_style or 'clean visuals'} illustrating: {seg.heading}",
        ))
        # A text-overlay emphasis mid-segment.
        cues.append(VisualCue(
            t + seg.target_seconds // 2, 6, "text_overlay",
            f"Key takeaway from '{seg.heading}' as on-screen text",
        ))
        t += seg.target_seconds
    return cues


def _seo(script: Script, niche: Niche) -> UploadMeta:
    base_tags = [niche.name.lower(), script.topic.lower(), "explained",
                 "beginners guide", str(2026), "how to"]
    desc_lines = [
        f"{script.topic} — {script.angle}.",
        "",
        "In this video:",
    ]
    for i, seg in enumerate(script.segments, 1):
        ts = "{:d}:{:02d}".format(*divmod(sum(
            s.target_seconds for s in script.segments[:i - 1]) + 15, 60))
        desc_lines.append(f"{ts} {seg.heading}")
    if script.disclaimer:
        desc_lines += ["", script.disclaimer]
    return UploadMeta(
        title=script.topic if len(script.topic) <= 70 else script.topic[:67] + "...",
        description="\n".join(desc_lines),
        tags=base_tags,
        thumbnail_brief=(
            f"High-contrast thumbnail: 3-4 word phrase about {script.topic}, "
            f"one bold number, a simple icon (chart/arrow), face-free, readable "
            f"at small size. {niche.visual_style}."
        ),
    )


def plan(script: Script, niche: Niche, *, title: str | None = None) -> ProductionBrief:
    voice = VoicePlan(
        words=script.total_words,
        est_minutes=round(script.total_seconds / 60, 1),
    )
    visuals = _visuals_for(script, niche)
    upload = _seo(script, niche)
    if title:
        upload.title = title
    steps = [
        "1. Fill each segment's prose using its llm_prompt (Claude/ChatGPT). "
        "Keep creative direction — do NOT publish raw template output.",
        "2. Generate voiceover from the assembled script (ElevenLabs v3).",
        f"3. Build visuals per the cue list ({len(visuals)} cues): charts in "
        "Canva/After Effects, stock B-roll from Pexels/Storyblocks.",
        "4. Assemble in your editor; place mid-roll-friendly pacing at the "
        f"marked seconds: {script.midroll_marks}.",
        "5. Render 1080p, add captions (boosts retention + accessibility).",
        "6. Upload with the SEO metadata; design thumbnail per brief; "
        "enable mid-roll ads; add end screen + 2 video picks.",
    ]
    return ProductionBrief(
        niche=niche.key,
        title=upload.title,
        voice=voice,
        visuals=visuals,
        upload=upload,
        midroll_marks=script.midroll_marks,
        steps=steps,
        disclaimer=script.disclaimer,
    )


def brief_to_dict(brief: ProductionBrief) -> dict:
    d = asdict(brief)
    return d
