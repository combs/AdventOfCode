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
        
        for item in range(fr_int, to_int + 1):
            stringed = str(item)
            le = len(stringed)

            for poss_length in range(1, le // 2 + 1):
                if le % poss_length != 0:
                    continue
                
                first = stringed[0:poss_length]
                identisame = True
                
                for chunk in range(le // poss_length):
                    poss = stringed[chunk * poss_length:(chunk+1) * poss_length]

                    if poss != first:
                        identisame = False
                
                if identisame:
                    print("Repeating sequence found:", item)
                    summed += item
                    break
                
print("Total sum:", summed)