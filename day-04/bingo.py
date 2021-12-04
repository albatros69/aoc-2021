#! /usr/bin/env python

import sys
from itertools import product
from copy import deepcopy

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

numbers = [int(i) for i in lines[0].split(',')]

class Board():
    numbers = None

    def __init__(self) -> None:
        self.numbers = { coord: -1 for coord in product(range(5), repeat=2) }

    def init_line(self, line, j) -> None:
        for i,n in enumerate(line.split()):
            self.numbers[i,j] = int(n)

    def __str__(self) -> str:
        return "\n".join(
            " ".join(f"{self.numbers[i,j]:2}" for i in range(5))
            for j in range(5)
        )

    def mark(self, k) -> None:
        for coord in product(range(5), repeat=2):
            if self.numbers[coord]==k:
                self.numbers[coord]=-1
                break
        else:
            return False

        return True

    def is_winning(self):
        columns = (sum(self.numbers[i,j] for i in range(5))==-5 for j in range(5))
        rows = (sum(self.numbers[i,j] for j in range(5))==-5 for i in range(5))
        if any(columns) or any(rows):
            return True
        else:
            return False

    def sum_unmarked(self):
        return sum(self.numbers[c] for c in product(range(5), repeat=2) if self.numbers[c]>=0)

j=0
boards=[]
for l in lines[2:]:
    if j==0:
        board = Board()

    if l=='':
        j=0
        boards.append(board)
        # print(board); print()
    else:
        board.init_line(l,j)
        j+=1
else:
    boards.append(board)

boards_ori = deepcopy(boards)

try:
    for k in numbers:
        for b in boards:
            b.mark(k)
            if b.is_winning():
                print("Part 1:", k*b.sum_unmarked())
                raise StopIteration
except:
    pass


boards = deepcopy(boards_ori)
for k in numbers:
    for b in boards:
        b.mark(k)

    if len(boards)==1 and boards[0].is_winning():
        print("Part 2:", k*boards[0].sum_unmarked())
        break
    else:
        boards = [ b for b in boards if not b.is_winning() ]

