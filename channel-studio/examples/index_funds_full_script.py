"""A fully-written, publish-ready example finance video for Fliki.

This is the finished article: real, careful, advertiser-safe prose (general
education, no buy/sell advice), expanded to clear the 8-minute mid-roll
threshold (~1,150 words ≈ 8.8 min at 130 wpm).

Run it to emit everything you paste into Fliki:
  * output/index_funds_fliki_script.txt  → paste into Fliki "Script to Video"
  * output/index_funds_scenes.md         → human storyboard (review)
  * output/index_funds_scenes.csv        → scene list (backup / manual mode)

    PYTHONPATH=src python examples/index_funds_full_script.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from channel_studio import sceneflow  # noqa: E402

TITLE = "How Index Funds Actually Work (Explained Simply)"

# Hook + segments, written to ~1,150 words ≈ 8.8 min at 130 wpm (8+ unlocks
# mid-roll ads). Each segment carries a concrete number and a relatable example.
SEGMENTS = [
    # HOOK (0:00-0:20)
    "If you had put just 100 dollars into a typical American index fund forty "
    "years ago, it would be worth over 5,000 dollars today, without you doing a "
    "single thing. No stock picking. No day trading. No staring at red and "
    "green numbers all day. You would have simply bought it, forgotten about "
    "it, and let time do the work. So why does almost nobody actually "
    "understand how these things work, even though they might be the single "
    "most powerful wealth-building tool available to ordinary people? By the "
    "end of this video, you will understand index funds better than most adults "
    "ever will. Let's get into it.",

    # SEGMENT 1 — what it is
    "Let's start with the simplest possible definition, because the name makes "
    "it sound more complicated than it is. An index is just a list. The S&P "
    "500, the most famous example, is simply a list of roughly 500 of the "
    "largest publicly traded companies in the United States. Think names like "
    "Apple, Microsoft, and Coca-Cola. An index fund is a basket that holds a "
    "tiny piece of every single company on that list. So when you buy one share "
    "of an S&P 500 index fund, you are not buying one company. You instantly "
    "own a microscopic sliver of all 500 of them at the same time. You are no "
    "longer betting on one business getting it right. You are betting that the "
    "American economy, as a whole, keeps growing over the long run, which, "
    "across its entire history, it has. That one idea is the foundation of "
    "everything else in this video.",

    # SEGMENT 2 — diversification
    "Now here is why owning that whole basket matters so much. Imagine you took "
    "your life savings and put all of it into a single company. If that company "
    "fails, and even huge companies sometimes do, your money is simply gone. "
    "There is no recovery. Now imagine instead that you own 500 companies, and "
    "one of them goes bankrupt. You would barely notice, because the other 499 "
    "are still out there working for you. This is called diversification, and "
    "it is often described as the only free lunch in investing. You dramatically "
    "lower your risk without necessarily lowering your long-term return. A "
    "single bad earnings report or scandal can destroy one stock overnight, but "
    "it almost never destroys the entire market at once. Spreading your money "
    "across hundreds of companies is what turns investing from a gamble into a "
    "patient, sensible strategy.",

    # SEGMENT 3 — fees
    "Next comes the part that quietly separates the people who build real wealth "
    "from the people who don't, and almost nobody pays attention to it: fees. "
    "Every fund charges a small annual fee called an expense ratio. It is taken "
    "out automatically, so you never feel it leave your pocket. A traditional, "
    "actively managed fund, where a manager picks stocks for you, might charge "
    "one percent or even more every year. A broad index fund might charge as "
    "little as three or four hundredths of one percent. That difference sounds "
    "almost too small to matter. But run the math over thirty years, and that "
    "one percent fee can quietly eat away tens of thousands of dollars from "
    "your final balance. Every dollar you don't pay in fees stays invested and "
    "keeps compounding for you. This single, boring detail is the biggest "
    "reason low-cost index funds tend to beat expensive funds over the long "
    "run.",

    # SEGMENT 4 — compounding
    "Speaking of compounding, this is where the real magic actually lives, and "
    "it is worth slowing down for. Compounding means your gains begin earning "
    "gains of their own. In year one, your money grows a little. In year two, "
    "that new growth also starts growing. Stretch this process over decades, "
    "and the line on the chart stops looking like a gentle hill and starts "
    "looking like a rocket leaving the ground. Here is the part that surprises "
    "people most: starting early matters far more than starting with a large "
    "amount. Someone who invests a modest sum in their twenties and stops can "
    "easily end up with more than someone who invests much more, but doesn't "
    "begin until their forties. The difference isn't the money. It's the "
    "years. Time is the one ingredient you can never buy back later, which is "
    "why the best moment to start is almost always as soon as you reasonably "
    "can.",

    # SEGMENT 5 — the big mistake
    "But there is one mistake that can quietly undo everything we've talked "
    "about, and nearly every beginner makes it at least once: panic selling. "
    "When the market drops sharply, and it absolutely will from time to time, "
    "every instinct in your body screams at you to pull your money out and stop "
    "the bleeding. The cruel irony is that some of the single biggest up days "
    "in market history have happened just days after the biggest down days. If "
    "you sell in fear at the bottom and sit in cash, you don't just lock in "
    "your losses, you also miss the powerful recovery that often follows. "
    "Decades of data show the same thing again and again: the investors who "
    "simply stayed put and did nothing during the scary stretches almost always "
    "came out far ahead of the ones who tried to cleverly time their way in and "
    "out. Doing nothing is a strategy, and often the winning one.",

    # SEGMENT 6 — getting started
    "So how would a complete beginner actually put all of this into practice? "
    "In plain terms, the process has just three steps. First, you open an "
    "investment account with a reputable, well-known brokerage. Second, you "
    "choose a broad, low-cost index fund, the kind that holds hundreds or even "
    "thousands of companies for a tiny fee. And third, and this is the secret "
    "that ties it all together, you set up a small automatic contribution every "
    "single month. That automation quietly removes emotion from the entire "
    "equation. You are no longer deciding whether to invest when the headlines "
    "are scary, because the decision was already made once, in advance. Month "
    "after month, those steady contributions combine with compounding to do the "
    "heavy lifting while you simply live your life. The goal was never to get "
    "rich by Friday. The goal is to be consistently, almost boringly, invested "
    "for a very long time.",

    # OUTRO
    "If this finally made index funds click for you, the most valuable thing "
    "you can do right now is keep learning before you ever put real money "
    "anywhere. Next week, we are breaking down exactly how much a small monthly "
    "investment can realistically grow into over twenty years, using real "
    "numbers you can follow along with. Subscribe so it lands in your feed the "
    "moment it goes live. And one important reminder: this video is general "
    "education, not financial advice, so always do your own research for your "
    "own situation before making any decision. Thanks for watching, and I'll "
    "see you in the next one.",
]


def main():
    scenes = sceneflow.to_scenes(SEGMENTS)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Clean paste-ready script for Fliki "Script to Video".
    script_txt = "\n\n".join(SEGMENTS)
    with open(os.path.join(out_dir, "index_funds_fliki_script.txt"), "w") as f:
        f.write(script_txt)

    # 2 + 3. Storyboard + scene CSV.
    with open(os.path.join(out_dir, "index_funds_scenes.md"), "w") as f:
        f.write(sceneflow.to_markdown(TITLE, scenes))
    with open(os.path.join(out_dir, "index_funds_scenes.csv"), "w") as f:
        f.write(sceneflow.to_csv(scenes))

    words = sum(len(seg.split()) for seg in SEGMENTS)
    print(f"✅ Full script: {words} words (~{words/130:.1f} min) — "
          f"{'PASS' if words/130 >= 8 else 'UNDER'} 8-min mid-roll threshold")
    print(f"   {len(scenes)} scenes")
    print("   output/index_funds_fliki_script.txt  → paste into Fliki")
    print("   output/index_funds_scenes.md         → storyboard")
    print("   output/index_funds_scenes.csv        → scene backup")


if __name__ == "__main__":
    main()
