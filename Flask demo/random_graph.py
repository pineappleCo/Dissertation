import sys
import random
import igraph
from rdflib import Graph
from rdflib.namespace import URIRef

def interactors_per_interaction(graph):
    ints_per_action = []
    interactions = [trip[0] for trip in graph.triples((None,
                                                       URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                                                       URIRef('http://ppi2rdf.org/proteins#interaction')))]
    for i in interactions:
        ints_per_action.append((i, [trip[2] for trip in graph.triples((i,
                                                                       URIRef('http://ppi2rdf.org/proteins#hasInteractor'),
                                                                       None))]))
    #list of tuples - tup[0] == interaction id, tup[1] == [interactorA id, interactorB id]
    return ints_per_action

def weight_by_refCount(ints_per_action, graph):
    weighted_ints_per_action = []
    for interaction in ints_per_action:
        refCount = len(list(graph.triples((interaction[0], URIRef('http://ppi2rdf.org/proteins#hasReference'), None))))
        weighted_edge = interaction + (refCount, )
        weighted_ints_per_action.append(weighted_edge)
    return weighted_ints_per_action

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
    weight = sys.argv[2]
    no_edges = sys.argv[3]
    how_many = sys.argv[4]

    db = Graph()
    db.parse(filename, format='nt')

    ints_per_action = interactors_per_interaction(db)

    if weight == 'weight':
        weighted_ints_per_action = weight_by_refCount(ints_per_action, db)
        print(weighted_ints_per_action[:10])
        print(len(weighted_ints_per_action))

    random_pin = ([], [])
    avg_trans = []
    already_chosen = []
    new_edge = False

    for i in range(int(how_many)):
        for j in range(int(no_edges)):
            while new_edge == False:
                rand_edge = random.randint(0, len(ints_per_action)-1)
                if rand_edge not in already_chosen:
                    new_edge = True
                    already_chosen.append(rand_edge)
            random_pin[0].append(ints_per_action[rand_edge][1][0])
            if len(ints_per_action[rand_edge][1]) > 1:
                random_pin[0].append(ints_per_action[rand_edge][1][1])
                random_pin[1].append((ints_per_action[rand_edge][1][0], ints_per_action[rand_edge][1][1]))
            new_edge = False
        already_chosen = []
        igraph_pin = to_igraph(random_pin)
        transitivity = igraph_pin.transitivity_avglocal_undirected()
        print(transitivity)
        avg_trans.append(transitivity)

    print('Average transitivity of random graphs from ' + str(how_many) + ' trials:')
    print(sum(avg_trans)/len(avg_trans))

'''
https://medium.com/@peterkellyonline/weighted-random-selection-3ff222917eb6
add up all the weights for all the items in the list
Pick a number at random between 1 and the sum of the weights
Iterate over the items
For the current item, subtract the item’s weight from the random number that was originally picked
Compare the result to zero. If less than or equal to zero then break otherwise keep iterating. The key is that the larger
the weight the more likely to be less than zero when compared to the random selection between zero and the sum of weights.
If not less than zero, continue iterating over the list, all the while subtracting more and more weights off the random
number chosen from the sum of the weights.
'''











