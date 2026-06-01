"""Portfolio curator for an A/B/C test across multiple channels.

The strategy (user's call): launch the top-RPM niches in parallel as separate
channels, publish to each on a schedule, then let real performance pick the
winner instead of guessing. This module is the "curator": it ingests simple
per-video metrics, scores each channel, and recommends where to double down,
hold, or cut.

Metrics are kept in a plain JSON file you update (or wire to the YouTube
Analytics API later). No external calls here — it's deterministic and testable.

Decision model (first ~60-90 days):
  * Score blends RPM realised, views velocity, retention, and CTR — the levers
    that actually drive AdSense income — into one comparable number per channel.
  * Recommends DOUBLE_DOWN / HOLD / CUT so effort concentrates on the winner.
"""

from __future__ import annotations

import json
import statistics
from dataclasses import asdict, dataclass, field


@dataclass
class VideoStat:
    title: str
    published: str          # ISO date
    views: int = 0
    watch_hours: float = 0.0
    avg_view_pct: float = 0.0  # average percentage viewed (retention)
    ctr_pct: float = 0.0       # impressions click-through rate
    rpm_usd: float = 0.0       # realised RPM
    revenue_usd: float = 0.0


@dataclass
class ChannelReport:
    niche: str
    name: str
    videos: int
    total_views: int
    total_revenue: float
    avg_rpm: float
    avg_retention: float
    avg_ctr: float
    score: float
    recommendation: str
    notes: list[str] = field(default_factory=list)


# Weights for the composite score. Tuned so realised revenue and retention
# (the two strongest signals of a durable AdSense channel) dominate.
_W = {
    "revenue": 0.40,
    "retention": 0.25,
    "rpm": 0.20,
    "ctr": 0.15,
}


def _norm(value: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


def score_channel(niche: str, name: str, stats: list[VideoStat]) -> ChannelReport:
    if not stats:
        return ChannelReport(niche, name, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             "NEED_DATA", ["No videos logged yet."])
    total_views = sum(s.views for s in stats)
    total_rev = sum(s.revenue_usd for s in stats)
    avg_rpm = statistics.mean([s.rpm_usd for s in stats if s.rpm_usd] or [0])
    avg_ret = statistics.mean([s.avg_view_pct for s in stats])
    avg_ctr = statistics.mean([s.ctr_pct for s in stats])

    # Normalise against rough healthy-channel reference bands.
    score = (
        _W["revenue"] * _norm(total_rev, 0, 500)       # $0-500 in test window
        + _W["retention"] * _norm(avg_ret, 25, 55)     # 25-55% avg view
        + _W["rpm"] * _norm(avg_rpm, 3, 20)            # $3-20 RPM
        + _W["ctr"] * _norm(avg_ctr, 2, 10)            # 2-10% CTR
    ) * 100

    notes: list[str] = []
    if avg_ret < 30:
        notes.append("Retention low (<30%): tighten hooks and pacing.")
    if avg_ctr < 4:
        notes.append("CTR low (<4%): rework thumbnails/titles.")
    if avg_rpm and avg_rpm < 5:
        notes.append("RPM below niche expectation: check audience geo/topic.")
    if len(stats) < 5:
        notes.append("Small sample (<5 videos): keep publishing before judging.")

    return ChannelReport(
        niche=niche, name=name, videos=len(stats), total_views=total_views,
        total_revenue=round(total_rev, 2), avg_rpm=round(avg_rpm, 2),
        avg_retention=round(avg_ret, 1), avg_ctr=round(avg_ctr, 1),
        score=round(score, 1), recommendation="", notes=notes,
    )


def curate(portfolio: dict[str, list[VideoStat]], names: dict[str, str]
           ) -> list[ChannelReport]:
    """Score every channel and tag DOUBLE_DOWN / HOLD / CUT relative to peers."""
    reports = [
        score_channel(niche, names.get(niche, niche), stats)
        for niche, stats in portfolio.items()
    ]
    scored = [r for r in reports if r.recommendation != "NEED_DATA"]
    if not scored:
        for r in reports:
            r.recommendation = "NEED_DATA"
        return reports

    best = max(r.score for r in scored)
    for r in reports:
        if r.recommendation == "NEED_DATA":
            continue
        if r.videos < 5:
            r.recommendation = "KEEP_TESTING"
        elif r.score >= 0.85 * best:
            r.recommendation = "DOUBLE_DOWN"
        elif r.score >= 0.5 * best:
            r.recommendation = "HOLD"
        else:
            r.recommendation = "CUT"
    return sorted(reports, key=lambda r: r.score, reverse=True)


def load_portfolio(path: str) -> tuple[dict[str, list[VideoStat]], dict[str, str]]:
    with open(path) as f:
        raw = json.load(f)
    portfolio: dict[str, list[VideoStat]] = {}
    names: dict[str, str] = {}
    for ch in raw["channels"]:
        names[ch["niche"]] = ch.get("name", ch["niche"])
        portfolio[ch["niche"]] = [VideoStat(**v) for v in ch.get("videos", [])]
    return portfolio, names


def report_text(reports: list[ChannelReport]) -> str:
    lines = ["PORTFOLIO CURATOR — channel A/B/C test\n"]
    for i, r in enumerate(reports, 1):
        lines.append(
            f"{i}. {r.name}  [{r.recommendation}]  score={r.score}\n"
            f"   videos={r.videos}  views={r.total_views}  "
            f"rev=${r.total_revenue}  rpm=${r.avg_rpm}  "
            f"retention={r.avg_retention}%  ctr={r.avg_ctr}%"
        )
        for n in r.notes:
            lines.append(f"     - {n}")
    return "\n".join(lines)


def to_dict(reports: list[ChannelReport]) -> dict:
    return {"reports": [asdict(r) for r in reports]}
