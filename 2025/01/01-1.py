import sys
import pyparsing as pp

pos = 50
integer = pp.Word(pp.nums)
pattern = pp.Char(["L", "R"]) + pp.pyparsing_common.integer()
passes = 0

with open(sys.argv[1], "r") as fh:
    for line in fh.readlines():
        (direction, amount) = pattern.parse_string(line)
        if direction=="L":
            amount *= -1
        
        print(pos, direction, amount)
        
        pos += amount
        pos = pos % 100
        if pos==0:
            passes += 1

print(passes)