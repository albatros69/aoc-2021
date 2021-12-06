#! /usr/bin/env python

import sys
from collections import Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def most_frequent(numbers_list: list, idx) -> str:
    counter = Counter()

    for l in numbers_list:
        counter.update(l[idx])

    return "0" if counter["0"]>counter["1"] else "1"

def complement(number: str) -> str:
    return "".join("0" if c=="1" else "1" for c in number)

gamma = "".join(most_frequent(lines, k) for k in range(0, len(lines[0])))
epsilon = complement(gamma)
print("Part 1:", gamma, epsilon, "→", int(gamma, base=2)*int(epsilon, base=2))

tmp_ox = lines
tmp_co = lines
ox = ""
co = ""
for k in range(0, len(lines[0])):
    if len(tmp_ox)==1:
        ox = tmp_ox[0]
    else:
        value_ox = most_frequent(tmp_ox, k)
        ox += value_ox
        tmp_ox = [ l for l in tmp_ox if l[k] == value_ox ]

    if len(tmp_co)==1:
        co = tmp_co[0]
    else:
        value_co = complement(most_frequent(tmp_co, k))
        co += value_co
        tmp_co = [ l for l in tmp_co if l[k] == value_co ]

print("Part 2:", ox, co, "→", int(ox, base=2)*int(co, base=2))
