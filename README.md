# Friday 20 November 2026: 37 stories, 6 continents, one front page (v4)

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/haidildariell/news-image-20261120-v4/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/haidildariell/news-image-20261120-v4/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A single 1024×1024 newspaper front page summing up Friday 20 November 2026,
rendered entirely by one Python/Pillow program (`build_image.py`) — no external
images, no network at build or run time. Version 4 is a legibility upgrade:
every illustrated banner carries one dominant in-banner word or number stating
its story's key fact, plus a small source chip, and the briefs lead with bold
red place names so the page stays readable at about 300 pixels across.

## Layout

- Masthead, red italic subhead, and a six-number stat strip (370,000+ evacuated
  ahead of Cyclone Akvan; 3 Dnipro bridges hit; −7% Asia shares; 2.3% Japan CPI;
  118 by Phillips; 60.7% on daraxonrasib + chemo).
- A coloured region strip whose segments sum to the 37 stories: Europe 8 ·
  Americas 7 · Asia-Pacific 8 · Mideast 5 · Africa 3 · Oceania 4 · World/Space 2.
- Three illustrated lead cards (Cyclone Akvan landfall in Odisha, the overnight
  ballistic-missile barrage on Kyiv, COP31's deadlocked final day in Antalya),
  each with a rich frame-filling flat-art banner.
- Ten mid cards in two rows of five (markets, Mercury, Brussels, Tokyo,
  Beijing, Wellington, Rome, Mato Grosso, Barcelona, Turin). Each banner is a
  layered scene with ONE dominant hero element (≥26px bold — "−7%", "6BN
  MILES", "RESET TALKS", "2.3%", "3.00% / 3.50%", "118", "100 SQUARES",
  "ANCESTRAL LANDS", "60.7%", "ATP FINALS") and a navy source chip in the
  banner's top-right corner.
- Bottom block: a filled-silhouette world map ("WHERE IT HAPPENED") with red
  numbered pins 1–13, beside "ALSO ON FRIDAY 20 NOVEMBER — 24 MORE STORIES":
  numbered one-liners 14–37 in two columns, each led by its place in bold red
  small caps with the source in parentheses.
- A TOMORROW strip, a DATE CHECK box listing items first reported on Thursday
  19 November (and therefore NOT shown as Friday's news), and an attribution
  footer.

## Honesty

Every story here happened, or was first reported, on Friday 20 November 2026
in at least one time zone. Claims are attributed, not stated as fact — each
story names its sources on the page and in [SOURCES.md](SOURCES.md). Verified
numbers are printed exactly as reported: Akvan's winds are 70–80 km/h gusting
90 and 370,000 people were evacuated; no missile count is printed for Kyiv
because none was verified; daraxonrasib's 60.7% comes from an early trial with
no chemo-only comparison, and the page says so. BepiColombo reached Mercury on
Friday; its orbit insertion is Saturday's event and is flagged as tomorrow's.
All artwork is original vector-style drawing made with Pillow primitives.

## Build & run

```sh
python3 build_image.py   # renders entry.png (1024×1024, deterministic)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

Requires Python 3.13 and Pillow only. Running `build_image.py` twice produces
byte-identical output.
