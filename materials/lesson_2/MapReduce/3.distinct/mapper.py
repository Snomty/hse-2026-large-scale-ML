#!/usr/bin/env python3
import re
import sys

word_re = re.compile(r"[a-z0-9]+")  # простая токенизация как в wordcount: lowercase + без пунктуации

for line in sys.stdin:
    for w in word_re.findall(line.lower()):
        print(f"{w}\t1")