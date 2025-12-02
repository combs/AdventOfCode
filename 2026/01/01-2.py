import sys
import pyparsing as pp

pos = 50
integer = pp.Word(pp.nums)
pattern = pp.Char(["L", "R"]) + pp.pyparsing_common.integer()
passes = 0

yoyo_next_loop = 0

with open(sys.argv[1], "r") as fh:
    for line in fh.readlines():
        new_passes = 0

        (dir_str, amount) = pattern.parse_string(line)
        direction = -1 if dir_str == "L" else 1
        
        to_go = amount * direction
        
        print(pos, to_go)

        while to_go:
            if to_go > 0:
                to_go -= 1
                pos -= 1
            else:
                to_go += 1
                pos += 1
            
            pos = pos % 100

            if pos == 0:
                passes += 1

print(passes)