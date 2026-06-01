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
# 13 beats for a ~9-min video (~40s of screen time each) so the visuals never
# go stale. Consistency tip: Mark always on the LEFT in red/orange, Dan always
# on the RIGHT in green/blue — repeat that in every prompt for a coherent cast.
_CAST = (
    "Mark is a friendly cartoon man on the left in a red and orange outfit; "
    "Dan is a friendly cartoon man on the right in a green and blue outfit; "
    "keep both characters looking the same in every scene"
)

MARK_VS_DAN_BEATS: list[InfographicBeat] = [
    # HOOK (2)
    InfographicBeat(
        "hook_handshake",
        f"{_CAST}. The two men shaking hands on their first day at the same "
        "office, an identical paycheck floating above each of them, a calendar "
        "showing the same start date",
    ),
    InfographicBeat(
        "hook_split_future",
        f"{_CAST}. A dramatic split down the middle: Mark on the left looking "
        "stressed in old work clothes, Dan on the right relaxed and wealthy, a "
        "big question mark between them",
    ),
    # MEET THEM (2)
    InfographicBeat(
        "meet_mark",
        f"{_CAST}. Focus on Mark on the left celebrating beside a shiny new "
        "leased sports car, a gold watch, a new phone and shopping bags, money "
        "flying away from his pockets",
    ),
    InfographicBeat(
        "meet_dan",
        f"{_CAST}. Focus on Dan on the right beside a modest used car, calmly "
        "setting up an automatic transfer arrow that moves a coin from his "
        "paycheck into a glowing investment jar",
    ),
    # INVISIBLE GAP (2)
    InfographicBeat(
        "party_scene",
        f"{_CAST}. A party: Mark on the left getting all the attention next to "
        "his flashy car while Dan stands quietly in the background, almost "
        "invisible",
    ),
    InfographicBeat(
        "hidden_seed",
        f"{_CAST}. Behind Dan on the right, a small stack of coins quietly "
        "glowing and beginning to sprout into a tiny money plant, unnoticed by "
        "everyone at the party",
    ),
    # COMPOUNDING (2)
    InfographicBeat(
        "dollar_army",
        "tiny friendly cartoon coin characters with little arms and legs "
        "marching out and bringing back even more coins, an army of dollars at "
        "work, on a navy background",
    ),
    InfographicBeat(
        "compounding_curve",
        "a row of money trees growing taller from left to right with a steep "
        "exponential green curve rising behind them like a rocket, a small "
        "calendar flipping from year one to year ten",
    ),
    # LIFESTYLE CREEP (2)
    InfographicBeat(
        "treadmill",
        f"{_CAST}. Mark running on a treadmill chasing an ever-bigger car and "
        "house that stay just out of reach, sweating, going nowhere",
    ),
    InfographicBeat(
        "opportunity_cost",
        f"{_CAST}. Mark on the left holding luxury items, while behind him a "
        "faded ghostly outline shows the giant fortune those purchases could "
        "have become, a sad shrinking arrow",
    ),
    # REVEAL (2)
    InfographicBeat(
        "finish_line",
        f"{_CAST}. A finish line: Mark on the left tired with an empty wallet "
        "still in his work uniform, Dan on the right relaxed in a beach chair "
        "beside a giant overflowing money bag and a soaring chart",
    ),
    InfographicBeat(
        "millionaire_dan",
        f"{_CAST}. Dan on the right smiling beside a huge money bag with a big "
        "upward chart, his money clearly now earning more than his old job, a "
        "trophy nearby",
    ),
    # YOUR TURN (1)
    InfographicBeat(
        "fork_in_road",
        "a single friendly cartoon viewer seen from behind standing at a fork "
        "in the road, one path leading to a treadmill and bills, the other to a "
        "money tree and a beach, a glowing arrow inviting a choice",
    ),
]


VIDEO_BEATS = {
    "index_funds": INDEX_FUNDS_BEATS,
    "mark_vs_dan": MARK_VS_DAN_BEATS,
}
