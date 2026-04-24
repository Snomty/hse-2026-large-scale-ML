#!/usr/bin/env python3
import sys

def bucket(x: int) -> str:
    if 0 <= x < 10:
        return "0-10"
    if 10 <= x < 50:
        return "10-50"
    if 50 <= x < 100:
        return "50-100"
    if 100 <= x < 500:
        return "100-500"
    if 500 <= x < 1000:
        return "500-1000"
    return "1000+"

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 2:
        continue

    _request_id, rt_s = parts
    try:
        rt = int(rt_s)
    except ValueError:
        continue

    b = bucket(rt)
    print(f"{b}\t1")