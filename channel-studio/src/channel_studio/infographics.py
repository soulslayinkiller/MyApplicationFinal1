"""Visual style + per-video infographic prompt sets.

The look we're after is "modern flat 2D vector infographic" — bold flat colors,
thick clean outlines, friendly cartoon characters, big charts and numbers. We
describe it generically (NEVER by referencing another channel/brand name — that
is a trademark risk and just bad practice). Swapping STYLE here re-skins every
image in the channel at once, keeping a consistent brand.

Each video has an ordered list of (scene_id, subject) infographic beats. The
art is generated from STYLE + subject via Higgsfield image models (Seedream 4.5
/ Flux.2 Pro / Nano Banana — all unlimited-eligible in the Higgsfield app).
"""

from __future__ import annotations

from dataclasses import dataclass

# The reusable house style. Channel-neutral, no brand names.
STYLE = (
    "modern flat 2D vector infographic illustration, bold clean flat colors, "
    "thick clean outlines, minimal shading, friendly simple cartoon characters, "
    "big bold charts and icons, navy blue background with bright green and "
    "yellow accents, high contrast, professional explainer graphic, vector art, "
    "no photorealism, clean composition"
)

# Optional: generate art WITHOUT embedded text (AI mangles small text). You then
# overlay perfect numbers/labels in your editor (Fliki). Recommended for any beat
# whose impact depends on a number being correct.
NO_TEXT_SUFFIX = "no text, no words, no letters, no numbers, leave clean space for captions"


@dataclass
class InfographicBeat:
    scene_id: str
    subject: str
    embed_text: bool = False  # False = generate text-free, overlay in editor

    def prompt(self, *, style: str = STYLE) -> str:
        base = f"{self.subject}. {style}"
        if not self.embed_text:
            base += f". {NO_TEXT_SUFFIX}"
        return base


# Index-funds video: the key beats worth illustrating (hook + one per segment).
INDEX_FUNDS_BEATS: list[InfographicBeat] = [
    InfographicBeat(
        "hook",
        "an upward-trending green growth chart line rising from a small stack "
        "of money on the left to a huge overflowing money bag on the right, a "
        "friendly cartoon businessman smiling and gesturing at the chart",
        embed_text=False,
    ),
    InfographicBeat(
        "what_is",
        "a big basket holding many small company building icons, representing "
        "owning a slice of 500 companies at once",
    ),
    InfographicBeat(
        "diversification",
        "a split scene: one lonely cracked building crumbling on the left "
        "versus a wide row of many small healthy buildings standing strong on "
        "the right, showing spreading risk",
    ),
    InfographicBeat(
        "fees",
        "two side-by-side jars of coins, one slowly leaking coins through a "
        "crack labeled high fee, the other staying full, a worried cartoon "
        "character watching the leaking jar",
    ),
    InfographicBeat(
        "compounding",
        "a small seed growing into a giant money tree across a row of stages, "
        "an exponential curve in the background shooting upward like a rocket",
    ),
    InfographicBeat(
        "mistake",
        "a panicked cartoon investor pressing a big red SELL button as a chart "
        "dips, while the chart immediately rebounds upward right after",
    ),
    InfographicBeat(
        "get_started",
        "three simple numbered steps as flat icons: open an account, choose a "
        "fund, set up automatic monthly contributions, with arrows between them",
    ),
]


# Mark vs Dan video: the satisfying two-character visual journey.
MARK_VS_DAN_BEATS: list[InfographicBeat] = [
    InfographicBeat(
        "hook",
        "split-screen of two friendly cartoon men in identical office uniforms "
        "shaking hands on their first day, an identical paycheck floating above "
        "each of them, a clock and calendar showing the same start date",
    ),
    InfographicBeat(
        "meet_them",
        "left side a flashy cartoon man with a shiny sports car, gold watch and "
        "shopping bags; right side a calm cartoon man beside a modest used car "
        "with a small arrow moving a coin into an investment jar",
    ),
    InfographicBeat(
        "invisible_gap",
        "a party scene: one cartoon man getting all the attention by a fancy "
        "car, the other standing quietly in the background while a tiny stack "
        "of coins behind him glows and slowly grows",
    ),
    InfographicBeat(
        "compounding",
        "a row of growing money trees getting taller left to right with a steep "
        "exponential curve rising behind them, tiny cartoon coin characters "
        "with arms carrying more coins, an army of dollars at work",
    ),
    InfographicBeat(
        "lifestyle_creep",
        "a cartoon man running on a treadmill chasing an ever-bigger car and "
        "house that stay just out of reach, sweating, going nowhere, a flat "
        "line of zero savings beneath him",
    ),
    InfographicBeat(
        "reveal",
        "split finish line: left a tired cartoon man with an empty wallet still "
        "in his work uniform; right a relaxed cartoon man on a beach chair "
        "beside a giant overflowing money bag and a soaring chart",
    ),
    InfographicBeat(
        "your_turn",
        "a single cartoon viewer standing at a fork in the road, one path toward "
        "a treadmill, the other toward a money tree and a beach, a glowing "
        "arrow inviting a choice",
    ),
]


VIDEO_BEATS = {
    "index_funds": INDEX_FUNDS_BEATS,
    "mark_vs_dan": MARK_VS_DAN_BEATS,
}
