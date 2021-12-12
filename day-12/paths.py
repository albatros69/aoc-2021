#! /usr/bin/env python

from collections import defaultdict, Counter
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

caves = defaultdict(list)
for l in lines:
   beg, end = l.split('-')
   caves[beg].append(end)
   caves[end].append(beg)

paths = []
queue = [ ['start', ] ]
while queue:
    current_path = queue.pop()
    current_pos = current_path[-1]
    small_caves_seen = tuple(c for c in current_path if c.islower())

    if current_pos == 'end':
        paths.append(current_path)
    else:
        queue.extend(current_path+[c] for c in caves[current_pos] if c not in small_caves_seen)

# paths.sort()
# print("\n".join(",".join(p) for p in paths))
print("Part 1:", len(paths))

def is_next_valid(cave: str, small_caves_seen: Counter):
    if cave=='start':
        return False
    elif cave.isupper() or cave=='end':
        return True
    elif cave not in small_caves_seen:
        return True
    else:
        return max(small_caves_seen.values()) < 2

paths = []
queue = [ ['start', ] ]
while queue:
    current_path = queue.pop()
    current_pos = current_path[-1]
    small_caves_seen = Counter(c for c in current_path if c.islower())

    if current_pos == 'end':
        paths.append(current_path)
    else:
        queue.extend(current_path+[c] for c in caves[current_pos] if is_next_valid(c, small_caves_seen))

# paths.sort()
# print("\n".join(",".join(p) for p in paths))
print("Part 2:", len(paths))
