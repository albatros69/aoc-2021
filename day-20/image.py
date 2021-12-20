#! /usr/bin/env python

import sys
from itertools import product
from functools import reduce

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

algorithm = [1 if c=='#' else 0 for c in lines[0]]

class Image:
    pixels: dict = None
    default: int = 0

    def __init__(self, lines) -> None:
        self.pixels = {}
        self.default = 0

        for y,l in enumerate(lines):
            for x,c in enumerate(l):
                self.pixels[x,y]=1 if c=='#' else 0

    def __str__(self) -> str:
        min_x, max_x, min_y, max_y = self.bbox()

        return "\n".join(
            "".join("#" if self.get((x,y)) else "." for x in range(min_x, max_x+1))
            for y in range(min_y, max_y+1)
            )


    def bbox(self) -> tuple:
        min_x, max_x = 0,0
        min_y, max_y = 0,0
        for x,y in self.pixels:
            min_x = min(min_x, x) ; max_x= max(max_x, x)
            min_y = min(min_y, y) ; max_y= max(max_y, y)
        return min_x-1, max_x+1, min_y-1, max_y+1


    def get(self, px):
        try:
            return self.pixels[px]
        except KeyError:
            self.pixels[px] = self.default
            return self.default


    def step(self):
        result = {}
        min_x, max_x, min_y, max_y = self.bbox()

        for x,y in product(range(min_x, max_x+1), range(min_y,max_y+1)):
            group = reduce(lambda x,y: 2*x+y,
                (self.get(px) for px in ((x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1))),
                0)
            result[x,y] = algorithm[group]

        self.default = algorithm[int(str(self.default)*9, 2)]
        self.pixels = result


    @property
    def nb_lit(self) -> int:
        min_x, max_x, min_y, max_y = self.bbox()
        return sum(self.get(px) for px in product(range(min_x, max_x+1), range(min_y,max_y+1)))


image = Image(lines[2:])
# print(image)

for _ in range(2):
    image.step()
    # print(image)
print("Part 1:", image.nb_lit)

for _ in range(2, 50):
    image.step()
print("Part 2:", image.nb_lit)
