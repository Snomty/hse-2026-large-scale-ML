#!/usr/bin/env python3
import sys

current_user = None
max_ts = None
best_event = None

def flush():
    if current_user is None:
        return
    if max_ts is None or best_event is None:
        return
    print(f"{current_user}\t{max_ts}\t{best_event}")

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 3:
        continue

    user_id, ts_s, event_type = parts
    try:
        ts = int(ts_s)
    except ValueError:
        continue

    if current_user is None:
        current_user = user_id
        max_ts = ts
        best_event = event_type
        continue

    if user_id != current_user:
        flush()
        current_user = user_id
        max_ts = ts
        best_event = event_type
        continue

    # same user, timestamps come in DESC order because of secondary sort
    if ts == max_ts:
        # tie-break: lexicographically max event_type
        if event_type > best_event:
            best_event = event_type
    else:
        # ts < max_ts => older; ignore
        pass

flush()