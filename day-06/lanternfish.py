#! /usr/bin/env python

import sys
from collections import Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

fishes = [ int(i) for i in lines[0].split(',') ]

status = Counter(fishes)
# print("Initial state:", status)
for day in range(256):
    new_status = Counter()
    for i in status:
        if i==0:
            new_status.update({6: status[i], 8: status[i], 0: 0})
        else:
            new_status.update({i-1: status[i]})
    status = new_status
    if day==79:
        print("Part 1:", sum(status.values()))

print("Part 2:", sum(status.values()))
