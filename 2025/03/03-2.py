import sys
import pyparsing as pp

pattern = pp.Char(pp.nums)[1,]
summed = 0

def recurse(nums_so_far, candidates):
    desired = 12
    if (12 - len(nums_so_far)) > len(candidates): 
        return None
    if len(nums_so_far)==12:
        # print(nums_so_far)
        total = int("".join([str(i) for i in nums_so_far]))
        # print("concatenated", total, "maxed out", str(nums_so_far))
        return total

    results = []
    temp_sorted = enumerate(candidates)
    temp_sorted = sorted(temp_sorted, key=lambda item: item[1], reverse=True)

    for index, num in temp_sorted:
        
        result = recurse(nums_so_far + [num], candidates[index+1:])
        if result is not None:
            return result

    return None

with open(sys.argv[1], "r") as fh:
    for line in fh.readlines():
        nums = [int(i) for i in pattern.parse_string(line)]
        biggest = 0
        biggest = recurse([], nums)
        print("biggest found in", line.strip(), "is", biggest)
        summed += biggest

print("Total sum:", summed)