import sys
import numpy

with open(sys.argv[1], "r") as fh:
    height = 0
    width = 0
    for row, line in enumerate(fh):
        ll = len(line.strip())
        if ll > 1:
            width = ll
        height += 1

map_starting = numpy.zeros((width, height), dtype=int)

with open(sys.argv[1], "r") as fh:
    for row, line in enumerate(fh):
        for col, char in enumerate(line):
            if char=="@":
                map_starting[row][col] = 1

def crownch(map_starting):

    map_working = numpy.pad(map_starting, 4, constant_values=(0))
    # print(map_starting)
    map_padded = map_working.copy()

    ortho = ( (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1) )

    for transform in ortho:
        temp = numpy.roll(map_padded, transform, axis=(0, 1))
        map_working += temp
    
    # print(map_working)
    map_working = map_working[4:-4,4:-4]
    map_working = map_working <= 4
    map_working = numpy.where(map_starting, map_working,  0)
    # print(map_working)
    map_starting -= map_working
    
    return map_starting, numpy.sum(map_working)

map_now = map_starting.copy()

amount = None
summed = 0

while amount != 0:
    map_now, amount = crownch(map_now)
    print(amount)
    summed += amount

print(map_starting)
print(map_now)
print(summed)
