#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n').split())

position, depth = (0, )*2
for action, amount in lines:
    if action=="forward":
        position += int(amount)
    elif action=="up":
        depth -= int(amount)
    elif action=="down":
        depth += int(amount)
print("Part 1:", position*depth)

position, depth, aim = (0, )*3
for action, amount in lines:
    if action=="forward":
        position += int(amount)
        depth += aim*int(amount)
    elif action=="up":
        aim -= int(amount)
    elif action=="down":
        aim += int(amount)
print("Part 2:", position*depth)
