#!/usr/bin/env python3
import sys

prev = None
s = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, val = line.split("\t", 1)
    v = int(val)

    if prev is None:
        prev = key
        s = v
    elif key == prev:
        s += v
    else:
        print(f"{prev}\t{s}")
        prev = key
        s = v

if prev is not None:
    print(f"{prev}\t{s}")