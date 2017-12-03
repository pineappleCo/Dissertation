from rdflib import Graph
from rdflib.namespace import URIRef
#import matplotlib

#matplotlib.use('Agg')

#import matplotlib.pyplot as plt

import plotly
from plotly.graph_objs import *

dip = Graph()
dip.parse("downloads/dip_fix", format='nt')

reference_triples = list(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#hasReference'), None)))
types_triples = list(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#interactionType'), None)))
detection_triples = list(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#methodName'), None)))

unique_interactions = set([trip[0] for trip in reference_triples])
unique_types = set([trip[2] for trip in types_triples])
detection_types = set([trip[2] for trip in detection_triples])

refs_per_interaction = [len(list(set(dip.triples((interaction, URIRef('http://ppi2rdf.org/proteins#hasReference'), None)))))
 for interaction in unique_interactions]
types_per_interaction = [len(list(set(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#interactionType'), type)))))
 for type in unique_types]
detection_per_interaction = [len(list(set(dip.triples((None, URIRef('http://ppi2rdf.org/proteins#methodName'), detection)))))
 for detection in detection_types]

#print(unique_types)
#print(sum(types_per_interaction))
#print(sum(detection_per_interaction))

print(list(zip(unique_interactions, refs_per_interaction)))
print(list(zip(unique_types, types_per_interaction)))
print(list(zip(detection_types, detection_per_interaction)))

#plt.hist(refs_per_interaction, bins=len(refs_per_interaction), log=True)
#plt.savefig("histograms/refs.png")

#plt.hist(types_per_interaction, bins=len(types_per_interaction), log=True, label=list(unique_types))
#plt.savefig("histograms/types.png")

"""
plt.bar(range(len(unique_types)), types_per_interaction, align='center')
plt.xticks(range(len(unique_types)), unique_types)
plt.yscale('log')
plt.ylabel("Count")
plt.xlabel("Reaction Type")
plt.title("Count of Reaction Types (DIP)")
plt.savefig("histograms/interactionTypes.png")
"""

data = [Bar(x=list(map(str, range(max(set(refs_per_interaction)) + 1))), y=[refs_per_interaction.count(c) for c in list(set(refs_per_interaction))])]
layout = Layout(yaxis=dict(type='log', autorange=True))
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='histograms/dipRefCounts.html')

data = [Bar(x=[literal.value for literal in unique_types], y=types_per_interaction)]
layout = Layout(yaxis=dict(type='log', autorange=True))
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='histograms/dipInteractionTypes.html')

data = [Bar(x=[literal.value for literal in detection_types], y=detection_per_interaction)]
layout = Layout(yaxis=dict(type='log', autorange=True))
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='histograms/dipDetectionTypes.html')