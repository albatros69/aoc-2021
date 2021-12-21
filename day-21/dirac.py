#! /usr/bin/env python

from __future__ import annotations
import sys
from itertools import cycle, zip_longest, product
from functools import lru_cache

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Player:
    position: int = None
    score: int = None

    def __init__(self, line: str) -> None:
        self.position = int(line[-1])
        self.score = 0

    def __repr__(self) -> str:
        return f"Player @ {self.position}: {self.score}"

    def move(self, draw):
        self.position = (self.position+sum(draw)-1)%10 + 1
        self.score += self.position


players = [ Player(l) for l in lines ]

dice = grouper(cycle(range(1,101)), 3)
turns = 0
try:
    while True:
        for p in players:
            turns += 3
            draw = next(dice)
            p.move(draw)
            if p.score >=1000:
                raise StopIteration
except StopIteration:
    print(turns, players)
    print("Part 1:", sum(p.score if p.score<1000 else 0 for p in players)*turns)


dice_draws = tuple(sum(d) for d in product((1,2,3), repeat=3))
# Return nb of victories of player1, plus total universes
@lru_cache(maxsize=None)
def play(player1, player2):
    p1p, p1s = player1
    p2p, p2s = player2

    if p1s >= 21:
        return 1,1
    elif p2s >= 21:
        return 0,1
    else:
        p1wins, total = 0, 0
        for draw in dice_draws:
            new_p1p = (p1p+draw-1)%10 + 1
            new_p1s = p1s+new_p1p
            p2wins, subtotal = play(player2, (new_p1p, new_p1s))
            total += subtotal
            p1wins += (subtotal - p2wins)

        return p1wins, total

p1wins, total = play(*((int(l[-1]),0) for l in lines))
print("Part 2:", max(p1wins, total-p1wins))