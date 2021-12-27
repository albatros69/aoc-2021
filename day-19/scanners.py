#! /usr/bin/env python

from __future__ import annotations
import sys
import time
import numpy as np
from itertools import permutations, product
from heapq import heappush, nsmallest
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


def norme(pt) -> int:
    return sum(abs(c) for c in pt)


class Scanner:
    id = None
    position = np.zeros(3, dtype=int)
    beacons = None
    configurations = None

    def __init__(self, id: int) -> None:
        self.id = id
        self.beacons = []
        self.configurations = {}

    def add_beacon(self, beacon) -> None:
        self.beacons.append(np.array(beacon, dtype=int))

    def transform(self, matrix) -> None:
        return [ matrix.dot(pt) for pt in self.beacons ]

    def __repr__(self) -> str:
        return f"Scanner #{self.id}: {self.position}" # + \
            # "\n".join(repr(b) for b in self.beacons)

    def as_tuples(self):
        return tuple(tuple(pt+self.position) for pt in self.beacons)

    def compute_config(self):
        distances = { tuple(pt): [] for pt in self.beacons }

        for i,pt in enumerate(self.beacons):
            for other in self.beacons[i+1:]:
                d = norme(pt-other)
                heappush(distances[tuple(pt)], (d, tuple(other)))
                heappush(distances[tuple(other)], (d, tuple(pt)))

        for pt in distances:
            (d1, o1), (d2, o2) = nsmallest(2, distances[pt])
            self.configurations[pt] = d1*d2*norme(np.array(o1)-np.array(o2))

    def is_overlap(self, other: Scanner):
        tmp = set(self.configurations.values()) & set(other.configurations.values())
        if len(tmp) == 0:
            return None
        else:
            return (sorted(pt for pt in self.configurations if self.configurations[pt] in tmp),
                    tuple(pt for pt in other.configurations if other.configurations[pt] in tmp))


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
start = time.time()
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
print("Execution time: %.3fs" % (time.time()-start, ))

print("Part 1:", len(known_beacons))
print("Part 2:", max(norme(s1.position - s2.position) for (s1, s2) in product(scanners, repeat=2)))
print("-"*8)

scanners = []
for l in lines:
    if l.startswith("--- scanner"):
        scanner = Scanner(int(l[12:].split(' ', 1)[0]))
        scanners.append(scanner)
    elif l:
        scanner.add_beacon(tuple(map(int, l.split(','))))

scanners[0].compute_config()
known_scanners = [scanners[0]]
known_beacons = set(scanners[0].as_tuples())
unknowns = scanners[1:]
start = time.time()
while unknowns:
    s = unknowns.pop(0)
    s.compute_config()
    try:
        for k in known_scanners:
            overlap = k.is_overlap(s)
            if overlap is not None:
                ref, to_move = overlap
                if len(ref) < 12:
                    continue

                for m in transformations_matrix:
                    tmp = sorted(tuple(m.dot(pt)) for pt in to_move)
                    pos = np.array(ref[0])-np.array(tmp[0])
                    if all(tuple(a)==tuple(pos+b) for (a,b) in zip(ref, tmp)):
                        s.beacons = s.transform(m)
                        s.position = pos+k.position
                        s.configurations = { tuple(m.dot(k)): v for (k,v) in s.configurations.items() }
                        # print(s)
                        known_beacons.update(s.as_tuples())
                        known_scanners.append(s)
                        raise StopIteration

    except StopIteration:
        continue
    else:
        unknowns.append(s)

print("Execution time: %.3fs" % (time.time()-start, ))
print("Part 1 (bis):", len(known_beacons))
print("Part 2 (bis):", max(norme(s1.position - s2.position) for (s1, s2) in product(scanners, repeat=2)))
