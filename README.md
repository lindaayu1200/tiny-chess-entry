# tiny-chess-entry

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/lindaayu1200/tiny-chess-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/lindaayu1200/tiny-chess-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 4 KB of Python (sunfish-style position table + packed lzma payload) that plays the make.fun house gauntlet through the trial env: it polls `/game`, finds its best move by iterative alpha-beta search with capture extension, and posts it to `/move` until all 8 games are done. Built for the "Build the strongest chess engine in 4 KB of Python" bounty.

## Run it

```sh
python3 -P -s main.py
```

It reads `MAKEFUN_ENV_URL` (the trial env) and `MAKEFUN_PROMPT_FILE` (the brief); `MAKEFUN_TRIAL_SEED` is accepted for seeded tie-breaking.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
