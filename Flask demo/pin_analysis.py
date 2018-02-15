import sys
import igraph
from pickler import unpickle

def edges_to_ids(nodes, edges):
    return [(nodes.index(edge[0]), nodes.index(edge[1])) for edge in edges]

def to_igraph(pin):
    g = igraph.Graph()
    g.add_vertices(pin[0])
    edge_ids = edges_to_ids(pin[0], pin[1])
    g.add_edges(edge_ids)
    print('graph constructed')
    return g

if __name__ == '__main__':
    filename = sys.argv[1]
    pin = unpickle(filename)
    igraph_pin = to_igraph(pin)
    deg_dist = igraph_pin.degree_distribution()
    transitivity = igraph_pin.transitivity_avglocal_undirected()
    close_cen = igraph_pin.closeness()
    bet_cen = igraph_pin.betweenness()
    print(igraph_pin.vcount())
    print(deg_dist)
    print(transitivity)
    print(close_cen)
    print(bet_cen)
