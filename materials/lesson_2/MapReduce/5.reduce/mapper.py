#!/usr/bin/env python3
import os
import sys

def input_basename() -> str:
    # MRv2:
    p = os.environ.get("mapreduce_map_input_file", "")
    # MRv1 fallback:
    if not p:
        p = os.environ.get("map_input_file", "")
    # examples: "file:/.../users.tsv" or "/.../users.tsv" or "users.tsv"
    p = p.replace("file:", "")
    return os.path.basename(p)

src = input_basename()

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue

    parts = line.split("\t")

    if src == "users.tsv":
        # user_id<TAB>name<TAB>country
        if len(parts) != 3:
            continue
        user_id, name, country = parts
        # tag 0 so user record sorts before events within the same key
        print(f"{user_id}\t0\t{name}\t{country}")

    elif src == "events.tsv":
        # user_id<TAB>timestamp<TAB>event_type
        if len(parts) != 3:
            continue
        user_id, ts, ev = parts
        # tag 1 so events go after user record
        print(f"{user_id}\t1\t{ts}\t{ev}")

    else:
        # unknown input file (skip)
        continue