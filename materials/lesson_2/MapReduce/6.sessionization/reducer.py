#!/usr/bin/env python3
import os
import sys

SESSION_GAP_MIN = int(os.environ.get("SESSION_GAP", "30"))
GAP_SEC = SESSION_GAP_MIN * 60

current_user = None
timestamps = []

def flush():
    if current_user is None:
        return

    if not timestamps:
        print(f"{current_user}\t0")
        return

    timestamps.sort()

    sessions = 1
    prev = timestamps[0]
    for ts in timestamps[1:]:
        if ts - prev > GAP_SEC:
            sessions += 1
        prev = ts

    print(f"{current_user}\t{sessions}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    user_id, ts_s = line.split("\t", 1)
    try:
        ts = int(ts_s)
    except ValueError:
        continue

    if current_user is None:
        current_user = user_id

    if user_id != current_user:
        flush()
        current_user = user_id
        timestamps = []

    timestamps.append(ts)

flush()