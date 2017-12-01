from rdflib import Graph
from rdflib.namespace import URIRef
import matplotlib.pyplot as plt

dip = Graph()
dip.parse("downloads/dip_alt_refs", format='nt')

reference_triples = list(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#hasReference'), None)))
types_triples = list(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#interactionType'), None)))

unique_interactions = set([trip[0] for trip in reference_triples])
unique_types = set([trip[2] for trip in types_triples])

refs_per_interaction = [len(list(set(dip.triples((interaction, URIRef('http://ppi2rdf.org/proteins#hasReference'), None)))))
 for interaction in unique_interactions]
types_per_interaction = [len(list(set(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#interactionType'), type)))))
 for type in unique_types]

print(unique_types)
print(types_per_interaction)

#plt.hist(refs_per_interaction)
#plt.savefig("histograms/refs.png")

print(list(zip(unique_types, types_per_interaction)))

plt.hist(types_per_interaction)
plt.savefig("histograms/types.png")