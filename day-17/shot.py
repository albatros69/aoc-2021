#! /usr/bin/env python

import sys
from typing import Tuple
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

target_x, target_y = (tuple(map(int, s[2:].split('..'))) for s in lines[0][13:].split(', '))

def in_target(p: complex, t_x: Tuple[int], t_y:Tuple[int]) -> bool:
    return t_x[0] <= p.real <= t_x[1] and t_y[0] <= p.imag <= t_y[1]

def missed(p: complex, t_x: Tuple[int], t_y:Tuple[int]) -> bool:
    return p.real > t_x[1] or p.imag < t_y[0]

def speed(speed_ini, n):
    return (max(speed_ini[0]-n, 0), speed_ini[1]-n)

def tentative(speed_ini):
    probe = complex(0,0)
    step=0
    max_y=target_y[0]
    while not missed(probe, target_x, target_y):
        probe += complex(*speed(speed_ini, step))
        max_y = max(max_y, probe.imag)
        if in_target(probe, target_x, target_y):
            return True, max_y, speed_ini
        else:
            step += 1
    else:
        return False, max_y, speed_ini

result = list(r for r in map(tentative, product(range(target_x[1]+1), range(target_y[0],target_x[1]+1))) if r[0])
print("Part 1:", int(max(result)[1]))
print("Part 2:", len(result))
