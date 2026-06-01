"""High-RPM niche data + a content-idea engine for a standalone AdSense channel.

The channel is monetised by ad revenue, NOT as a funnel to the shop, so niches
are ranked purely by RPM and faceless-producibility (June 2026 market data).

Each niche carries an estimated US RPM range, a faceless-difficulty score, and a
bank of proven long-form title templates. `ideas()` expands those templates into
a publishable backlog.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Niche:
    key: str
    name: str
    rpm_low: float
    rpm_high: float
    faceless_score: int  # 1-5, higher = easier to run faceless
    why: str
    title_templates: list[str] = field(default_factory=list)
    disclaimer: str = ""
    visual_style: str = ""


PERSONAL_FINANCE = Niche(
    key="personal_finance",
    name="Personal Finance & Investing",
    rpm_low=15.0,
    rpm_high=22.0,
    faceless_score=5,
    why="Highest RPM on YouTube + easiest faceless: visuals are charts, text "
    "overlays and stock B-roll. Advertisers pay premium because one converted "
    "customer is worth a lot.",
    title_templates=[
        "How {vehicle} Actually Work (Explained Simply)",
        "{number} Money Habits That Quietly Build Wealth",
        "The Truth About {topic} Nobody Tells Beginners",
        "How to Start Investing With ${amount} in {year}",
        "{number} Budgeting Mistakes That Keep You Broke",
        "Index Funds vs {alt}: Which Builds More Wealth?",
        "What ${amount} a Month Becomes in {years} Years",
        "How Compound Interest Really Works (With Examples)",
    ],
    disclaimer="This video is for general education only and is not financial "
    "advice. Consider speaking with a licensed professional before making "
    "investment decisions.",
    visual_style="clean animated charts, big on-screen numbers, neutral stock "
    "B-roll (city, office, laptop), calm muted color palette",
)

MAKE_MONEY_ONLINE = Niche(
    key="make_money_online",
    name="Make Money Online / Side Hustles",
    rpm_low=15.0,
    rpm_high=20.0,
    faceless_score=4,
    why="Very high RPM; screen-recordings + text. Watch for over-promising — "
    "keep claims realistic to stay advertiser-friendly.",
    title_templates=[
        "{number} Realistic Side Hustles for {year}",
        "How People Actually Make Money With {skill}",
        "I Researched {number} Online Income Ideas — These Work",
        "The Beginner's Guide to {skill} Income",
    ],
    disclaimer="Results are not typical or guaranteed; this is educational "
    "content, not a promise of income.",
    visual_style="screen recordings, UI walkthroughs, text overlays, stock B-roll",
)

LEGAL_EXPLAINER = Niche(
    key="legal_explainer",
    name="Legal & Consumer-Rights Explainers",
    rpm_low=12.0,
    rpm_high=18.0,
    faceless_score=4,
    why="High RPM, evergreen, faceless-friendly (text + simple motion graphics).",
    title_templates=[
        "Your Rights When {situation} (Explained)",
        "{number} Things You Didn't Know Were Legal",
        "What To Do If {situation}",
        "The Law About {topic}, Explained Simply",
    ],
    disclaimer="This is general legal information, not legal advice. Laws vary "
    "by location; consult a qualified attorney for your situation.",
    visual_style="document/graphic motion, text overlays, neutral stock B-roll",
)

TECH_REVIEW = Niche(
    key="tech_explainer",
    name="Tech & Software Explainers",
    rpm_low=7.0,
    rpm_high=14.0,
    faceless_score=5,
    why="Strong RPM, fully faceless via screen recordings and AI voice.",
    title_templates=[
        "{number} {category} Tools That Actually Save You Time",
        "How {tech} Works (No Jargon)",
        "{toolA} vs {toolB}: Which Should You Use?",
        "The Best Free Tools for {task} in {year}",
    ],
    visual_style="screen recordings, app UI, clean text overlays",
)

NICHES = {
    n.key: n
    for n in (PERSONAL_FINANCE, MAKE_MONEY_ONLINE, LEGAL_EXPLAINER, TECH_REVIEW)
}


def get(key: str) -> Niche:
    if key not in NICHES:
        raise ValueError(f"Unknown niche {key!r}. Known: {', '.join(NICHES)}")
    return NICHES[key]


def ranked() -> list[Niche]:
    """Niches sorted by midpoint RPM, highest first."""
    return sorted(
        NICHES.values(), key=lambda n: (n.rpm_low + n.rpm_high) / 2, reverse=True
    )


# Simple fill values to expand title templates into a concrete backlog.
_FILLS = {
    "vehicle": ["index funds", "ETFs", "Roth IRAs", "401(k)s", "bonds", "HYSAs"],
    "number": ["5", "7", "8", "10", "12"],
    "topic": ["compound interest", "the stock market", "inflation", "credit scores"],
    "amount": ["100", "500", "1000", "5000"],
    "year": ["2026"],
    "years": ["10", "20", "30"],
    "alt": ["real estate", "savings accounts", "individual stocks"],
    "skill": ["writing", "design", "AI tools", "spreadsheets"],
    "situation": [
        "you're pulled over", "a flight is cancelled", "you're laid off",
        "a landlord won't return your deposit",
    ],
    "category": ["AI", "productivity", "free"],
    "tech": ["AI chatbots", "VPNs", "cloud storage", "password managers"],
    "toolA": ["Notion"], "toolB": ["Obsidian"],
    "task": ["budgeting", "note-taking", "editing"],
}


def ideas(niche_key: str, count: int = 12) -> list[str]:
    """Expand a niche's title templates into a concrete content backlog."""
    import itertools
    import random

    niche = get(niche_key)
    rng = random.Random(42)
    out: list[str] = []
    for tmpl in itertools.cycle(niche.title_templates):
        title = tmpl
        for key, opts in _FILLS.items():
            token = "{" + key + "}"
            if token in title:
                title = title.replace(token, rng.choice(opts))
        if title not in out:
            out.append(title)
        if len(out) >= count:
            break
    return out
