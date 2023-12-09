#!/usr/bin/env python3
import sys

if __name__ == '__main__':
    for line in sys.stdin:
        sys.stdout.write(line.upper());
        sys.stdout.flush()
