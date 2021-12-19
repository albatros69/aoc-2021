#! /usr/bin/env python

from __future__ import annotations
import sys
import numpy as np
from itertools import permutations, product
from collections import Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


transformations_matrix = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for q in permutations([[x,0,0], [0,y,0], [0,0,z]]):
                m = np.array(q, dtype=int)
                if np.linalg.det(m) == 1:
                    transformations_matrix.append(m)


class Scanner:
    id = None
    position = np.zeros(3, dtype=int)
    beacons = None

    def __init__(self, id: int) -> None:
        self.id = id
        self.beacons = []

    def add_beacon(self, beacon) -> None:
        self.beacons.append(np.array(beacon, dtype=int))

    def transform(self, matrix) -> None:
        return [ matrix.dot(pt) for pt in self.beacons ]

    def __repr__(self) -> str:
        return f"Scanner #{self.id}: {self.position}" # + \
            # "\n".join(repr(b) for b in self.beacons)

    def as_tuples(self):
        return tuple(tuple(pt+self.position) for pt in self.beacons)

def overlaps(beacons, refs):
    best = Counter(tuple(a-b) for (a,b) in product(refs, beacons)).most_common(1)[0]
    if best[1]>=12:
        return best[0]
    else:
        return None


scanners = []
for l in lines:
    if l.startswith("--- scanner"):
        scanner = Scanner(int(l[12:].split(' ', 1)[0]))
        scanners.append(scanner)
    elif l:
        scanner.add_beacon(tuple(map(int, l.split(','))))

known_beacons = set(scanners[0].as_tuples())
unknowns = scanners[1:]
while unknowns:
    s = unknowns.pop(0)
    for m in transformations_matrix:
        beacons = s.transform(m)
        pos = overlaps(beacons, known_beacons)
        if pos is not None:
            s.position = np.array(pos, dtype=int)
            s.beacons = beacons
            # print(s)
            known_beacons.update(s.as_tuples())
            break
    else:
        unknowns.append(s)

print("Part 1:", len(known_beacons))

print("Part 2:", max(sum(abs(c) for c in (s1.position-s2.position)) for (s1, s2) in product(scanners, repeat=2)))