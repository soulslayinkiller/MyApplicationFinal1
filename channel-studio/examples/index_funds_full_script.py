"""A fully-written example finance video, ready for auto-assembly.

This is what a *finished* script looks like after the segment LLM-prompts are
filled in with real, careful, advertiser-safe prose (general education, no
buy/sell advice). Run this file to emit the scene-script (Markdown + CSV) you
paste into Fliki / Pictory / InVideo.

    PYTHONPATH=src python examples/index_funds_full_script.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from channel_studio import sceneflow  # noqa: E402

TITLE = "How Index Funds Actually Work (Explained Simply)"

# Hook + each segment, written out.
# NOTE: As written this is ~710 words ≈ 5.5 min — a DEMO of the format, not a
# finished runtime. For AdSense you want 8+ min to unlock mid-roll ads, so the
# real video needs ~40% more prose: add a concrete numeric example and one
# real-world story to each segment (the LLM segment-prompts ask for exactly
# this). Treat this file as the structure/quality bar, then expand each beat.
SEGMENTS = [
    # HOOK (0:00-0:15)
    "If you put 100 dollars into a typical index fund forty years ago, it would "
    "be worth over 5,000 dollars today, without you doing anything at all. No "
    "stock picking, no day trading, no watching the news. So why does almost "
    "nobody understand how these things actually work? In the next few minutes, "
    "that changes.",

    # SEGMENT 1 — what it is
    "Let's start with the simplest possible definition. An index is just a list. "
    "The S&P 500, for example, is a list of about 500 of the largest companies "
    "in the United States. An index fund is a basket that holds a tiny slice of "
    "every company on that list. So when you buy one share of an S&P 500 index "
    "fund, you instantly own a sliver of 500 businesses at once. You are not "
    "betting on one company winning. You are betting that the overall economy "
    "keeps growing over time, which, historically, it has. That single idea is "
    "why index funds exist.",

    # SEGMENT 2 — why diversification matters
    "Here is why that basket matters so much. Imagine you put everything into a "
    "single company, and that company goes bankrupt. Your money is gone. Now "
    "imagine you own 500 companies, and one goes bankrupt. You barely feel it, "
    "because the other 499 are still working for you. This is called "
    "diversification, and it is the closest thing investing has to a free lunch. "
    "You lower your risk without necessarily lowering your long-term return. A "
    "single bad headline can sink one stock, but it almost never sinks the "
    "entire market at once.",

    # SEGMENT 3 — fees, the silent killer
    "Now for the part that quietly decides who builds wealth and who doesn't: "
    "fees. Every fund charges a small yearly fee called an expense ratio. A "
    "typical actively managed fund might charge one percent or more. A broad "
    "index fund might charge as little as three hundredths of a percent. That "
    "sounds tiny, but over thirty years, a one percent fee can eat away tens of "
    "thousands of dollars from your final balance. Lower fees mean more of your "
    "money stays invested and keeps compounding. This is the main reason index "
    "funds quietly beat most expensive funds over the long run.",

    # SEGMENT 4 — compounding
    "Speaking of compounding, this is where the real magic lives. Compounding "
    "means your gains start earning their own gains. In year one, your money "
    "grows a little. In year two, that growth also grows. Stretch this over "
    "decades and the curve stops looking like a gentle slope and starts looking "
    "like a rocket. This is exactly why starting early matters more than "
    "starting with a lot. Someone who invests a small amount in their twenties "
    "can end up ahead of someone who invests far more in their forties, simply "
    "because time did the heavy lifting.",

    # SEGMENT 5 — common mistake
    "But there is one mistake that wrecks all of this, and almost every beginner "
    "makes it: panic selling. When the market drops, and it always does "
    "sometimes, the instinct is to pull your money out to stop the pain. The "
    "problem is that the biggest up days in the market often happen right after "
    "the biggest down days. If you sell at the bottom and sit in cash, you miss "
    "the recovery. Historically, the people who simply stayed invested and did "
    "nothing during the scary periods came out far ahead of the people who "
    "tried to time their exit.",

    # SEGMENT 6 — getting started
    "So how would a complete beginner actually start? In simple terms, you open "
    "an investment account with a reputable brokerage, you choose a broad, "
    "low-cost index fund, and you set up a small automatic contribution every "
    "month. That last part, automation, removes emotion from the equation. You "
    "are no longer deciding whether to invest each month; it just happens. Over "
    "years, those automatic contributions plus compounding do the work while you "
    "live your life. The goal is not to get rich this week. The goal is to be "
    "consistently, boringly invested for a very long time.",

    # OUTRO
    "If this made index funds finally click, the best thing you can do is keep "
    "learning before you put real money anywhere. Next week, we are breaking "
    "down exactly how much a small monthly investment can grow into over twenty "
    "years, with real numbers. Subscribe so you don't miss it. And remember, "
    "this video is general education, not financial advice, so always do your "
    "own research for your own situation.",
]


def main():
    scenes = sceneflow.to_scenes(SEGMENTS)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    md = sceneflow.to_markdown(TITLE, scenes)
    csv_text = sceneflow.to_csv(scenes)
    with open(os.path.join(out_dir, "index_funds_scenes.md"), "w") as f:
        f.write(md)
    with open(os.path.join(out_dir, "index_funds_scenes.csv"), "w") as f:
        f.write(csv_text)
    words = sum(len(s.narration.split()) for s in scenes)
    print(f"✅ {len(scenes)} scenes, ~{words} words (~{words/130:.1f} min)")
    print("   output/index_funds_scenes.md  (review)")
    print("   output/index_funds_scenes.csv (paste into Fliki/Pictory)")


if __name__ == "__main__":
    main()
