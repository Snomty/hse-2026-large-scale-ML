#!/usr/bin/env python3
import sys

def main() -> None:
  current_key: str | None = None
  current_sum = 0

  for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
      continue

    key, val = line.split("\t", 1)
    v = int(val)

    if current_key is None:
      current_key = key

    if key != current_key:
      print(f"{current_key}\t{current_sum}")
      current_key = key
      current_sum = 0

    current_sum += v

  if current_key is not None:
    print(f"{current_key}\t{current_sum}")

if __name__ == "__main__":
  main()