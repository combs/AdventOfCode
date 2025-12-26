import networkx, sys


points = []
graph = networkx.Graph()

with open(sys.argv[1], "r") as fh:
    for line in fh:
        if "," not in line:
            continue
        raw_point = line.split(",")
        point = tuple([int(i) for i in raw_point])
        graph.add_node(point)

distances = []

def compute_distance(p1, p2):
    x_d = pow(p2[0] - p1[0], 2)
    y_d = pow(p2[1] - p1[1], 2)
    z_d = pow(p2[2] - p1[2], 2)
    return pow(x_d + y_d + z_d, 0.5)

def shortest_distance():
    global graph, distances
    for d in sorted(distances):
        if not graph.has_edge(d[1], d[2]):
            yield(d)
    

for node1 in graph.nodes:
    for node2 in graph.nodes:
        d = (compute_distance(node1, node2), node1, node2)
        if d[0] > 0:
            distances.append(d)

desired_joins = 10
if len(sys.argv) > 2:
    desired_joins = int(sys.argv[2])
print("seeking", desired_joins, "joins")
joins = 0

shortest = shortest_distance()

while joins < desired_joins:
    d = next(shortest)
    print("adding edge", d, "for join #", joins)
    graph.add_edge(d[1], d[2])
    joins += 1

chains = networkx.chain_decomposition(graph)
ccs = networkx.algorithms.components.connected_components(graph)

lengths = []

for cc in ccs:
    subgraph = graph.subgraph(cc)
    
    length = len(subgraph)
    lengths.append(length)

sorted_lengths = list(sorted(lengths, reverse=True))
print(sorted_lengths[0] * sorted_lengths[1] * sorted_lengths[2])