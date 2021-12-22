#! /usr/bin/env python

from __future__ import annotations
import sys
from collections import defaultdict
from itertools import product, chain
from functools import reduce


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


reactor = defaultdict(int)
for l in lines:
    action, coords = l.split(' ')
    intervals = []
    cube = []
    for interval in coords.split(','):
        (a,b) = map(int, interval[2:].split('..'))
        if -50<=a<=50 and -50<=b<=50:
            intervals.append(range(a, b+1))
    for c in product(*intervals):
        reactor[c] = 1 if action =='on' else 0

print("Part 1:", sum(reactor[c] for c in product(range(-50, 51), repeat=3)))


class Cube:
    action: int = None
    x: tuple = None
    y: tuple = None
    z: tuple = None

    def __init__(self, **kwargs) -> None:
        self.x = tuple(kwargs['x'])
        self.y = tuple(kwargs['y'])
        self.z = tuple(kwargs['z'])
        self.action = kwargs['action']

    def __repr__(self) -> str:
        return "Cube({}, x={}, y={}, z={})".format('on' if self.action else 'off', self.x, self.y, self.z)

    def volume(self) -> int:
        return reduce(lambda x,y: x*y, ((b-a+1) for (a,b) in (self.x, self.y, self.z)))

    def intersect(self, other: Cube):
        if self.x[0] > other.x[1] or self.x[1] < other.x[0]:
            return None
        elif self.y[0] > other.y[1] or self.y[1] < other.y[0]:
            return None
        elif self.z[0] > other.z[1] or self.z[1] < other.z[0]:
            return None
        else:
            x_sorted = sorted(chain(self.x, other.x))
            y_sorted = sorted(chain(self.y, other.y))
            z_sorted = sorted(chain(self.z, other.z))
            return Cube(x=x_sorted[1:3], y=y_sorted[1:3], z=z_sorted[1:3], action=int(not other.action))

cubes = []
for l in lines:
    cube = {}
    action, coords = l.split(' ')
    cube['action'] = 1 if action=='on' else 0
    for interval in coords.split(','):
        (a,b) = map(int, interval[2:].split('..'))
        cube[interval[0]] = a,b

    new_cube = Cube(**cube)
    new_cubes = []
    for other in cubes:
        c = new_cube.intersect(other)
        if c:
            new_cubes.append(c)
    if new_cube.action:
        cubes.append(new_cube)
    cubes.extend(new_cubes)

count_part1 = count_part2 = 0
for c in cubes:
    if c.action:
        if all(abs(i)<=50 for i in chain(c.x, c.y, c.z)):
            count_part1 += c.volume()
        count_part2 += c.volume()
    else:
        if all(abs(i)<=50 for i in chain(c.x, c.y, c.z)):
            count_part1 -= c.volume()
        count_part2 -= c.volume()

print("Part 1 (bis):", count_part1)
print("Part 2:", count_part2)