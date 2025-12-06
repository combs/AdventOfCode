import sys
import pyparsing as pp
import numpy

pattern_ranges = pp.pyparsing_common.integer() + ... + pp.pyparsing_common.integer()
pattern_vals = pp.OneOrMore(pp.pyparsing_common.integer())
pattern_operations = pp.OneOrMore(pp.Char(list("+-*/")))

summed = 0
values = []
operations = []

with open(sys.argv[1], "r") as fh:
    line = None
    while True:
        line = fh.readline()
        try:
            values.append(list(pattern_vals.parse_string(line)))
        except pp.ParseException as e:
            break
    for thingie in pattern_operations.parse_string(line):
        operations.append(thingie)

values = numpy.array(values).transpose()
print(operations)
for index, op in enumerate(operations):
    result = 0
    if op=="+":
        result = numpy.sum(values[index])
    elif op=="-":
        result = values[index][0]
        for i in range(1, values.shape[1]):
            result -= values[index][i]
    elif op=="/":
        result = values[index][0]
        for i in range(1, values.shape[1]):
            result /= values[index][i]
    elif op=="*":
        result = values[index][0]
        for i in range(1, values.shape[1]):
            result *= values[index][i]
    print(values[index], op, result)
    summed += result

print("Total sum:", summed)