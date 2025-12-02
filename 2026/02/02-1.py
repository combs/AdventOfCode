import sys
import pyparsing as pp

summed = 0
pattern = pp.Word(pp.nums) + "-" + pp.Word(pp.nums)

with open(sys.argv[1], "r") as fh:
    expressions = fh.read()

    for expr in expressions.split(","):

        (fr, zap, to) = pattern.parse_string(expr)
        fr_int = int(fr)
        to_int = int(to)
        
        print(fr, to)

        for item in range(fr_int, to_int + 1):
            stringed = str(item)
            if len(stringed) % 2 == 1:
                continue
            halfway = len(stringed)//2

            if stringed[0:halfway] == stringed[halfway:]:
                print("Duplicate found:", stringed)
                summed += item
                
print("Total sum:", summed)