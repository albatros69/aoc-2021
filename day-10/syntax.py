#! /usr/bin/env python

import sys
from functools import reduce

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

chunks = { '(': ')', '[': ']', '{': '}', '<': '>' }

def read_chunks(line: str) -> str:
    accu = []
    for c in line:
        if c in chunks:
            accu.append(c)
        elif c in chunks.values() and chunks[accu[-1]]==c:
            accu.pop()
        else:
            return (False, c)

    return (True, "".join(chunks[c] for c in accu[::-1]))

scores_syntax = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
def score_syntax(test: bool, c: str) -> int:
    if not test and c in scores_syntax:
        return scores_syntax[c]
    else:
        return 0

# for l in lines:
#     print(l, "→", read_chunks(l))
print("Part 1:", sum(score_syntax(*read_chunks(l)) for l in lines))

scores_autocomplete = { ')': 1, ']': 2, '}': 3, '>': 4 }
def score_autocomplete(test: bool, s: str) -> int:
    if test:
        return reduce(lambda x,c: 5*x+scores_autocomplete[c], s, 0)
    else:
        return 0

# for l in lines:
#     print(l, "→", score_autocomplete(*read_chunks(l)))
scores = []
for l in lines:
    s = score_autocomplete(*read_chunks(l))
    if s > 0:
        scores.append(s)
scores.sort()
print("Part 2:", scores[len(scores)//2])


