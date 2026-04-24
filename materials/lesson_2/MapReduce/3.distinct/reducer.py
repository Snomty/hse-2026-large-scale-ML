#!/usr/bin/env python3
import sys

prev_key = None
distinct = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    # ожидаем: key\tvalue (value не важен)
    key = line.split("\t", 1)[0]

    if key != prev_key:
        distinct += 1
        prev_key = key

print(f"distinct_words {distinct}")