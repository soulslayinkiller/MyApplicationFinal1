# Project Summary & Handoff

_Last updated: 2026-06-02 · Branch: `claude/yt-pod-puzzle-shop-MLgty`_

A running summary of everything built and decided in this project, so you can
pick up where we left off.

---

## The big picture

You're building **two separate businesses**, and a key decision we made is that
they are **decoupled** (different audiences, different goals):

1. 🧩 **POD Puzzle/Activity Book Shop** (Amazon KDP + Etsy) — sells printable
   books. Audience: moms, and parents of kids 3–5.
2. 📈 **Faceless YouTube Channel(s)** — a *standalone* business monetized by
   **AdSense ad revenue** (NOT a funnel to the shop).

Two code "studios" were built in the repo, one per business.

---

## Key strategic decisions (the "why")

- **Channel = AdSense, not a shop funnel.** You optimize the channel purely for
  ad revenue/RPM, unrelated to the puzzle books.
- **Long-form (8+ min) beats Shorts ~30× for AdSense** ($3–15 RPM vs
  $0.05–0.20) because 8+ min unlocks multiple mid-roll ads. So we build
  long-form, not Shorts.
- **Finance is the top niche** — highest RPM ($15–22) AND easiest faceless
  (charts + text + AI voice). Runner-ups: Make Money Online, Legal explainers.
- **Run the top 3 niches in parallel** (A/B/C test), let a **curator** score
  them on real data, then double down on the winner.
- **Editing = auto-tool (Fliki).** You don't hand-edit. Fliki turns the script
  into a finished video (voice + visuals + captions). You picked Fliki over
  Pictory (better AI voice, better footage matching, built for original
  scripts).
- **Visual style = "modern flat 2D vector infographic."** Described generically
  on purpose — we do NOT name any real channel (trademark risk).
- **Kids 3–5 content:** great as *books* (parent is the buyer), but a *channel*
  aimed at kids triggers COPPA (kills ad rates + links). If done, make it
  parent-facing.

---

## Higgsfield (AI image/video) — what we learned

- Plan: **Plus**, ~664 credits remaining.
- Your **unlimited models ARE active** (Kling 2.5 Turbo, Seedance Pro Fast,
  Minimax Hailuo 2.3, + image models Seedream 4.5/V5 Lite, Flux.2 Pro, Nano
  Banana, GPT Image) — confirmed by your screenshot.
- **BUT:** unlimited only applies **in the Higgsfield web app**, not through the
  assistant connection. Generating via chat still costs ~1 credit/image. So for
  free generation, regenerate in the app using the saved prompts.
- Image generation is cheap and the workhorse; video less so.

---

## What's been BUILT (all committed to the branch)

### 📈 `channel-studio/` — the AdSense channel system
- `src/channel_studio/niches.py` — high-RPM niche data + content-idea engine
- `src/channel_studio/script.py` — long-form script scaffolds.
  **Calibrated to Fliki's real voice speed: ~173 wpm** (so 9 min ≈ 1,560 words).
- `src/channel_studio/production.py` — production briefs (voice + visual cues +
  SEO metadata)
- `src/channel_studio/sceneflow.py` — exports scene scripts (narration + B-roll
  keyword + on-screen text) as Markdown/CSV for Fliki
- `src/channel_studio/curator.py` — scores the 3-channel A/B/C test
  (revenue 40% / retention 25% / RPM 20% / CTR 15%) → DOUBLE_DOWN/HOLD/CUT
- `src/channel_studio/infographics.py` — the flat-vector house style + the 16
  Mark-vs-Dan image "beats"
- `cli.py` — commands: `niches`, `ideas`, `plan`, `curate`
- `README.md`, `ROLLOUT.md` (realistic 3-channel time/cost plan)

### 🎬 The first finished video: "Mark vs Dan"
- `examples/mark_vs_dan_script.py` → generates the script files
- `output/mark_vs_dan_fliki_script.txt` — **9.1-min script, paste into Fliki**
- `examples/mark_vs_dan_images.md` — manifest of the **16 generated infographic
  images** (job IDs + which scene + overlay-text suggestions)
- Story: two friends, same paycheck, opposite money habits, satisfying
  compounding reveal. Higher retention than a dry explainer.
- 16 flat-vector text-free images generated, sitting in your Higgsfield feed.

### 🧩 `pod-puzzle-studio/` — the book shop tooling
- Generates print-ready KDP/Etsy PDF interiors (correct trim/bleed/gutter)
- Puzzle types: word search, sudoku, maze, crossword, coloring, **dot-to-dot**
- Themes: `self_care`, `cottagecore`, `parenting`, `construction_kids`
  (Diggers & Trucks, for the kids 3–5 line)
- Higgsfield prompt manifest for coloring art + funnel Shorts
- `README.md`, `STRATEGY.md`

---

## WHERE WE LEFT OFF

You built the Mark vs Dan video in Fliki and it came out great. You wanted to
**remove the heading/title text Fliki adds to each scene**. The fix:
- **Fliki Settings → Text → turn OFF "scene titles/headings"** (global), or
- click each scene's heading text box on the canvas and delete it, or
- avoid header-like first lines in the script step.
- ⚠️ Keep the captions/subtitles at the bottom (good for retention) — only
  delete the big heading.

> Note: I run in a cloud container and **cannot control your local Chrome/Fliki**
> or see your screen — I can only guide you through clicks.

---

## SUGGESTED NEXT STEPS (pick up here)

1. Finish removing the Fliki scene headings; export the video 1080p.
2. Build the **upload package** for Mark vs Dan (title A/B, description with
   chapters, thumbnail brief, tags).
3. Publish: enable mid-roll ads, add end screen, do NOT mark "Made for Kids".
4. Write **video #2** (another Mark-vs-Dan-style finance story) to build a
   backlog and keep a 1/week cadence.
5. Once Channels B & C exist, log stats into `config/portfolio.json` and run
   `curate` to start the A/B/C test.

## How to regenerate things locally
```bash
# The channel script files
cd channel-studio
PYTHONPATH=src python examples/mark_vs_dan_script.py

# A book interior
cd pod-puzzle-studio
PYTHONPATH=src python -m pod_studio.cli --config config/book.example.json --out output/book.pdf
```

## Reminders / honest caveats
- Finance content = **general education, not advice**; disclaimers are baked in.
- Plan for **~6 months of unpaid runway** before AdSense meaningfully pays.
- Consistency (1 video/week) matters more than any single video.
- All Higgsfield images are in your **app feed** — I can't pull them into the
  repo (the environment blocks Higgsfield's image CDN).
