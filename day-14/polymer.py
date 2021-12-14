#! /usr/bin/env python

import sys
from collections import defaultdict, Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

poly_template = lines[0]
rules = defaultdict(dict)
for l in lines[2:]:
    pattern, insertion = l.split(' -> ')
    rules[pattern[0]][pattern[1]] = insertion

def step_1(poly: str) -> str:
    i = 0
    result = ''
    while i < len(poly)-1:
        a,b = poly[i], poly[i+1]
        if a in rules and b in rules[a]:
            insertion = rules[a][b]
        else:
            insertion = ''
        result += a + insertion
        i += 1

    return result+poly[-1]

# print("Template:    ", poly_template)
# p = poly_template
# for i in range(1, 5):
#     p = step(p)
#     print(f"After step {i}:", p)
p = poly_template
for _ in range(10):
    p = step_1(p)
counter = Counter(p).most_common()
print("Part 1:", counter[0][1]-counter[-1][1])

def step_2(poly: Counter) -> Counter:
    result = Counter()

    for s,v in poly.items():
        if len(s) < 2:
            insertion = { s: v }
        else:
            a, b = s
            if a in rules and b in rules[a]:
                insertion = { a+rules[a][b]: v, rules[a][b]+b: v, rules[a][b]: v, }
            else:
                insertion = { s: v }

        result.update(insertion)

    return result

p = Counter(poly_template[i:i+2] for i in range(len(poly_template)-1))
p.update(poly_template)
for _ in range(10):
    p = step_2(p)
result = Counter({s: p[s] for s in p if len(s)==1}).most_common()
print("Part 1 (bis):", result[0][1]-result[-1][1])

for _ in range(30):
    p = step_2(p)
result = Counter({s: p[s] for s in p if len(s)==1}).most_common()
print("Part 2:", result[0][1]-result[-1][1])
