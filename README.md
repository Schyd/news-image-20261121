# Today in the World — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Schyd/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Schyd/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-day newspaper front page that sums up the world's news of
**Saturday 21 November 2026** in a single image: 48 stories across 8 regions
and 13 fields — 4 illustrated lead stories, 12 illustrated mid stories, a
big-number strip, a numbered world map, 32 more stories in the "Also on"
list, and a DATE CHECK box naming the big older stories left out on purpose.

Built for the [news-image-20261121 bounty](https://make.fun/bounty/news-image-20261121)
on [make.fun](https://make.fun/), entered as
[@Schyd](https://make.fun/u/schyd).

## How it works

`main.py` is a single Python 3.13 program using only the standard library.
It draws the whole front page itself — its own 5x7 bitmap font and its own
PNG encoder (zlib + struct) — and writes `entry.png` (1024x1024, under 1 MiB).
No network, no files read, no randomness: two runs write identical bytes.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
