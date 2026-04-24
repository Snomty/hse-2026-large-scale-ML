#!/usr/bin/env python3
import sys

def main() -> None:
    # One record per input line
    for _line in sys.stdin:
        # constant key so everything aggregates together
        sys.stdout.write("lines\t1\n")

if __name__ == "__main__":
    main()