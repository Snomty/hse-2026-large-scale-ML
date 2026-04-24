#!/usr/bin/env python3
import sys
import re

def main() -> None:
  for line in sys.stdin:
    for word in re.findall(r"\w+", line.lower()):
      if not word:
        continue
      prefix2 = word[:2] if len(word) >= 2 else word
      # 3 поля: prefix2, word, 1
      print(f"{prefix2}\t{word}\t1")

if __name__ == "__main__":
  main()