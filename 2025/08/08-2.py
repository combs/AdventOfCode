import networkx, sys

points = []
graph = networkx.Graph()

def compute_distance(p1, p2):
    x_d = pow(p2[0] - p1[0], 2)
    y_d = pow(p2[1] - p1[1], 2)
    z_d = pow(p2[2] - p1[2], 2)
    return pow(x_d + y_d + z_d, 0.5)

def get_segments(g):
    l = len(list(networkx.algorithms.components.connected_components(g)))
    print(l)
    return l

def shortest_distance():
    global graph, distances
    for d in sorted(distances):
        if not graph.has_edge(d[1], d[2]):
            yield(d)
    
with open(sys.argv[1], "r") as fh:
    for line in fh:
        if "," not in line:
            continue
        raw_point = line.split(",")
        point = tuple([int(i) for i in raw_point])
        graph.add_node(point)

distances = []

for node1 in graph.nodes:
    for node2 in graph.nodes:
        d = (compute_distance(node1, node2), node1, node2)
        if d[0] > 0:
            distances.append(d)

shortest = shortest_distance()

xy = 0

while get_segments(graph) > 1:
    d = next(shortest)
    print("adding edge", d, "for join #", joins)
    graph.add_edge(d[1], d[2])
    xy = d[1][0] * d[2][0]

print(xy)