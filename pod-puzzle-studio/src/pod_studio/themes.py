"""Themed content packs.

The whole studio is niche-agnostic: a "theme" is just a name, a list of words
(for word search), a list of (answer, clue) pairs (for crosswords) and a list
of coloring-art subjects.  Swap these and the same engine produces a book for
any niche.  The packs below seed the "moms" niche options we researched:
self-care, cozy/cottagecore, and parenting-affirmations.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Theme:
    key: str
    title: str
    description: str
    words: list[str] = field(default_factory=list)
    crossword: list[tuple[str, str]] = field(default_factory=list)
    coloring_subjects: list[str] = field(default_factory=list)
    affirmations: list[str] = field(default_factory=list)


SELF_CARE = Theme(
    key="self_care",
    title="Self-Care Sunday",
    description="calming self-care, bubble baths, candles, tea, soft cozy mood",
    words=[
        "SELFCARE", "BUBBLEBATH", "BOUNDARIES", "JOURNAL", "MEDITATE",
        "GRATITUDE", "SUNSHINE", "CANDLES", "HERBALTEA", "BREATHE",
        "REST", "BALANCE", "KINDNESS", "SOFTLIFE", "SLOWDOWN",
        "AFFIRM", "NOURISH", "STILLNESS", "PAUSE", "RECHARGE",
    ],
    crossword=[
        ("BREATHE", "Slow, deep ___ to calm the nervous system"),
        ("JOURNAL", "Write your thoughts in this"),
        ("CANDLE", "Light one for a cozy evening"),
        ("TEA", "Warm herbal cup for winding down"),
        ("REST", "What every tired mom deserves"),
        ("BOUNDARY", "A healthy 'no' creates this"),
        ("GRATITUDE", "Daily practice of thankfulness"),
        ("BATH", "Bubble ___ for relaxation"),
        ("CALM", "Peaceful state of mind"),
        ("PAUSE", "Take a short ___ in your day"),
    ],
    coloring_subjects=[
        "a cozy bathtub with bubbles, candles and plants",
        "a steaming mug of tea surrounded by flowers",
        "a soft armchair with a blanket and a book",
        "a bouquet of wildflowers in a mason jar",
        "a crescent moon with stars and soft clouds",
    ],
    affirmations=[
        "I am allowed to rest.",
        "My needs matter too.",
        "I am doing enough.",
        "Calm is my superpower.",
        "I choose peace today.",
    ],
)

COTTAGECORE = Theme(
    key="cottagecore",
    title="Cozy Cottagecore",
    description="cottagecore, mushrooms, wildflowers, cottages, gardens, soft nature",
    words=[
        "COTTAGE", "MUSHROOM", "WILDFLOWER", "GARDEN", "TEACUP",
        "LANTERN", "MEADOW", "HONEYBEE", "BUTTERFLY", "BASKET",
        "DAISIES", "LAVENDER", "SUNFLOWER", "COZY", "QUILT",
        "BAKING", "BERRIES", "FERNS", "STREAM", "ACORN",
    ],
    crossword=[
        ("MUSHROOM", "Toadstool with a spotted cap"),
        ("GARDEN", "Where the wildflowers grow"),
        ("LAVENDER", "Purple, fragrant calming herb"),
        ("HONEYBEE", "Buzzing pollinator"),
        ("COTTAGE", "Small cozy country home"),
        ("QUILT", "Patchwork blanket"),
        ("MEADOW", "Open grassy field of flowers"),
        ("LANTERN", "Old-fashioned light to carry"),
        ("BERRIES", "Picked for the pie"),
        ("ACORN", "Oak tree's seed"),
    ],
    coloring_subjects=[
        "a cozy cottage with a thatched roof and flower garden",
        "a cluster of spotted mushrooms with ferns",
        "a honeybee on a sunflower",
        "a basket of wildflowers and berries",
        "a teapot surrounded by daisies and butterflies",
    ],
    affirmations=[
        "Slow mornings, full heart.",
        "Bloom at your own pace.",
        "Find joy in small things.",
        "Grow through what you go through.",
        "Peace grows here.",
    ],
)

PARENTING = Theme(
    key="parenting",
    title="Mom Affirmations",
    description="warm parenting affirmations, hearts, hugs, family, gentle mood",
    words=[
        "PATIENCE", "BEDTIME", "SNUGGLES", "STORYTIME", "GROWTH",
        "LAUGHTER", "MESSY", "GENTLE", "PRESENT", "ENOUGH",
        "COFFEE", "NAPTIME", "VILLAGE", "GRACE", "RESILIENT",
        "LOVE", "PLAYDATE", "TANTRUM", "HUGS", "BREATHE",
    ],
    crossword=[
        ("PATIENCE", "Hard to keep, worth the practice"),
        ("BEDTIME", "Routine at the end of the day"),
        ("VILLAGE", "It takes one to raise a child"),
        ("GRACE", "Give yourself some ___"),
        ("COFFEE", "A tired parent's best friend"),
        ("SNUGGLE", "Cozy cuddle with little ones"),
        ("ENOUGH", "You are already ___"),
        ("GENTLE", "A calm parenting approach"),
        ("GROWTH", "Both yours and theirs"),
        ("LAUGH", "The best family medicine"),
    ],
    coloring_subjects=[
        "a heart made of swirls with the word LOVE",
        "a cozy reading nook with pillows and books",
        "a coffee cup with a sweet hand-lettered quote",
        "a mama bear hugging a baby bear",
        "a sun with a smiling face and gentle rays",
    ],
    affirmations=[
        "I am the mom my kids need.",
        "Good enough is good enough.",
        "I lead with love.",
        "We are learning together.",
        "My patience grows each day.",
    ],
)

THEMES = {t.key: t for t in (SELF_CARE, COTTAGECORE, PARENTING)}


def get(key: str) -> Theme:
    if key not in THEMES:
        raise ValueError(f"Unknown theme {key!r}. Known: {', '.join(THEMES)}")
    return THEMES[key]
