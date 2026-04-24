#!/usr/bin/env python3
import sys

def main() -> None:
    total = 0

    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue

        # Expect: key \t value
        if "\t" in line:
            _key, value = line.split("\t", 1)
        else:
            # fallback (shouldn't happen in this demo)
            value = "1"

        try:
            total += int(value)
        except ValueError:
            pass

    # unified output format: "lines <count>"
    sys.stdout.write(f"lines {total}\n")

if __name__ == "__main__":
    main()