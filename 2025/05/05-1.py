import sys
import pyparsing as pp

pattern_ranges = pp.pyparsing_common.integer() + ... + pp.pyparsing_common.integer()
pattern_vals = pp.pyparsing_common.integer()

summed = 0
patterns = []
values = []


with open(sys.argv[1], "r") as fh:

    while True:
        line = fh.readline()
        try:
            patterns.append((pattern_ranges.parse_string(line)[0], pattern_ranges.parse_string(line)[2]) )
        except pp.ParseException as e:
            break
    print(patterns)

    while True:
        line = fh.readline()
        try:
            values.append(pattern_vals.parse_string(line)[0])
        except pp.ParseException as e:
            break

def fresh(val):
    for pat in patterns:
        if val >= pat[0] and val <= pat[1]:
            print("fresh due to", pat)
            return True
    return False

for val in values:
    if fresh(val):
        summed += 1
        print("val is fresh")
        
print("Total sum:", summed)