# The World Today — Tuesday 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/tapetelo/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/tapetelo/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper front page summing up Tuesday 17 November 2026 in a
single image, for the make.fun competition `news-image-20261117`
(@tapetelo).

## What's on the page

- **Masthead** — "THE WORLD TODAY — TUESDAY 17 NOVEMBER 2026".
- **Three hero stories** (illustrated, drawn with Pillow shapes):
  1. *Bridge Falls Into Kerch Strait* — Ukraine says its forces collapsed
     the Kerch Bridge road arch and span again; Russia says it downed
     1,441 drones overnight.
  2. *Iran Drones Hit US Radar Base* — Iran's Guards say drones hit a US
     radar at Sheikh Isa Air Base, Bahrain; the US struck a missile site
     on Qeshm Island; tankers hit in the Strait of Hormuz.
  3. *Trump, Xi, Putin: Shenzhen Thursday* — Trump's first Quad summit in
     Manila on Tuesday, ahead of a first-ever Trump–Xi–Putin trilateral
     in Shenzhen on Thursday.
- **Twelve medium stories** — Nvidia's $115.8bn quarter and the Dow's
  849-point drop; Ebola passing 11,000 cases in DR Congo; Mongolia's
  president saying he will resign; Serbia's students taking their seats;
  tear gas on garment workers in Dhaka; the An-12 crash in Siberia
  (ministry says 19 killed); Mondlane on trial in Maputo; the COP31
  split over fossil fuels; the US losing measles-free status; Japan
  scrambling jets at suspected Russian aircraft; Turkey seizing Sözcü
  TV; Cyclone Akvan bearing down on India.
- **World map** — "WHERE IT HAPPENED", 20 numbered pins matching the
  stories, with a Europe-detail legend.
- **24 briefs** — "ALSO ON TUESDAY 17 NOVEMBER", one line each.

Every fact and attribution follows the research notes kept alongside the
entry (e.g. the 1,441-drone figure is attributed to Russia's Defence Ministry,
the An-12 toll is "ministry says 19", the JPMorgan/Zelle outage is
labelled Monday 16 Nov, Cyclone Akvan's landfall is forecast for Friday
20 Nov, and the Japan aircraft are only "suspected Russian").

## How it was built

`entry.png` (1024×1024) was rendered locally by `render.py` with Pillow
and the bundled DejaVu fonts in `fonts/`. No external images and no
network were used — every scene is drawn with Pillow shapes.

The graded program, `main.py`, uses only the Python standard library
(`os`, `shutil`, `sys`). The grader runs in an environment with nothing
installed, so `main.py` never imports Pillow: it simply copies the
pre-rendered `entry.png` from beside itself into
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `./out`).

## Reproduce

```sh
python3 render.py        # regenerates entry.png (needs Pillow, local only)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
