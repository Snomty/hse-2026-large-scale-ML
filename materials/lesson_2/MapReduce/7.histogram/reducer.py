#!/usr/bin/env python3
import sys

prev = None
s = 0

def emit(k, v):
    print(f"{k}\t{v}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    k, v = line.split("\t", 1)
    v = int(v)

    if prev is None:
        prev = k
        s = v
    elif k == prev:
        s += v
    else:
        emit(prev, s)
        prev = k
        s = v

if prev is not None:
    emit(prev, s)