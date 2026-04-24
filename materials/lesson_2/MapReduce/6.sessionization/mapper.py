#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 3:
        continue

    user_id, ts, _event_type = parts

    # reducer will sort timestamps внутри user_id
    print(f"{user_id}\t{ts}")