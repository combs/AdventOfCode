import itertools, sys
points = []

with open(sys.argv[1], "r") as fh:
    for line in fh:
        x, y = [ int(i) for i in line.strip().split(",") ] 
        points.append((x, y))

areas = []

for (left, right) in itertools.combinations(points, 2):
    xd = abs(left[0] - right[0]) + 1
    yd = abs(left[1] - right[1]) + 1
    area = xd * yd
    areas.append( (area, left, right))

print(list(sorted(areas, reverse=True))[0])
