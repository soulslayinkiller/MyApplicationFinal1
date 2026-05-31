"""Command-line entrypoint.

    python -m pod_studio.cli --config config/book.example.json --out output/book.pdf

The config is a small JSON file describing the book (trim, title, theme,
sections).  This keeps the actual book definitions as data, so launching a new
title for a new niche is a config edit, not a code change.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import themes
from .book import BookSpec, Section, build


def load_spec(path: str) -> tuple[BookSpec, int]:
    with open(path) as f:
        cfg = json.load(f)
    theme = themes.get(cfg["theme"])
    sections = [Section(**s) for s in cfg["sections"]]
    spec = BookSpec(
        title=cfg["title"],
        subtitle=cfg.get("subtitle", ""),
        author=cfg.get("author", ""),
        trim=cfg.get("trim", "8.5x8.5"),
        theme=theme,
        sections=sections,
        shop_url=cfg.get("shop_url", "your-shop-url.etsy.com"),
        bleed=cfg.get("bleed", True),
    )
    return spec, cfg.get("page_count_estimate", 100)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build a KDP-ready puzzle book.")
    parser.add_argument("--config", required=True, help="Path to book config JSON")
    parser.add_argument("--out", required=True, help="Output PDF path")
    parser.add_argument(
        "--art-dir", default=None,
        help="Directory of coloring PNGs (defaults to <out>/assets/art)",
    )
    args = parser.parse_args(argv)

    spec, page_est = load_spec(args.config)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    result = build(spec, args.out, page_count_estimate=page_est, art_dir=args.art_dir)

    print(f"✅ Built: {result['out_path']}")
    print(f"   Pages: {result['pages']}")
    print(f"   Coloring art prompts: {result['image_prompts']}")
    print(f"   Funnel Shorts planned: {result['shorts']}")
    print(f"   Higgsfield manifest: {result['manifest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
