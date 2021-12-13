#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

dot = '█'
paper = set()
instructions = []
for l in lines:
    if l.startswith('fold along'):
        instructions.append(l[11:])
    elif l:
        x,y = map(int, l.split(','))
        paper.add((x,y))

def str_paper(p):
    width, height = max(x[0] for x in p)+1, max(x[1] for x in p)+1
    return "\n".join(
        "".join(dot if (x,y) in p else ' ' for x in range(width)) for y in range(height))

# print(str_paper(paper), "\n", instructions)

def fold_paper(p, instr):
    new_p = set()
    axe, v = instr.split('=')
    v = int(v)
    for x,y in p:
        c = (2*v-x if (axe=='x' and x>v) else x, 2*v-y if (axe=='y' and y>v) else y)
        new_p.add(c)

    return new_p

print("Part 1:", len(fold_paper(paper, instructions[0])))

p = paper
for i in instructions:
    p = fold_paper(p, i)
print("Part 2:", str_paper(p), sep="\n")
