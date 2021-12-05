#! /usr/bin/env python

import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

field = defaultdict(int)
for l in lines:
    pt1, pt2 = l.split(' -> ')
    x1,y1 = [ int(i) for i in pt1.split(',') ]
    x2,y2 = [ int(i) for i in pt2.split(',') ]

    if x1==x2:
        for y in range(min(y1,y2), max(y1,y2)+1):
            field[x1,y] += 1
    elif y1==y2:
        for x in range(min(x1,x2), max(x1,x2)+1):
            field[x,y1] += 1

print("Part 1:", sum(c>1 for c in field.values()))

field = defaultdict(int)
for l in lines:
    pt1, pt2 = l.split(' -> ')
    x1,y1 = [ int(i) for i in pt1.split(',') ]
    x2,y2 = [ int(i) for i in pt2.split(',') ]

    if x1==x2:
        for y in range(min(y1,y2), max(y1,y2)+1):
            field[x1,y] += 1
    elif y1==y2:
        for x in range(min(x1,x2), max(x1,x2)+1):
            field[x,y1] += 1
    else:
        sx=(x1<x2)-(x2<x1)
        sy=(y1<y2)-(y2<y1)
        for c in zip(range(x1,x2+sx,sx), range(y1,y2+sy,sy)):
            field[c] += 1

print("Part 2:", sum(c>1 for c in field.values()))
