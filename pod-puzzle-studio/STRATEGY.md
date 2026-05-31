# Launch Playbook — Automated YouTube + POD Puzzle/Activity Shop

This is the business side. The repo's code builds the *product*; this doc is the
*strategy* for the channel that sells it.

---

## The core principle

The YouTube channel's job is **not** ad revenue — it's a **funnel** to the shop.
That single decision rules out chasing high-RPM niches (finance, etc.) that
don't connect to the product. Every video should make a viewer want the book.

Two income layers, in priority order:
1. **Book sales** (KDP royalties ~$2–4/book + Etsy digital ~$5–8/download).
2. **Ad revenue** (bonus, once monetized — but see the COPPA warning below).

---

## ⚠️ Two compliance landmines (read first)

1. **YouTube's mass-AI policy (July 2025).** Mass-produced, template AI videos
   with no creative input are **demonetized**. "AI slop + robot voice" is
   suppressed. Fix: every video needs a real hook/creative angle. AI-*assisted*,
   not AI-*autopilot*.
2. **COPPA / "Made for Kids".** If you target **kids 3–5**, YouTube law forces
   you to mark videos "Made for Kids," which **disables**: personalized ads
   (much lower RPM), comments, end screens, notifications, and Community posts.
   This **kneecaps the funnel** — you can't easily link to your shop, and the
   audience (kids) can't buy anyway. **The buyer is the parent.**

---

## Channel options (pick 1–2 to start)

| # | Channel | Audience watching | Who buys the book | Funnel strength | COPPA risk |
|---|---------|-------------------|-------------------|-----------------|------------|
| A | **ASMR coloring / page-flip** | Moms (relaxation) | The viewer herself | ⭐⭐⭐⭐⭐ | None |
| B | **Mom self-care / relatable** | Moms | The viewer | ⭐⭐⭐⭐ | None |
| C | **Brain-game "can you solve?"** | Adults | The viewer | ⭐⭐⭐ | None |
| D | **Kids 3–5 learning** (your idea) | Kids + parents | The parent | ⭐⭐ (COPPA-limited) | **High** |
| E | **Paint-mixing satisfying** (your idea) | Broad/all ages | Depends | ⭐⭐ if generic | Medium* |

\*Paint-mixing aimed at toddlers/learning colors often gets auto-flagged "Made
for Kids."

### How your two new ideas fit

- **Kids 3–5 content** is a *great product* idea and a *tricky channel* idea.
  - ✅ **Product:** activity books for 3–5 (big-line coloring, dot-to-dot,
    simple mazes, "trace the letter") sell extremely well — **the parent is the
    buyer**, which is still your "moms" customer. The generator already does
    mazes/coloring; dot-to-dot + tracing are on the roadmap.
  - ⚠️ **Channel:** going *directly* at toddlers triggers COPPA and breaks the
    funnel. **Better play:** make a **"activities for your 3–5 year old"
    channel aimed at the *parent*** ("5 quiet-time activities that actually
    work", "screen-free busy book flip-through"). Parent-facing = funnel intact,
    no COPPA penalty, and it sells the kids' activity book.

- **Paint-mixing / color-mixing satisfying videos** are a strong *format*, not a
  niche on their own.
  - ✅ As **ASMR/satisfying B-roll** they're proven viral and pair perfectly
    with **Channel A** (mix paint → reveal a colored version of one of your
    coloring pages). Higgsfield can generate the satisfying mix clips.
  - ⚠️ As a standalone "learn colors" toddler channel they drift into COPPA + a
    crowded, hard-to-monetize space.
  - **Verdict:** use paint-mixing as a *hook/transition* inside the coloring
    channel, not as its own channel.

### Recommendation

**Start with Channel A (ASMR coloring), using paint-mixing clips as hooks.**
It's the only option where: the content *is* the product demo, your Higgsfield
subscription is a real edge, there's zero COPPA risk, and the funnel is
unbroken. Add a **parent-facing kids-activity** angle (Channel D-reframed) as a
second book line once the first is selling.

---

## The production pipeline (per video)

1. **Generate the book** → `pod_studio.cli` → PDF + `prompts.json`.
2. **Make the art** → feed `prompts.json` image prompts to Higgsfield
   (Nano Banana / Seedream — unlimited-eligible). Save PNGs, rebuild.
3. **Make the Short** → use the `shorts` plans in `prompts.json`:
   - Hook (0–1.5s) + satisfying color-fill / paint-mix (Higgsfield Kling 3.0).
   - On-screen caption + soft track. Vertical 9:16.
4. **Publish** → title with the keyword ("Bold & Easy Self-Care Coloring"),
   pinned comment + bio link to the Etsy/Amazon listing.
5. **Repeat** 1×/day for 30 days (consistency beats volume).

### Credit economics (your Plus plan = 688 credits)
- **Images** are the workhorse and are *unlimited-eligible* — activate a 365-day
  image unlimited add-on and coloring art/covers cost ~nothing.
- **Video** (Kling 3.0) is unlimited only on the **7-day** pack; otherwise it
  sips credits (~3–5 credits/clip). Budget accordingly or batch in a 7-day
  sprint.

---

## Product / shop setup

- **Format:** 8.5×8.5 square (64% of best-sellers), bold-&-easy lines.
- **Price:** $7.99 paperback (KDP) / $4–6 printable PDF (Etsy).
- **Niche down:** "Cozy Cottagecore Coloring for Tired Moms" beats "Coloring
  Book for Adults." Niche titles do $500–3,000/mo with <500 competitors.
- **Two storefronts:**
  - **Amazon KDP** — physical paperback, print-on-demand, huge search traffic.
  - **Etsy** — instant-download printable PDFs (higher margin, no printing).
- **Keywords:** put the buyer's words in the title/subtitle ("stress relief",
  "self-care gift for mom", "quiet time activity").

## 30-day launch checklist

- [ ] Pick channel angle (recommend A) + first book theme.
- [ ] Generate book #1 interior with the tool.
- [ ] Activate Higgsfield image unlimited add-on; generate coloring art + cover.
- [ ] Design KDP cover (spine from final page count).
- [ ] Publish to KDP + list printable on Etsy.
- [ ] Produce 10 Shorts from the `prompts.json` plans; schedule daily.
- [ ] Add shop link to channel bio + pinned comments.
- [ ] After 2 weeks, check which Shorts performed; double down on that style.
