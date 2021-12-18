#! /usr/bin/env python

from __future__ import annotations
import sys
from typing import Union
from itertools import product


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Number():
    parent: Number = None
    right: Union[Number,int] = None
    left: Union[Number,int] = None

    def __init__(self, number, parent: Number=None):
        left, right = number
        self.parent = parent

        if isinstance(left, int):
            self.left = left
        elif isinstance(left, Number):
            self.left = left
            self.left.parent = self
        else:
            self.left = Number(left, parent=self)
        if isinstance(right, int):
            self.right = right
        elif isinstance(right, Number):
            self.right = right
            self.right.parent = self
        else:
            self.right = Number(right, parent=self)

    def __repr__(self):
        return f"[{self.left},{self.right}]"

    def __add__(self, other: Number) -> Number:
        return Number((self, other))

    def add(self, n: int, left: bool) -> None:
        if left:
            if isinstance(self.left, int):
                self.left += n
            elif isinstance(self.right, int):
                self.right += n
            else:
                raise ValueError
        else:
            if isinstance(self.right, int):
                self.right += n
            elif isinstance(self.left, int):
                self.left += n
            else:
                raise ValueError


    def is_regular(self) -> bool:
        return isinstance(self.left, int) and isinstance(self.right, int)

    @property
    def nesting_level(self) -> int:
        if self.is_regular():
            return 0
        elif isinstance(self.left, int):
            return 1 + self.right.nesting_level
        elif isinstance(self.right, int):
            return 1 + self.left.nesting_level
        else:
            return 1+max(self.left.nesting_level, self.right.nesting_level)

    @property
    def level(self) -> int:
        if self.parent==None:
            return 0
        else:
            return 1+self.parent.level

    @property
    def magnitude(self) -> int:
        if isinstance(self.left, int):
            left_magn = self.left
        else:
            left_magn = self.left.magnitude
        if isinstance(self.right, int):
            right_magn = self.right
        else:
            right_magn = self.right.magnitude
        return 3*left_magn + 2*right_magn


    def split(self):
        result = False
        if isinstance(self.left, int) and self.left>9:
            self.left = Number((self.left//2, self.left//2+self.left%2), parent=self)
            result |= True
        if not result and isinstance(self.left, Number):
            result |= self.left.split()
        if not result and isinstance(self.right, int) and self.right>9:
            self.right = Number((self.right//2, self.right//2+self.right%2), parent=self)
            result |= True
        if not result and isinstance(self.right, Number):
            result |= self.right.split()
        return result


    def flatten(self) -> list[Number]:
        if self.is_regular():
            return [self]
        elif isinstance(self.left, int):
            return [self] + self.right.flatten()
        elif isinstance(self.right, int):
            return self.left.flatten() + [self]
        else:
            return self.left.flatten() + self.right.flatten()


    def explode(self):
        if self.nesting_level >= 4:
            leafs = self.flatten()
            left_nested = next(l for l in leafs if l.level>=4 and l.is_regular())
            i = leafs.index(left_nested)
            if i>0:
                leafs[i-1].add(left_nested.left, left=False)
            if i<len(leafs)-1:
                leafs[i+1].add(left_nested.right, left=True)
            p = left_nested.parent
            if p.right == left_nested:
                p.right = 0
            else:
                p.left = 0
            return True
        else:
            return False


    def reduce(self):
        while self.explode() or self.split():
            pass


result=None
for l in lines:
    if result:
        result += Number(eval(l))
        # print(result)
        result.reduce()
    else:
        result = Number(eval(l))
    # print(result)

print("Part 1:", result.magnitude)

results = list(Number(eval(x))+Number(eval(y)) for (x,y) in product(lines, repeat=2) if x!=y)
for r in results:
    r.reduce()
print("Part 2:", max(r.magnitude for r in results))