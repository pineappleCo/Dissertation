from rdflib import Graph
from rdflib.namespace import URIRef
import pickler

def species(graph):
    taxId_trips = graph.triples((None,
                                 URIRef('http://ppi2rdf.org/proteins#taxId'),
                                 None))

    taxIds = [trip[2] for trip in taxId_trips]
    distinct_taxIds = list(set(taxIds))
    counts = [taxIds.count(id) for id in distinct_taxIds]
    count_per_tax = list(zip(distinct_taxIds, counts))

    #count_per_tax.sort(key=lambda x: x[1])

    #print("Distinct Taxinomic IDs are: ")
    #print(str(count_per_tax))

    return distinct_taxIds, count_per_tax

def interactors_per_species(ids, graph):
    ints_per_tax = []
    for id in ids:
        interactors = graph.triples((None,
                                    URIRef('http://ppi2rdf.org/proteins#taxId'),
                                    id))
        ints_per_tax.append((id, [trip[0] for trip in interactors]))

    #print(ints_per_tax)
    return ints_per_tax

def check_interactors_per_species(counts_per_tax, ints_per_tax):
    #print(str(len(counts_per_tax)))
    #print(str(len(ints_per_tax)))

    for i in range(len(counts_per_tax)):
        if len(ints_per_tax[i][1]) != counts_per_tax[i][1]:
            print("FAIL")

def interactors_per_interaction(graph):
    ints_per_action = []
    interactions = [trip[0] for trip in graph.triples((None,
                                                       URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                                                       URIRef('http://ppi2rdf.org/proteins#interaction')))]
    for i in interactions:
        ints_per_action.append((i, [trip[2] for trip in graph.triples((i,
                                                                       URIRef('http://ppi2rdf.org/proteins#hasInteractor'),
                                                                       None))]))
    return ints_per_action

def interactions_check(ints_per_action):
    for i in ints_per_action:
        if len(i[1]) > 2:
            print(i[0])

def interactions_with_taxid(ints_per_tax, ints_per_action):
    interactions_labelled_tax = []
    for reaction in ints_per_action:
        for tax in ints_per_tax:
            if set(reaction[1]).issubset(set(tax[1])):
                interactions_labelled_tax.append((reaction[0], reaction[1], tax[0]))
    return interactions_labelled_tax

def tax_dict(tax_ids, ints_with_tax):
    tax_vals = [tax.value for tax in tax_ids]
    tax_dict = {}
    for id in tax_vals:
        species_interactome = [(trip[0], trip[1]) for trip in ints_with_tax if trip[2].value == id]
        tax_dict[id] = species_interactome
    return tax_dict

def get_pin(taxid, interactome):
    nodes = []
    edges = []
    for iaction in interactome:
        nodes.append(iaction[1])
        if len(iaction[1]) == 2:
            edges.append((iaction[1][0], iaction[1][1]))
    flat_nodes = [item for sublist in nodes for item in sublist]
    pickler.pickler('pickles/' + str(taxid) + 'pin', (list(set(flat_nodes)), edges))
    return (list(set(flat_nodes)), edges)

def find_connected_components(pin):
    marked = pin[0]
    print('marked ' + str(marked))
    all_ccs = []
    while marked != []:
        cc = [marked[0]]
        marked = marked[1:]
        cc_size = 1
        cc_next_size = 2
        while cc_size < cc_next_size:
            #add anything connected to anything in cc
            r = None
            for i in marked:
                for edge in pin[1]:
                    if i == edge[0] and edge[1] in cc:
                        cc.append(i)
                        r = i
                    if i == edge[1] and edge[0] in cc:
                        cc.append(i)
                        r = i
                print('cc ' + str(cc))
            #remove anything added from marked
            marked.remove(r)
            print('marked ' + str(marked))
            cc_size = cc_next_size
            cc_next_size = len(cc)
            print('cc_size ' + str(cc_size))
            print('cc_next_size ' + str(cc_next_size))
        all_ccs.append(cc)
    return all_ccs

'''
sources = ["downloads/dip_fix", "downloads/biogrid_fix"]

dip = Graph()
dip.parse(sources[0], format='nt')

tax_ids, counts_per_tax = species(dip)
ints_per_tax = interactors_per_species(tax_ids, dip)
check_interactors_per_species(counts_per_tax, ints_per_tax)
ints_per_action = interactors_per_interaction(dip)
interactions_check(ints_per_action)
ints_with_tax = interactions_with_taxid(ints_per_tax, ints_per_action)
interactomes = tax_dict(tax_ids, ints_with_tax)
pickler.pickler('pickles/interactomes', interactomes)
pins = []
for i in interactomes.keys():
    pins.append(get_pin(i, interactomes[i]))
print('all pins pickled!')
connected_components = []
for pin in pins:
    connected_components.append(find_connected_components(pin))
'''



