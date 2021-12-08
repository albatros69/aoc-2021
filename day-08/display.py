#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

segments = {
    'abcefg': 0 ,
    'cf': 1 ,
    'acdeg': 2 ,
    'acdfg': 3 ,
    'bcdf': 4 ,
    'abdfg': 5 ,
    'abdefg': 6 ,
    'acf': 7 ,
    'abcdefg': 8 ,
    'abcdfg': 9,
}

count=0
for l in lines:
    signals, displays = l.split(' | ')
    signals = signals.split()
    displays = displays.split()
    count += sum(len(d) in (2,3,4,7) for d in displays)
print('Part 1:', count)

def sorted_signal(s):
    return "".join(sorted(s))

result_part2 = 0
for l in lines:
    signals, displays = l.split(' | ')
    signals = signals.split()
    displays = displays.split()

    trans_table = {}
    while len(trans_table)<10:
        for s in signals:
            sorted_s = sorted_signal(s)
            if len(s)==2: # 1
                trans_table[1] = sorted_s
            elif len(s)==3: # 7
                trans_table[7] = sorted_s
            elif len(s)==4: # 4
                trans_table[4] = sorted_s
            elif len(s)==7: # 8
                trans_table[8] = sorted_s
            elif len(s)==5: # 2,3,5
                if 1 in trans_table and all(c in s for c in trans_table[1]):
                    # if all the segments of 1 are there, it's 3
                    trans_table[3] = sorted_s
                elif 6 in trans_table and sum(c not in s for c in trans_table[6])==1:
                    # 5 has exactly one difference with 6
                    trans_table[5] = sorted_s
                elif 6 in trans_table and sum(c not in s for c in trans_table[6])==2:
                    # 2 has exactly two differencess with 6
                    trans_table[2] = sorted_s
            elif len(s)==6: # 0,6,9
                if 1 in trans_table and not all(c in s for c in trans_table[1]):
                    # 1 is included in 0 and 9, but 6
                    trans_table[6] = sorted_s
                elif 4 in trans_table and all(c in s for c in trans_table[4]):
                    # 4 is included in 0 and 6, but 9
                    trans_table[9] = sorted_s
                else:
                    if 6 in trans_table and 9 in trans_table:
                        trans_table[0] = sorted_s
            else:
                print("Oups")

    # print(trans_table)
    reversed_trans_table = dict(zip(trans_table.values(), trans_table.keys()))
    # print(displays, '→', "".join(str(reversed_trans_table[sorted_signal(s)]) for s in displays))
    result_part2 += int("".join(str(reversed_trans_table[sorted_signal(s)]) for s in displays))

print("Part 2:", result_part2)

