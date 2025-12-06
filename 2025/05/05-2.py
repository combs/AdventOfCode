import sys
import pyparsing as pp

pattern_ranges = pp.pyparsing_common.integer() + ... + pp.pyparsing_common.integer()
pattern_vals = pp.pyparsing_common.integer()

summed = 0
patterns = []
values = []

class Breaker(Exception):
    pass

with open(sys.argv[1], "r") as fh:

    while True:
        line = fh.readline()
        try:
            patterns.append([pattern_ranges.parse_string(line)[0], pattern_ranges.parse_string(line)[2]] )
        except pp.ParseException as e:
            break
    print(patterns)

    while True:
        line = fh.readline()
        try:
            values.append(pattern_vals.parse_string(line)[0])
        except pp.ParseException as e:
            break

patterns_new = patterns.copy()
# patterns = sorted(patterns, key=lambda pat: pat[0])
restart = True
while restart==True:
    try:
        for index_one, (pat_one_fr, pat_one_to) in enumerate(patterns):
            for index_two, (pat_two_fr, pat_two_to) in enumerate(patterns):
                if index_one==index_two:
                    continue
                if pat_one_to >= pat_two_fr and pat_one_to <= pat_two_to:
                    # Pattern two extends pattern one
                    # print("Pattern", index_one, patterns[index_one], "extended by", index_two, patterns[index_two])
                    patterns[index_one][1] = pat_two_to
                    patterns[index_one][0] = min(pat_one_fr, pat_two_fr) 
                    print("Updated", index_one, "from", (pat_one_fr, pat_one_to), "to", patterns[index_one], "and deleting", index_two, patterns[index_two])
                    del(patterns[index_two])
                    # print(patterns)

                    raise Breaker
        restart = False
    except Breaker:
        restart = True

for pat in patterns:
    summed += (pat[1] - pat[0] + 1)
    # Inclusive not exclusive. 3-5 means 3 numbers not 2

print("Total sum:", summed)