#!/usr/bin/env python3
import sys

current_user = None
name = None
country = None
buffered_events = []

def flush():
    if current_user is None:
        return
    if name is None or country is None:
        # inner join: no user -> skip events
        return
    for ts, ev in buffered_events:
        print(f"{current_user}\t{name}\t{country}\t{ts}\t{ev}")

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) < 2:
        continue

    user_id = parts[0]
    tag = parts[1]  # "0" (user) or "1" (event)

    if current_user is None:
        current_user = user_id

    if user_id != current_user:
        flush()
        current_user = user_id
        name = None
        country = None
        buffered_events = []

    if tag == "0":
        # user record: user_id 0 name country
        if len(parts) >= 4 and name is None:
            name = parts[2]
            country = parts[3]
        # if duplicate user rows -> ignore after first

    elif tag == "1":
        # event record: user_id 1 ts ev
        if len(parts) >= 4:
            ts = parts[2]
            ev = parts[3]
            buffered_events.append((ts, ev))

flush()