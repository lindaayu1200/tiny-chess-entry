# Self-test

From the repository root:

```sh
node /root/makefun-setup/tchess-kit2/tiny-chess-01-kit/cli/makefun.mjs compress engine_src.py --out main.py
wc -c main.py   # must be at most 4096
git diff --exit-code main.py   # packed payload must match the source byte for byte
python3 -c "import engine_src as e; p=e.A5('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'); print(p)"   # engine parses the start position
```

A pass is: main.py is 4,096 bytes or fewer, git reports no change after the compress, and the engine's position parser prints a Position built from the standard start FEN.
