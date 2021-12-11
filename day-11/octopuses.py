#! /usr/bin/env python

import sys
from collections import defaultdict
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

cave = defaultdict(int)
height, width = len(lines), len(lines[0])

for y,line in enumerate(lines):
    for x in range(width):
        cave[x,y] = int(line[x])

def print_cave():
    for y in range(height):
        print("".join(str(cave[x,y]) for x in range(width)))

def flash(x,y):
    cave[x,y]=0
    for a,b in product(range(-1,2), repeat=2):
        if (a,b) != (0,0):
            cave[x+a,y+b]+=1

nb_flashes = 0
for step in range(100):
    # print(f"---- Step {step} ----"); print_cave();
    for c in product(range(width), range(height)):
        cave[c]+=1

    has_flashed = set()
    while len(nines:=tuple(c for c in product(range(width), range(height)) if cave[c]>9)) > 0:
        for c in nines:
            if c not in has_flashed:
                flash(*c)
                has_flashed.add(c)
    for c in has_flashed:
        cave[c] = 0

    nb_flashes += len(has_flashed)

# print(f"---- Step {step+1} ----"); print_cave();
print("Part 1:", nb_flashes)

try:
    while True:
        step+=1
        for c in product(range(width), range(height)):
            cave[c]+=1

        has_flashed = set()
        while len(nines:=tuple(c for c in product(range(width), range(height)) if cave[c]>9)) > 0:
            for c in nines:
                if c not in has_flashed:
                    flash(*c)
                    has_flashed.add(c)
        for c in has_flashed:
            cave[c] = 0

        if len(has_flashed)==100:
            raise StopIteration

except StopIteration:
    # print(f"---- Step {step+1} ----"); print_cave();
    print("Part 2:", step+1)