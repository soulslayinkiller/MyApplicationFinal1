"""Channel Studio CLI.

Two modes:

  # 1. Explore niches / generate a content backlog
  python -m channel_studio.cli niches
  python -m channel_studio.cli ideas --niche personal_finance --count 15

  # 2. Build a full production brief for one video
  python -m channel_studio.cli plan \
      --niche personal_finance \
      --topic "How Index Funds Actually Work (Explained Simply)" \
      --minutes 10 --out output/index_funds.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import curator as curator_mod
from . import niches as niche_mod
from . import production, script


def _cmd_niches(_args):
    print("High-RPM niches (ranked by midpoint RPM):\n")
    for n in niche_mod.ranked():
        mid = (n.rpm_low + n.rpm_high) / 2
        stars = "★" * n.faceless_score + "☆" * (5 - n.faceless_score)
        print(f"  {n.name}")
        print(f"    RPM ${n.rpm_low:.0f}-${n.rpm_high:.0f} (mid ${mid:.0f})  "
              f"faceless {stars}  key={n.key}")
        print(f"    {n.why}\n")
    return 0


def _cmd_ideas(args):
    backlog = niche_mod.ideas(args.niche, count=args.count)
    n = niche_mod.get(args.niche)
    print(f"Content backlog for {n.name} (RPM ${n.rpm_low:.0f}-${n.rpm_high:.0f}):\n")
    for i, title in enumerate(backlog, 1):
        print(f"  {i:2d}. {title}")
    return 0


def _default_points(topic: str) -> list[str]:
    """Reasonable starter talking points so the scaffold is usable immediately."""
    return [
        f"What {topic} means and why it matters",
        "A concrete real-world example with numbers",
        "The most common beginner mistake",
        "A simple step-by-step you can follow",
        "What the data/history actually shows",
        "A myth to debunk",
        "How to get started this week",
    ]


def _cmd_plan(args):
    n = niche_mod.get(args.niche)
    points = args.points.split("|") if args.points else _default_points(args.topic)
    scr = script.build(
        args.topic, n.name, points,
        disclaimer=n.disclaimer, target_minutes=args.minutes,
    )
    brief = production.plan(scr, n, title=args.title)

    payload = {
        "niche": n.key,
        "script": {
            "topic": scr.topic,
            "angle": scr.angle,
            "hook": scr.hook,
            "promise": scr.promise,
            "target_runtime_min": round(scr.total_seconds / 60, 1),
            "target_words": scr.total_words,
            "midroll_marks_sec": scr.midroll_marks,
            "segments": [
                {
                    "heading": s.heading,
                    "target_seconds": s.target_seconds,
                    "target_words": s.target_words,
                    "talking_points": s.talking_points,
                    "llm_prompt": s.llm_prompt,
                }
                for s in scr.segments
            ],
            "outro_cta": scr.outro_cta,
            "disclaimer": scr.disclaimer,
        },
        "production": production.brief_to_dict(brief),
    }

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"✅ Production brief: {args.out}")
        print(f"   Runtime ~{payload['script']['target_runtime_min']} min "
              f"({scr.total_words} words)")
        print(f"   Mid-roll ad marks (sec): {scr.midroll_marks}")
        print(f"   Segments: {len(scr.segments)} | Visual cues: "
              f"{len(brief.visuals)}")
        print(f"   Est. RPM ${n.rpm_low:.0f}-${n.rpm_high:.0f}")
    else:
        print(json.dumps(payload, indent=2))
    return 0


def _cmd_curate(args):
    portfolio, names = curator_mod.load_portfolio(args.portfolio)
    reports = curator_mod.curate(portfolio, names)
    print(curator_mod.report_text(reports))
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(curator_mod.to_dict(reports), f, indent=2)
        print(f"\n✅ Wrote curator report: {args.out}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="channel_studio")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("niches", help="List high-RPM niches").set_defaults(
        func=_cmd_niches)

    p_ideas = sub.add_parser("ideas", help="Generate a content backlog")
    p_ideas.add_argument("--niche", required=True)
    p_ideas.add_argument("--count", type=int, default=12)
    p_ideas.set_defaults(func=_cmd_ideas)

    p_plan = sub.add_parser("plan", help="Build a full video production brief")
    p_plan.add_argument("--niche", required=True)
    p_plan.add_argument("--topic", required=True)
    p_plan.add_argument("--title", default=None)
    p_plan.add_argument("--minutes", type=int, default=10)
    p_plan.add_argument("--points", default=None,
                        help="Pipe-separated talking points (optional)")
    p_plan.add_argument("--out", default=None)
    p_plan.set_defaults(func=_cmd_plan)

    p_cur = sub.add_parser("curate", help="Score the multi-channel A/B/C test")
    p_cur.add_argument("--portfolio", required=True,
                       help="Path to portfolio.json with channel metrics")
    p_cur.add_argument("--out", default=None)
    p_cur.set_defaults(func=_cmd_curate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
