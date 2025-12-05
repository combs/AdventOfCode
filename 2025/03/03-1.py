import sys
import pyparsing as pp

pattern = pp.Char(pp.nums)[1,]
summed = 0

with open(sys.argv[1], "r") as fh:
    for line in fh.readlines():
        nums = list(pattern.parse_string(line))
        vals_first = sorted(set(nums), reverse=True)
        biggest = 0

        for first in vals_first:
            location_first = nums.index(first)
            try:
                second = sorted(set(nums[location_first+1:]), reverse=True)[0]
                biggest = max(biggest, int(first + second))
            except IndexError:
                continue

        print("biggest found in", line.strip(), "is", biggest)
        summed += biggest

print("Total sum:", summed)