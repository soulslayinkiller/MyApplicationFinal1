# 🎬 Video #1 — Ready to Publish (Fliki walkthrough)

**Channel A — Personal Finance** · "How Index Funds Actually Work (Explained Simply)"
8.6 min · 1,124 words · clears the 8-min mid-roll threshold ✅

Everything below is done. Follow the 6 steps and you'll have a published video.

---

## STEP 1 — Generate the files (already done)

```bash
cd channel-studio
PYTHONPATH=src python examples/index_funds_full_script.py
```
Produces in `output/`:
- `index_funds_fliki_script.txt` ← the script you paste into Fliki
- `index_funds_scenes.md` ← storyboard to review B-roll choices
- `index_funds_scenes.csv` ← scene backup (if you use manual mode)

## STEP 2 — Build the video in Fliki (~10 min, near hands-off)

1. Fliki → **New File → Script to Video**.
2. Paste the full contents of `index_funds_fliki_script.txt`.
3. **Voice:** pick an "ultra-realistic" male or female voice — try
   *"Sara"* or *"Liam"* (calm, authoritative). Preview one paragraph first.
4. **Aspect ratio:** 16:9 (long-form, NOT vertical).
5. Click **Generate**. Fliki auto-segments the script, fetches B-roll for each
   line, generates the voiceover, and adds captions.
6. **Review pass (~10 min):** scrub through. Wherever a clip looks off-topic,
   click it and swap using the keyword from `index_funds_scenes.md` for that
   scene (e.g. scene 8 → `stock market graph`). Add a few on-screen numbers
   where the storyboard shows 🔤 (the $100, 500, 1% moments).
7. **Export** at 1080p.

> Free plan = watermark + 720p (fine for a test). For publishing, Standard tier
> (~$28/mo) gives 1080p + the best voices and includes ElevenLabs-tier audio,
> so you don't need a separate voice subscription.

## STEP 3 — Title (A/B two options)

- **A:** How Index Funds Actually Work (Explained Simply)
- **B:** I Wish I Understood Index Funds Sooner (Beginner's Guide)

Start with A; if CTR is low after ~48h, swap to B.

## STEP 4 — Description (paste as-is, with chapters)

```
Index funds might be the most powerful wealth-building tool for ordinary
people — but almost nobody understands how they actually work. This beginner's
guide breaks it down simply, with real numbers and no jargon.

⏱️ Chapters
0:00 The $100 that became $5,000
0:20 What an index fund actually is
1:30 Why diversification is a "free lunch"
3:00 Fees: the silent wealth killer
4:30 How compounding really works
6:00 The #1 mistake beginners make
7:15 How to actually get started

📌 This video is general education, not financial advice. Always do your own
research for your own situation before making any investment decision.

#indexfunds #investing #personalfinance #investingforbeginners #compoundinterest
```
*(Adjust the chapter timestamps to match your final render — Fliki shows them.)*

## STEP 5 — Thumbnail (face-free, readable small)

- Big bold text: **"$100 → $5,000"** with an upward arrow.
- Sub-text: **"INDEX FUNDS EXPLAINED"**
- Style: clean, one chart icon, calm muted colors (navy/green), high contrast.
- Tools: Canva (free) "YouTube Thumbnail" template. Keep it to 3–4 words.

## STEP 6 — Upload settings (this is where the money is)

- ✅ **Monetization → enable mid-roll ads** (auto-placement is fine; the 8.6-min
  length unlocks them — that's the whole point of going past 8:00).
- ✅ Add an **end screen** (last 20s) with "subscribe" + 1 video pick.
- ✅ Add to a **Playlist** ("Investing for Beginners") — boosts session time.
- ❌ Do **NOT** mark "Made for Kids."
- Tags: `personal finance, index funds, investing for beginners, compound
  interest, how to invest, explained, 2026`

---

## After it's live
Log the stats into `config/portfolio.json` after ~a week and run:
```bash
PYTHONPATH=src python -m channel_studio.cli curate --portfolio config/portfolio.json
```
That starts feeding the A/B/C curator so the data can pick your winning channel.

## ⚠️ Honest expectations
This is video #1. It will probably get modest views — that's normal. Channel
growth comes from **publishing consistently** (1/week) so the algorithm learns
who to show it to. One video is a test of your *workflow*, not your *channel*.
