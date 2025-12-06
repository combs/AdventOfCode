import sys
import numpy

summed = 0
values = []
operations = []
temp = []

with open(sys.argv[1], "r") as fh:
    line = None
    length = 0
    for line in fh.readlines():
        line = line.replace("\n", "").ljust(length)
        length = max(length, len(line))
        if len(line) > 3:
            temp.append(list(line))

matrix = numpy.array(temp, dtype=str)

these_values = []
class NextIteration(Exception):
    pass

for col in reversed(range(matrix.shape[1])):
    letters = matrix[:, col]

    try:
        for op in list("+-*/"):
            if op in letters:
                operations.append(op)
                strang = "".join(letters).strip().replace(op, "")
                these_values.append(int(strang))
                values.append(these_values.copy())
                these_values = []
                raise NextIteration
        
        strang = "".join(letters).strip()
        if len(strang):
            these_values.append(int(strang))
    except NextIteration:
        pass

    

for index, op in enumerate(operations):
    result = 0
    if op=="+":
        result = sum(values[index])
    elif op=="-":
        result = values[index][0]
        for i in range(1, len(values[index])):
            result -= values[index][i]
    elif op=="/":
        result = values[index][0]
        for i in range(1, len(values[index])):
            result /= values[index][i]
    elif op=="*":
        result = values[index][0]
        for i in range(1, len(values[index])):
            result *= values[index][i]
    print(values[index], op, result)
    summed += result

print("Total sum:", summed)