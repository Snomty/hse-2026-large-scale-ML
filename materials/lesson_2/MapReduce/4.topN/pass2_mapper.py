#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    word, cnt = line.split("\t", 1)
    cnt = int(cnt)

    # all records to one reducer (key = "top")
    print(f"top\t{cnt}\t{word}")