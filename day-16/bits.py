#! /usr/bin/env python

import sys
from itertools import chain, zip_longest
from functools import reduce
from typing import Tuple

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def hex_to_bin(s: str) -> list:
    return list(chain.from_iterable("{:04b}".format(int(c, 16)) for c in s))

def read_literal(p: list) -> list:
    groups = []
    for g in grouper(p, 5, "0"):
        groups.append(int("".join(g[1:]), 2))
        if g[0]=="0":
            return groups

def literal_to_int(l: list) -> int:
    if l:
        return l[-1]+16*literal_to_int(l[:-1])
    else:
        return 0


class Packet():
    version=None
    type=None
    data=None
    payload=None
    length=0

    def __init__(self, data) -> None:
        self.data = data[:]
        self.decode()

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return "".join(self.data)

    def __repr__(self) -> str:
        return "Packet({}, {}, {})".format(self.version, self.type, self.payload)


    def decode(self) -> None:
        if all(c=="0" for c in self.data):
            self.payload=None
            self.length=len(self.data)
            return

        self.version = int("".join(self.data[0:3]), 2)
        self.type = int("".join(self.data[3:6]), 2)

        if self.type==4:
            self.payload = read_literal(self.data[6:])
            self.length = 6+5*len(self.payload)
        else:
            type_id = self.data[6]
            if type_id=="0":
                length = int("".join(self.data[7:22]), 2)
                self.payload, l = read_sub_packets(self.data[22:22+length])
                self.length = 6+1+15+l
                assert(l==length)
            elif type_id=="1":
                nb_sub_packets = int("".join(self.data[7:18]), 2)
                self.payload, l = read_sub_packets(self.data[18:], nb=nb_sub_packets)
                self.length = 6+1+11+l
                assert(len(self.payload)==nb_sub_packets)


    def sum_version(self) -> int:
        return self.version + sum(x.sum_version() if isinstance(x, Packet) else 0 for x in self.payload)


    def eval(self) -> int:
        if self.type==0:
            return sum(p.eval() for p in self.payload)
        elif self.type==1:
            return reduce(lambda x,y: x*y, (p.eval() for p in self.payload))
        elif self.type==2:
            return min(p.eval() for p in self.payload)
        elif self.type==3:
            return max(p.eval() for p in self.payload)
        elif self.type==4:
            return literal_to_int(self.payload)
        elif self.type==5:
            assert(len(self.payload)==2)
            return int(self.payload[0].eval() > self.payload[1].eval())
        elif self.type==6:
            assert(len(self.payload)==2)
            return int(self.payload[0].eval() < self.payload[1].eval())
        elif self.type==7:
            assert(len(self.payload)==2)
            return int(self.payload[0].eval() == self.payload[1].eval())


def read_sub_packets(data: list, nb=None) -> Tuple[list, int]:
    tmp = data
    result = []
    total_length = 0
    while (nb is None and tmp) or (isinstance(nb, int) and len(result)<nb):
        p = Packet(tmp)
        total_length += len(p)
        if p.payload is not None:
            result.append(p)
        tmp = tmp[len(p):]

    return result, total_length


for l in lines:
    packet = Packet(hex_to_bin(l))
    # print(l, str(packet))
    # print(repr(packet))
    print("Part 1:", packet.sum_version())
    print("Part 2:", packet.eval())


