#!/usr/bin/env python3
import sys

# output: user_id <TAB> timestamp <TAB> event_type
# With stream.num.map.output.key.fields=2, (user_id, timestamp) becomes the key.
for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 3:
        continue

    user_id, ts_s, event_type = parts

    # Keep timestamp numeric-friendly; comparator will use numeric sort anyway.
    # (Optional) validate it's int:
    try:
        int(ts_s)
    except ValueError:
        continue

    print(f"{user_id}\t{ts_s}\t{event_type}")