# Today in the World — 21 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/)
[![@Schyd](https://img.shields.io/badge/@Schyd-make.fun-green)](https://make.fun/u/schyd)
[![news-image-20261121](https://img.shields.io/badge/news--image--20261121-bounty-orange)](https://make.fun/bounty/news-image-20261121)

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
