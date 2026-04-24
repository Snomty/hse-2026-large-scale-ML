#!/usr/bin/env python3
import os
import sys

TOP_N = int(os.environ.get("TOP_N", "3"))

items = []
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    _top, cnt_s, word = line.split("\t", 2)
    items.append((int(cnt_s), word))

# sort: count desc, word asc
items.sort(key=lambda x: (-x[0], x[1]))

for cnt, word in items[:TOP_N]:
    print(f"{word} {cnt}")