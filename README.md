# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/argasap87/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/argasap87/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the make.fun bounty
[`news-image-20261120`](https://make.fun/bounty/news-image-20261120)
("Sum up 20 November's world news in one image", $250, 50 places).

A five-sector "cyclone wheel" infographic, drawn programmatically with
Python/PIL, that sums up Friday 20 November 2026 in one 1024×1024 image.
The day's storm — Cyclone Akvan — is the wheel itself: five colour-coded
sectors spin out from a central date medallion, one per story, over faint
concentric storm rings. Every word is drawn as text, so nothing is
misspelled and everything stays legible at thumbnail size.

## The five stories (each verified as happening / first reported on 20 Nov 2026)

1. **Akvan hits Odisha — Cyclone Akvan makes landfall near Gopalpur.**
   Severe cyclone crosses the coast at noon, winds 100 km/h, gusts 110;
   105,000+ people evacuated to shelters.
   Source: India Meteorological Department, via Reuters / India Today, 19–20 Nov 2026.
2. **Students walk out — International Youth Strike.**
   Young people walk out of schools and universities across Europe and
   the UK: "Fight for our futures, not their wars."
   Source: Socialist Party / Socialist Students, 18–19 Nov 2026 (walkouts on 20 Nov).
3. **Albanese meets Xi — Australia's PM meets China's president in Shenzhen.**
   Their fifth formal meeting, on APEC week; Albanese also holds his
   annual leaders' meeting with Premier Li Qiang.
   Source: VNN / Australian reporting, 18 Nov 2026 (meeting on Friday 20 Nov).
4. **Nicholls 146\* — New Zealand reach 317/6 on Day 2 in Wellington.**
   First Test vs India: Nicholls 146 not out at lunch on Day 2; Glenn
   Phillips 118 — a century against India in all three formats in 2026.
   Source: Cricbuzz live / ICC, 20 Nov 2026.
5. **World Children's Day — 20 November marks the UN day for children's rights.**
   The date the Convention on the Rights of the Child was adopted in 1989.
   Source: United Nations observance, 20 November (annual).

Stories from other days were deliberately excluded: the Trump–Xi–Putin
trilateral, the ICJ Myanmar genocide ruling, the Kyiv embassy strikes and
the Han Duck-soo ruling all happened on 19 November; the Fiji drought
disaster declaration and the US–Venezuela military deal were 18 November.

## How to run

```sh
node main.ts            # writes entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

`main.ts` (Node 22, standard library only) copies `entry.png` beside it to
`$MAKEFUN_OUTPUT_DIR/entry.png`, fails loudly if the copy is short or the
bytes differ, and logs the bytes written.

## Output

- `entry.png` — 1024×1024 PNG, 135,368 bytes (under the 1 MiB limit).
- `draw.py` — the script that drew the infographic from scratch with PIL.
