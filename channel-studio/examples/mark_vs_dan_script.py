"""Mark vs Dan — a character-driven finance narrative video.

Format: two friends, identical paychecks, opposite money habits, followed across
decades to a satisfying reveal. This story structure retains far better than a
dry explainer because the viewer picks a side and stays for the payoff.

~1,200 words ≈ 9 min at 130 wpm (clears the 8-min mid-roll threshold).
Advertiser-safe: general education, illustrative numbers, explicit "not advice".

Run to emit the Fliki paste-script + scene CSV/storyboard:
    PYTHONPATH=src python examples/mark_vs_dan_script.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from channel_studio import sceneflow  # noqa: E402

TITLE = "Two Friends, Same Paycheck — One Retired Rich (Here's Why)"

SEGMENTS = [
    # HOOK
    "Mark and Dan started the exact same job, on the exact same day, for the "
    "exact same paycheck. Same salary every year. Same raises. On paper, they "
    "were financial twins. But thirty years later, one of them retired a "
    "millionaire, and the other was still clocking in, quietly terrified of his "
    "bank account. Here's the unsettling part: the one who ended up rich never "
    "earned a single dollar more than the other. The difference came down to a "
    "few small choices that looked almost meaningless at the time. Let me show "
    "you exactly how this happened, month by month, because once you see it, "
    "you can't unsee it.",

    # SEGMENT 1 — meet the two
    "Let's meet our two friends properly. Mark is the guy everyone loves. The "
    "day his first paycheck hit, he leased a brand-new car with the big engine "
    "and the leather seats. He upgraded to the nicer apartment downtown. Nice "
    "watch, newest phone every year, dinners out four nights a week. From the "
    "outside, Mark looked like the most successful person in the room. Dan? Dan "
    "was almost boring. He drove a clean, reliable used car he paid for "
    "outright. He found a modest apartment with a roommate for the first few "
    "years. He still went out, still had fun, but he quietly set up one thing "
    "Mark never did: an automatic transfer that moved a slice of every "
    "paycheck into investments before he could spend it. Same income. Two "
    "completely different machines running underneath.",

    # SEGMENT 2 — the invisible gap forms
    "For the first couple of years, nothing dramatic happened, and that's "
    "exactly why this trap is so dangerous. Mark was clearly winning. He had "
    "the lifestyle, the photos, the envy. Dan's investment account was small "
    "and unimpressive, growing slowly in the background where nobody could see "
    "it. If you froze the story right here, everyone would want to be Mark. "
    "Picture them at a party at year three. Mark pulls up in the new car, "
    "everyone turns to look. Dan pulls up in the same used car he's had the "
    "whole time, and nobody notices. In that exact moment, Mark feels rich and "
    "Dan feels invisible. But underneath the surface, Dan's money had quietly "
    "started doing something Mark's money never could: it began earning money "
    "on its own. Every dollar Dan invested was now a tiny worker, going out and "
    "earning more dollars, which then went out and earned even more. His army "
    "of dollar-workers was small for now, but it was growing every single "
    "month, and crucially, it never slept and never took a day off. Mark's "
    "dollars, meanwhile, left his account the moment they arrived and never "
    "came back. He wasn't building an army. He was renting a lifestyle, and the "
    "rent was due again every month, forever.",

    # SEGMENT 3 — compounding takes over
    "Now let's fast-forward and watch the gap explode. Around year ten, "
    "something quietly flips. Dan's account isn't growing mainly from his "
    "monthly deposits anymore. It's growing from its own past growth. This is "
    "compounding, and it is the closest thing to magic in all of personal "
    "finance. The returns start earning returns. The curve stops looking like a "
    "gentle hill and starts bending upward like a rocket. Mark, at year ten, is "
    "in a strange spot. He earns a great salary, but he has almost nothing "
    "saved, because every raise he ever got was immediately swallowed by a "
    "bigger lifestyle. A nicer car. A bigger apartment. The treadmill just got "
    "faster. He's running harder than ever and standing in exactly the same "
    "place.",

    # SEGMENT 4 — the lifestyle trap named
    "What happened to Mark has a name: lifestyle creep. Every time his income "
    "went up, his spending went up to match it, so he never actually got "
    "ahead. This is the quiet trap that trains people in great-paying jobs to "
    "stay broke for their entire lives. And here's the brutal math behind it. "
    "Because Mark never invested, he didn't just miss out on the money he could "
    "have saved. He missed out on everything that money would have earned, and "
    "everything those earnings would have earned, for thirty straight years. "
    "Economists have a phrase for that lost future growth: opportunity cost. "
    "Mark's daily luxuries didn't just cost him their price tag. They cost him "
    "the entire fortune that money could have quietly become.",

    # SEGMENT 5 — the satisfying reveal
    "So let's jump to the finish line, thirty years in, and add it all up, "
    "because this is the part that's genuinely satisfying. Dan, the boring one, "
    "by consistently investing a sensible slice of that same ordinary paycheck "
    "and simply leaving it alone, has built a portfolio worth well over a "
    "million dollars. Sit with that number. Same salary as Mark, never a dollar "
    "more, and he's a millionaire. He can walk away from work whenever he "
    "wants. His money now earns more in a single good year than his job ever "
    "paid him in that year, which means his dollar-army now out-earns him. He "
    "has crossed the line where he works because he wants to, not because he "
    "has to. Now look over at Mark. Same career, same lifetime earnings, same "
    "thirty years of paychecks. But Mark is approaching retirement with almost "
    "nothing saved, staring down the frightening reality of working a decade "
    "longer than he ever planned, because he has no choice. The cruel twist is "
    "that Mark spent thirty years feeling richer than Dan the entire way, right "
    "up until the moment it mattered most. Same paycheck. Same thirty years. "
    "One quietly built a machine that now works for him, while the other spent "
    "three decades feeding a machine that gave nothing back. That contrast, "
    "right there, is the entire lesson.",

    # SEGMENT 6 — the viewer's turn
    "Now here's why this actually matters for you, watching right now. The good "
    "news buried in this story is that Dan was not special. He wasn't smarter, "
    "he didn't earn more, and he didn't pick magic stocks. He simply automated "
    "one boring decision and then got out of his own way for a very long time. "
    "The two levers that decided everything were within his control the whole "
    "time: how much of each paycheck he kept, and how early he started letting "
    "it grow. You don't need a huge income to become Dan. You need consistency "
    "and time, and the single most powerful day to start was years ago. The "
    "second most powerful day is today.",

    # OUTRO
    "So the real question this story leaves you with is simple: right now, are "
    "you building Dan's machine, or are you feeding Mark's treadmill? If this "
    "made the choice click for you, subscribe, because next week we're breaking "
    "down exactly how much of each paycheck someone like Dan actually sets "
    "aside, with real numbers you can follow. And one important note: this "
    "video is general education, not financial advice, so always do your own "
    "research for your own situation. Thanks for watching, and I'll see you in "
    "the next one.",
]


def main():
    scenes = sceneflow.to_scenes(SEGMENTS)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, "mark_vs_dan_fliki_script.txt"), "w") as f:
        f.write("\n\n".join(SEGMENTS))
    with open(os.path.join(out_dir, "mark_vs_dan_scenes.md"), "w") as f:
        f.write(sceneflow.to_markdown(TITLE, scenes))
    with open(os.path.join(out_dir, "mark_vs_dan_scenes.csv"), "w") as f:
        f.write(sceneflow.to_csv(scenes))

    words = sum(len(seg.split()) for seg in SEGMENTS)
    print(f"✅ {words} words (~{words/130:.1f} min) — "
          f"{'PASS' if words/130 >= 8 else 'UNDER'} 8-min mid-roll threshold")
    print(f"   {len(scenes)} scenes")
    print("   output/mark_vs_dan_fliki_script.txt  → paste into Fliki")
    print("   output/mark_vs_dan_scenes.md / .csv  → storyboard / backup")


if __name__ == "__main__":
    main()
