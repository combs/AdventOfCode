import sys
import numpy

temp = []
SPLITTER = -1
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

for row in range(matrix.shape[0]):
    if row==0:
        continue
    for col, val in enumerate(matrix[row]): # Do a separate path to propagate beams
        if matrix[row-1][col] >= BEAM and val == 0:
            matrix[row][col] = matrix[row-1][col]

    for col, val in enumerate(matrix[row]):
        if val==SPLITTER and matrix[row-1][col] >= BEAM: # A beam is above it
            split = False
            if col > 0:
                matrix[row][col-1] += matrix[row-1][col]
            if col < (matrix.shape[1] - 1):
                matrix[row][col+1] += matrix[row-1][col]

print(sum(list(matrix[-1,])))