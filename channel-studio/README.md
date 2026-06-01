# Channel Studio 📈🎙️

A standalone system for **faceless long-form YouTube channels monetized by
AdSense** — decoupled from the POD shop (different audience, different goal).

Built around three hard truths from June 2026 RPM data:

1. **Long-form (8+ min) earns ~30× more than Shorts** ($3–15 RPM vs $0.05–0.20),
   because 8+ minutes unlocks multiple mid-roll ads + a 55% rev share.
2. **Finance is the highest-RPM, most faceless-friendly niche** ($15–22 RPM;
   visuals are just charts + text + stock B-roll + AI voice).
3. **Lazy AI mass-production is demonetized** (YouTube July 2025 policy) — so
   this tool produces *scaffolds + prompts*, keeping a human in creative control.

## The strategy: run the top 3 niches in parallel

The top niches are within a few RPM points, so instead of guessing, **launch one
channel per niche and let real performance pick the winner**, then a **curator**
tells you where to double down.

```
Channel A — Personal Finance      ($15–22 RPM)
Channel B — Make Money Online      ($15–20 RPM)
Channel C — Legal / Know Your Rights ($12–18 RPM)
        │
        ▼
   curator  →  DOUBLE_DOWN / HOLD / CUT
```

## Commands

```bash
cd channel-studio

# 1. See the ranked high-RPM niches
PYTHONPATH=src python -m channel_studio.cli niches

# 2. Generate a content backlog for a niche
PYTHONPATH=src python -m channel_studio.cli ideas --niche personal_finance --count 15

# 3. Build a full production brief for one video (script scaffold + LLM prompts
#    + timed visual cues + SEO metadata + mid-roll markers)
PYTHONPATH=src python -m channel_studio.cli plan \
    --niche personal_finance \
    --topic "How Index Funds Actually Work (Explained Simply)" \
    --minutes 10 --out output/index_funds.json

# 4. Score the A/B/C test once you have metrics
PYTHONPATH=src python -m channel_studio.cli curate \
    --portfolio config/portfolio.example.json --out output/curator_report.json
```

## What a production brief contains

- **Script scaffold**: 0–15s hook, 15–30s promise/open-loop, 4–7 timed content
  segments, recap + subscribe outro.
- **Per-segment LLM prompts**: paste into Claude/ChatGPT to write the prose —
  you keep creative direction (required for monetization).
- **Mid-roll markers**: exact seconds (only after 8:00, spaced, on segment
  boundaries) so ads never cut a sentence.
- **Visual cue list**: timed charts / text overlays / stock B-roll / screen
  recordings matched to each segment.
- **Upload metadata**: SEO title, chaptered description, tags, thumbnail brief.
- **Niche disclaimer**: auto-included for finance/legal (advertiser safety).

## The production stack (cheap faceless long-form)

| Step | Tool | Notes |
|------|------|-------|
| Script prose | Claude / ChatGPT | Fill each segment's `llm_prompt` |
| Voiceover | ElevenLabs v3 | Calm explainer voice |
| Visuals | Canva / AE charts + Pexels/Storyblocks B-roll | No generative video needed |
| Assembly | Any NLE | Captions on (retention) |
| Upload | YouTube Studio | Enable mid-rolls, end screens |

> Note: Higgsfield generative video is **not** the core here — high-RPM
> explainer content wins on clear charts, not cinematic clips. Save Higgsfield
> credits for the POD shop side (coloring art) where they add real value.

## The curator scoring model

A composite 0–100 score per channel, weighted toward the signals that drive
durable AdSense income:

- **Revenue 40%** · **Retention 25%** · **RPM 20%** · **CTR 15%**

Recommendations: `KEEP_TESTING` (<5 videos), `DOUBLE_DOWN` (≥85% of best),
`HOLD` (≥50%), `CUT` (<50%). Update `config/portfolio.json` from YouTube Studio
(or wire the Analytics API later) and re-run `curate` weekly.

## ⚠️ Compliance notes

- Finance/legal content is **general education, not advice** — disclaimers are
  auto-added; keep claims careful and avoid specific buy/sell calls.
- Keep real creative input in every video (the tool gives scaffolds, not
  publish-ready slop) to stay monetizable under YouTube's 2026 policy.

## Layout

```
src/channel_studio/
  niches.py       # RPM data + content-idea engine
  script.py       # long-form script scaffolding (8+ min, mid-roll aware)
  production.py   # voice + visuals + SEO production brief
  curator.py      # multi-channel A/B/C scoring + recommendations
  cli.py          # niches | ideas | plan | curate
config/           # portfolio + per-video configs
output/           # generated briefs + curator reports
```
