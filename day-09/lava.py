#! /usr/bin/env python

import sys
from collections import defaultdict
from itertools import product
from functools import reduce
from heapq import nlargest

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

cave = defaultdict(lambda: 9)
height, width = len(lines), len(lines[0])
for y,l in enumerate(lines):
    for x,i in enumerate(l):
        cave[x,y]= int(i)

low_points = []
for (x,y) in product(range(width), range(height)):
    if all(cave[x,y] < cave[v] for v in ((x-1,y), (x+1,y), (x,y-1), (x,y+1))):
        low_points.append((x,y))
print("Part 1:", sum(1+cave[c] for c in low_points))

basins = []
for lp in low_points:
    basin = set()
    candidates = [lp]
    while candidates:
        x,y = candidates.pop()
        if cave[x,y] < 9:
            basin.add((x,y))
            candidates.extend(v for v in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)) if v not in basin)
    basins.append(basin)

# for y in range(height):
#     print("".join(
#         str(cave[x,y]) if any((x,y) in b for b in basins) else " "
#         for x in range(width)
#         )
#     )
print("Part 2:", reduce(lambda x,y: x*y, nlargest(3, (len(b) for b in basins))))
