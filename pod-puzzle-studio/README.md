# POD Puzzle Studio 🧩🎨

A niche-agnostic toolkit for the two halves of the business:

1. **The product** — generate print-ready, KDP/Etsy-compliant puzzle, activity
   and coloring book interiors (PDF) from a small config file.
2. **The funnel** — emit a Higgsfield prompt manifest so the coloring art and
   the YouTube Shorts that sell the books can be produced with AI, with a
   human-in-the-loop credit check.

Built in Python with `reportlab` (vector-sharp print output) + `Pillow`.

---

## Why it's built this way

- **Niche-agnostic.** A "niche" is just a [`Theme`](src/pod_studio/themes.py):
  a word list, a list of `(answer, clue)` crossword pairs, and a list of
  coloring-art subjects. Swap those and the same engine makes a book for *any*
  audience — moms, kids 3–5, seniors, cottagecore, etc. No code changes.
- **Puzzles are free.** Word search, sudoku, mazes and crosswords are generated
  algorithmically — **no AI, no credits, infinite books.**
- **Art is AI, but gated.** Coloring line-art and covers come from Higgsfield
  image models (Nano Banana / Seedream / Flux — all *unlimited-eligible* on the
  Plus plan's add-ons). The tool writes the prompts; generation happens through
  the MCP tools so a human always confirms before credits are spent.

## Print compliance (KDP)

[`kdp.py`](src/pod_studio/kdp.py) handles the stuff that gets books rejected:
- Trim sizes (default **8.5×8.5** — 64% of best-selling coloring books).
- **0.125"** bleed for full-page art.
- **Dynamic gutter** that grows with page count so the binding never eats text.
- Mirrored inside/outside margins (gutter flips on odd/even pages).

## Quick start

```bash
cd pod-puzzle-studio
pip install -r requirements.txt
PYTHONPATH=src python -m pod_studio.cli \
    --config config/book.example.json \
    --out output/self_care_sunday.pdf
```

This produces:
- `output/self_care_sunday.pdf` — the book interior (title page, "this book
  belongs to", puzzle sections, answer key, shop CTA page).
- `output/assets/prompts.json` — the Higgsfield manifest: one image prompt per
  coloring page + 3 funnel Short plans, each tagged with the recommended model
  and whether it's unlimited on Plus.

## Adding the AI art

1. Open `output/assets/prompts.json`.
2. For each image, run the prompt through the listed Higgsfield model
   (`generate_image` via MCP — confirm credits first).
3. Save each returned PNG to its `art_path` (e.g.
   `output/assets/art/coloring-self_care-01.png`).
4. Re-run the build. Placeholders are replaced by the real coloring pages.

## Defining a new book / niche

Edit a JSON config (see [`config/book.example.json`](config/book.example.json)):

```json
{
  "title": "Cozy Cottagecore Coloring",
  "subtitle": "Bold & Easy Pages for Tired Moms",
  "trim": "8.5x8.5",
  "theme": "cottagecore",
  "sections": [
    { "type": "coloring",    "count": 20 },
    { "type": "word_search", "count": 10 },
    { "type": "maze",        "count": 5 }
  ]
}
```

Section types: `coloring`, `word_search`, `crossword`, `sudoku`, `maze`.
Built-in themes: `self_care`, `cottagecore`, `parenting`
(add your own in [`themes.py`](src/pod_studio/themes.py)).

## Project layout

```
src/pod_studio/
  kdp.py            # print geometry (trim, bleed, gutter)
  themes.py         # niche content packs (words, clues, art subjects)
  render.py         # draw each puzzle onto the canvas
  coloring.py       # coloring-page layout + art placeholder
  higgsfield.py     # prompt manifest + model/credit guidance
  book.py           # assemble the full interior PDF
  cli.py            # command-line entrypoint
  puzzles/
    word_search.py  sudoku.py  maze.py  crossword.py
config/             # book definitions (data, not code)
output/             # generated PDFs + assets (gitignored)
```

## Roadmap / next steps

- KDP cover wrap generator (spine width from page count).
- Dot-to-dot and "spot the difference" page types (great for kids 3–5).
- Direct MCP automation of the art step (currently human-gated by design).
- Per-puzzle difficulty curves across a book.

See [`STRATEGY.md`](STRATEGY.md) for the channel + shop launch playbook.
