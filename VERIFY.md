# Self-test

From the repository root:

```sh
node /root/makefun-setup/tchess-kit2/tiny-chess-01-kit/cli/makefun.mjs compress engine_src.py --out main.py
wc -c main.py   # must be at most 4096
git diff --exit-code main.py   # packed payload must match the source byte for byte
python3 -c "import ast; ast.parse(open('engine_src.py').read()); print('source-parse-ok')"
```

A pass is: main.py is 4,096 bytes or fewer, git reports no change after the compress, and the packed source parses as valid Python.
