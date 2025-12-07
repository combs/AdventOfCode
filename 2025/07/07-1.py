import sys
import numpy

summed = 0
values = []
operations = []
temp = []
SPLITTER = 10
BEAM = 1

def replacer(thing):
    global SPLITTER, BEAM
    replaces = {".": 0, "S": BEAM, "^": SPLITTER}
    return replaces.get(thing, thing)
    
with open(sys.argv[1], "r") as fh:
    line = None
    length = 0
    for line in fh.readlines():
        line = line.replace("\n", "")
        length = max(length, len(line))
        ll = list(line)

        ll = list(map(replacer, ll))

        if len(ll):
            temp.append(ll)

matrix = numpy.array(temp, dtype=int)

count = 0
for row in range(matrix.shape[0]):
    if row==0:
        continue
    for col, val in enumerate(matrix[row]):
        if matrix[row-1][col] == BEAM and val == 0:
            matrix[row][col] = BEAM

        if val==SPLITTER and matrix[row-1][col] == BEAM: # A beam is above it
            split = False
            if col > 0 and matrix[row][col-1] != BEAM:
                matrix[row][col-1] = BEAM
                split = True
            if col < (matrix.shape[1] - 1) and matrix[row][col+1] != BEAM:
                matrix[row][col+1] = BEAM
                split = True
            if split:
                count += 1

print(matrix)
print(count)
