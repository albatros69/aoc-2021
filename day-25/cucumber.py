#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

floor={}
height, width=len(lines), len(lines[0])
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        floor[x,y]=c


def print_floor(floor):
    print("\n".join(
        "".join(floor[x,y] for x in range(width))
        for y in range(height)
    ))


def move(h, x,y):
    if h == '>':
        return (x+1)%width, y
    elif h == 'v':
        return x, (y+1)%height

def substep(floor: dict, herd: str) -> dict:
    new_floor = floor.copy()
    moves = 0

    for c in floor:
        if floor[c] == herd:
            new_pos=move(herd, *c)
            if floor[new_pos] == '.':
                new_floor[new_pos]=herd
                new_floor[c]='.'
                moves+=1

    return new_floor, moves


def step(floor: dict) -> dict:
    new_floor = floor.copy()
    moves = 0
    for h in ('>', 'v'):
        new_floor, m = substep(new_floor, h)
        moves+=m
    return new_floor, moves


i=0
while True:
    i=i+1
    floor, moves = step(floor)
    if moves == 0:
        # print(f"After {i} steps:")
        # print_floor(floor)
        break

print("Part 1:", i)