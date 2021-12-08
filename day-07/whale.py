#! /usr/bin/env python

import sys
from multiprocessing import Pool

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

crabs = tuple(map(int, lines[0].split(',')))

def fuel_part1(med: int) -> tuple:
    return (sum(abs(i-med) for i in crabs), med)

with Pool() as pool:
    print("Part 1:", min(pool.imap_unordered(fuel_part1, range(0, max(crabs)+1))))

def fuel_part2(med: int) -> tuple:
    return (sum(sum(range(1, abs(i-med)+1)) for i in crabs), med)

with Pool() as pool:
    print("Part 2:", min(pool.imap_unordered(fuel_part2, range(0, max(crabs)+1))))
