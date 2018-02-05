from rdflib import Graph
from rdflib.namespace import URIRef
import plotly
from plotly.graph_objs import *

#dip = Graph()
#biogrid = Graph()
intact = Graph()
#dip.parse("downloads/dip_fix", format='nt')
#biogrid.parse("downloads/biogrid_fix", format='nt')
intact.parse("downloads/intact_rdf", format='nt')

#sources = [dip, biogrid, intact]
#str_sources = ['DIP', 'Biogrid', 'intact']
sources = [intact]
str_sources = ['intact']
i = 0

for db in sources:
    reference_triples = list(db.triples((None,
                                         URIRef('http://ppi2rdf.org/proteins#hasReference'),
                                         None)))
    types_triples = list(db.triples((None,
                                     URIRef('http://ppi2rdf.org/proteins#interactionType'),
                                     None)))
    detection_triples = list(db.triples((None,
                                         URIRef('http://ppi2rdf.org/proteins#methodName'),
                                         None)))

    unique_interactions = set([trip[0] for trip in reference_triples])
    unique_types = set([trip[2] for trip in types_triples])
    detection_types = set([trip[2] for trip in detection_triples])

    refs_per_interaction = [len(list(set(db.triples((interaction,
                                                     URIRef('http://ppi2rdf.org/proteins#hasReference'),
                                                     None)))))
                            for interaction in unique_interactions]
    types_per_interaction = [len(list(set(db.triples((None,
                                                       URIRef('http://ppi2rdf.org/proteins#interactionType'),
                                                       type)))))
                             for type in unique_types]
    detection_per_interaction = [len(list(set(db.triples((None,
                                                          URIRef('http://ppi2rdf.org/proteins#methodName'),
                                                          detection)))))
                                 for detection in detection_types]
    print(str_sources[i])
    print(list(zip(unique_interactions, refs_per_interaction)))
    print(list(zip(unique_types, types_per_interaction)))
    print(list(zip(detection_types, detection_per_interaction)))

    data = [Bar(x=list(map(str, range(max(set(refs_per_interaction)) + 1))), y=[refs_per_interaction.count(c) for c in list(set(refs_per_interaction))])]
    layout = Layout(yaxis=dict(type='log', autorange=True))
    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='histograms/' + str_sources[i] + 'RefCounts.html')

    data = [Bar(x=[literal.value for literal in unique_types], y=types_per_interaction)]
    layout = Layout(yaxis=dict(type='log', autorange=True))
    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='histograms/' + str_sources[i] + 'InteractionTypes.html')

    data = [Bar(x=[literal.value for literal in detection_types], y=detection_per_interaction)]
    layout = Layout(yaxis=dict(type='log', autorange=True))
    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='histograms/' + str_sources[i] + 'DetectionTypes.html')

    i = i + 1