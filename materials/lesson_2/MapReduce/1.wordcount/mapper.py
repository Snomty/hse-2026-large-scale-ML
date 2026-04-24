#!/usr/bin/env python3
import sys

def main() -> None:
  for line in sys.stdin:
    for w in line.strip().split():
      if w:
        print(f"{w}\t1")

if __name__ == "__main__":
  main()