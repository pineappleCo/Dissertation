import sys
import igraph
from pickler import unpickle

def edges_to_ids(nodes, edges):
    return [(nodes.index(edge[0]), nodes.index(edge[1])) for edge in edges]

def cc_for_pin(pin):
    g = igraph.Graph()
    g.add_vertices(pin[0])
    edge_ids = edges_to_ids(pin[0], pin[1])
    g.add_edges(edge_ids)
    print('graph constructed')

    ccs = g.components(mode='STRONG')
    cc_subgs = ccs.subgraphs()

    sums = []

    for graph in cc_subgs:
        sums.append(graph.summary(verbosity=0))

    f = open('summary.txt', 'w')

    for summary in sums:
        f.write("%s\n" % summary)

if __name__ == '__main__':
    filename = sys.argv[1]
    pin = unpickle(filename)
    cc_for_pin(pin)