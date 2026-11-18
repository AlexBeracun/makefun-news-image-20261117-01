# makefun-news-image-20261117-01

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/AlexBeracun/makefun-news-image-20261117-01/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/AlexBeracun/makefun-news-image-20261117-01/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image that sums up the world news of **Tuesday, 17 November 2026**: a
newspaper front page ("The World in One Day") led by Ukraine's strike on the
Kerch Bridge and Russia's retaliatory strikes on Kyiv's bridges, with six
more stories across regions and fields — US AI chip curbs on China, the
Xi–Putin–Trump trilateral set for APEC Shenzhen, five EU states' Rwanda
return-hub plan, Japan scrambling jets over Russian aircraft, the Western call
to open Gaza aid crossings, and Mongolia's president resigning — plus a footer
of three further items from the day. Every story was cross-checked against at
least two reports of 17 November 2026.

## How the image was made

`entry.png` (1024×1024, ~130 KB) was drawn locally by `draw_news.py` with
Pillow and the DejaVu fonts: flat vector-style panels and icons, no
photographs, no AI-generated imagery, so every word is crisp and legible.
The graded program does not draw anything — it only copies the finished
image, so both graded runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Node 22, standard library only, no network. `main.ts` copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) and verifies the copied
file opens with the PNG signature.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ajkq5baq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
