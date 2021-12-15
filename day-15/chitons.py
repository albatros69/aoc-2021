#! /usr/bin/env python

import sys
from itertools import product
from collections import defaultdict
from heapq import heappush, heappop

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

cave = defaultdict(lambda: -1)
for y,l in enumerate(lines):
    for x,risk in enumerate(l):
        cave[(x,y)] = int(risk)
max_x, max_y = len(lines[0]), len(lines)

def search_path(cave):
    exit_pos = max(cave)
    queue = [ (0, (0,0)) ]
    already_seen = set((0,0))
    while queue:
        risk, pos = heappop(queue)

        if pos == exit_pos:
            break
        else:
            for v in ((i,j) for (i,j) in ((0,1), (0,-1), (1,0), (-1,0))):
                new_pos = pos[0]+v[0], pos[1]+v[1]
                if cave[new_pos]>=0 and new_pos not in already_seen:
                    already_seen.add(new_pos)
                    heappush(queue, (risk+cave[new_pos], new_pos))

    return risk

print("Part 1:", search_path(cave))

for y in range(5*max_y):
    if y>=max_y:
        for x in range(max_x):
            cave[x,y]=cave[x,y-max_y]+1
            if cave[x,y]>9:
                cave[x,y]=1

    for x in range(max_x, 5*max_x):
        cave[x,y]=cave[x-max_x,y]+1
        if cave[x,y]>9:
            cave[x,y]=1
# print("\n".join(
#     "".join(str(cave[x,y]) for x in range(5*max_x)) for y in range(5*max_y)
# ))

print("Part 2:", search_path(cave))

