#! /usr/bin/env python

import sys
from heapq import heappop, heappush
from copy import deepcopy

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


energies = dict(zip('ABCD', (10**k for k in range(4))))
exits = dict(zip('ABCD', (2,4,6,8)))


def is_organized(room: list, k) -> bool:
    car = 'ABCD'[k] if isinstance(k, int) else k
    return all(a == car for a in room)


def sign(a: int) -> int:
    if a>0:
        return 1
    elif a<0:
        return -1
    else:
        return 0


def print_status(current, dir, rooms, hallway):
    if dir==1:
        car = '→'
    elif dir==-1:
        car = '←'
    else:
        car = '↓'
    print(" ", "".join(car if current==k else ' ' for k in range(11)), " ", sep='')

    print("#############")
    print("#", ''.join(hallway), '#', sep='')
    for k in range(DEPTH-1,-1,-1):
        print('###', '#'.join(r[k] if len(r) > k else '.' for r in rooms), '###', sep='')
    print("  #########")


def hash_status(rooms, hallway):
    return "".join(('{:.<%d}' % (DEPTH,)).format("".join(r)) for r in rooms) + "".join(hallway)


def search_solution(rooms_ini):
    # print_status(-1, 0, rooms_ini, ['.',]*11)
    queue = [(0, rooms_ini, -1, 0, [ '.', ] *11)]
    already_seen = { hash_status(rooms_ini, [ '.', ] *11): 0 }

    while queue:
        nrj, rooms, current, dir, hallway = heappop(queue)

        if all(is_organized(rooms[k], k) and len(rooms[k])==DEPTH for k in range(4)):
            # print(len(queue))
            # print_status(nrj, dir, rooms, hallway)
            return nrj
        else:
            if current >= 0:
                new_rooms = deepcopy(rooms)
                new_hallway = hallway[:]
                curr_a = hallway[current]
                k_room = ord(curr_a)-ord('A')
                new_pos = current+dir

                if current == exits[curr_a] and is_organized(rooms[k_room], curr_a):
                    new_hallway[current] = '.'
                    new_rooms[k_room].append(curr_a)
                    new_nrj = nrj+(DEPTH-len(rooms[k_room]))*energies[curr_a]
                    if hash_status(new_rooms, new_hallway) not in already_seen \
                      or already_seen[hash_status(new_rooms, new_hallway)] > new_nrj:
                        already_seen[hash_status(new_rooms, new_hallway)] = new_nrj
                        heappush(queue, (new_nrj, new_rooms, -1, 0, new_hallway))
                else:
                    if 0 <= new_pos < 11 and hallway[new_pos]=='.':
                        new_hallway[current] = '.'
                        new_hallway[new_pos] = curr_a
                        new_nrj = nrj+energies[curr_a]
                        if hash_status(new_rooms, new_hallway) not in already_seen \
                          or already_seen[hash_status(new_rooms, new_hallway)] > new_nrj:
                            already_seen[hash_status(new_rooms, new_hallway)] = new_nrj
                            heappush(queue, (new_nrj, new_rooms, new_pos, dir, new_hallway))
                            # current decides to stop
                            if new_pos not in exits.values():
                                heappush(queue, (new_nrj, deepcopy(new_rooms), -1, 0, new_hallway[:]))
            else:
                for k in range(4):
                    color = 'ABCD'[k]
                    new_rooms = deepcopy(rooms)
                    new_hallway = hallway[:]
                    if is_organized(new_rooms[k], color) or len(new_rooms[k])==0:
                        # room already full with the correct type or empty
                        continue
                    else:
                        curr_a = new_rooms[k].pop()
                        new_hallway[exits[color]] = curr_a
                        new_nrj = nrj+(DEPTH+1-len(rooms[k]))*energies[curr_a]
                        if hash_status(new_rooms, new_hallway) not in already_seen \
                          or already_seen[hash_status(new_rooms, new_hallway)] > new_nrj:
                            already_seen[hash_status(new_rooms, new_hallway)] = new_nrj
                            heappush(queue, (new_nrj, new_rooms, exits[color], 1, new_hallway))
                            heappush(queue, (new_nrj, deepcopy(new_rooms), exits[color], -1, new_hallway[:]))

                for i,a in enumerate(hallway):
                    if a in 'ABCD' and is_organized(rooms[ord(a)-ord('A')], a):
                        new_dir = sign(exits[a]-i)
                        new_pos = i+new_dir
                        if 0 <= new_pos < 11 and hallway[new_pos]=='.':
                            new_rooms = deepcopy(rooms)
                            new_hallway = hallway[:]
                            new_hallway[i] = '.'
                            new_hallway[new_pos] = a
                            new_nrj = nrj+energies[a]
                            if hash_status(new_rooms, new_hallway) not in already_seen \
                              or already_seen[hash_status(new_rooms, new_hallway)] > new_nrj:
                                already_seen[hash_status(new_rooms, new_hallway)] = new_nrj
                                heappush(queue, (new_nrj, new_rooms, new_pos, new_dir, new_hallway))

        # print(len(queue), " "*10, end="\r")

    return None


DEPTH = 2
rooms = [ [], [], [], [] ]

for l in lines[-2:-4:-1]:
    for k in range(4):
        rooms[k].append(l[3+2*k])

print("Part 1:", search_solution(rooms))

DEPTH=4
rooms = [ [], [], [], [] ]

for l in lines[-2:-3:-1]+ ['  #D#B#A#C#', '  #D#C#B#A#' ] + lines[-3:-4:-1]:
    for k in range(4):
        rooms[k].append(l[3+2*k])

print("Part 2:", search_solution(rooms))
