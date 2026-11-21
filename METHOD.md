# Method — news-image-20261121

## What the entry is

A Python 3.13 program (`main.py`, Pillow for drawing) that renders a
one-page newspaper front page — "THE WORLD, Saturday 21 November 2026" —
and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).
It reads nothing, uses no network, and is fully deterministic: fixed
layout, fixed palette, fixed shapes, no randomness, no timestamps.

## Layout

- Masthead with the date (Saturday 21 November 2026).
- Lead hero: GTA VI launch weekend, with a programmatically drawn Vice
  City sunset skyline (gradient sky, sun, tower silhouettes with lit
  windows, palm silhouettes, water with reflections).
- Second hero: Cyclone Akvan (drawn cyclone swirl + rain).
- "Around the World": trilateral declaration (20 Nov), Houthi missile
  over Riyadh (20 Nov), ICJ ruling on Myanmar (19 Nov).
- "Also on the wires": Anthropic IPO priced at $81.34bn (19 Nov),
  Anthropic $1.5tn valuation report (20 Nov), Crimean Bridge third hit
  this week (20 Nov), GTA VI launch prices (19 Nov).
- "Where it happened": stylised world map with dots for Vice City,
  Crimea, Riyadh, Myanmar.
- Red "GTA 6 SCAMS" strip (fake free-copy pages, bogus PC installers,
  20,000+ GTA-themed tokens, 8,800+ flagged malicious).
- "DATE CHECK" box listing the verified date of every story.

## Research note — IMPORTANT, read before submitting

The web search tool was unavailable during this build session (two
consecutive `browser_search` failures, both `web_search failed`), so no
fresh 21 November wire reporting could be pulled. Every story and figure
in the image is grounded in reporting verified on 19–20 November 2026:

- GTA VI launched Thursday 19 November on PS5 / Xbox Series X|S,
  $79.99 standard / $99.99 ultimate; no PC version, demo, beta or early
  access; scam campaign (fake Google logins, infostealer installers,
  20,000+ GTA-themed Solana tokens, 8,800+ malicious/warning/spam)
  per the Airdrop Finder article shared 20 Nov.
- Cyclone Akvan: 300,000 evacuated (reported 20 Nov).
- ICJ Myanmar genocide ruling: 19 Nov. Anthropic $81.34bn IPO: 19 Nov.
  Anthropic $1.5tn valuation report: 20 Nov. Trilateral meeting 19 Nov,
  joint declaration issued 20 Nov. Crimean Bridge span fell 17–18 Nov,
  third hit this week reported 20 Nov. Houthi missile at Riyadh KAFD:
  20 Nov.

The lead story (GTA VI launch weekend) is genuinely a 21 November story
— Saturday is the first weekend day after the 19 Nov launch. The other
stories are developing carry-overs, each labelled on the image with its
verified date, and the DATE CHECK box states the 19–20 Nov sourcing
plainly. Before submitting, re-check the day's wires and replace any
headline that fresh 21 November reporting supersedes — the story text
lives in one place in `main.py` (the hero/mini/wire strings), so a swap
is a small edit followed by a re-run.

## Determinism

Verified 21 Nov 2026: three runs (repo dir, /tmp/det1, /tmp/det2) all
produced byte-identical `entry.png`.

- sha256: `90db53ecfc181c762f48d1bec1af613a131547e08edca0ec1c7283704c83d00a`
- size: 120,794 bytes (< 1 MiB), 1024×1024 PNG.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=output python3 main.py
```
