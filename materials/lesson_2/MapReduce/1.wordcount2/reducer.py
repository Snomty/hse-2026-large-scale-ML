#!/usr/bin/env python3
import sys

def main() -> None:
  cur_prefix: str | None = None
  cur_word: str | None = None

  # сколько раз встретилось текущее слово (внутри prefix)
  cur_word_sum = 0

  # агрегаты по prefix
  unique_words = 0
  total_words = 0

  def flush_word() -> None:
    nonlocal unique_words, total_words, cur_word_sum, cur_word
    if cur_word is None:
      return
    unique_words += 1
    total_words += cur_word_sum
    cur_word_sum = 0

  def flush_prefix() -> None:
    nonlocal cur_prefix, unique_words, total_words
    if cur_prefix is None:
      return
    print(f"{cur_prefix} {unique_words} {total_words}")
    unique_words = 0
    total_words = 0

  for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
      continue

    prefix, word, val = line.split("\t", 2)
    v = int(val)

    if cur_prefix is None:
      cur_prefix, cur_word = prefix, word

    if prefix != cur_prefix:
      flush_word()
      flush_prefix()
      cur_prefix, cur_word = prefix, word
      cur_word_sum = 0
    elif word != cur_word:
      flush_word()
      cur_word = word

    cur_word_sum += v

  flush_word()
  flush_prefix()

if __name__ == "__main__":
  main()