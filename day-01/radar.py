#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(int(line.rstrip('\n')))

count = 0
for i in range(0, len(lines)-1):
    count += int((lines[i+1]-lines[i])>0)
print('Part 1:', count)

sliding_windows = [ sum(lines[i:i+3]) for i in range(0, len(lines)-2) ]
# tmp = lines
# for i in range(0, len(lines)-2):
#     a,b,c,*l = tmp
#     sliding_windows.append(a+b+c)
#     tmp = [b,c]+l
count = 0
for i in range(0, len(sliding_windows)-1):
    count += int((sliding_windows[i+1]-sliding_windows[i])>0)
print('Part 2:', count)