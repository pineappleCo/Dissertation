from rdflib import Graph
from rdflib.namespace import URIRef

def species(graph):
    taxId_trips = graph.triples((None,
                                 URIRef('http://ppi2rdf.org/proteins#taxId'),
                                 None))

    taxIds = [trip[2].value for trip in taxId_trips]
    distinct_taxIds = list(set(taxIds))
    counts = [taxIds.count(id) for id in distinct_taxIds]
    count_per_tax = list(zip(distinct_taxIds, counts))

    count_per_tax.sort(key=lambda x: x[1])

    print("Distinct Taxinomic IDs are: ")
    print(str(count_per_tax))

    return distinct_taxIds

def get_connected(graph, node):
    connected_subjects = [trip[0] for trip in graph.triples((None, None, node))]
    connected_objects = [trip[2] for trip in graph.triples((node, None, None))]
    return connected_subjects + connected_objects

def get_component(graph, component):
    last_component = []
    all_components = []

    while len(component) != len(last_component):
        for node in component:
            if node not in last_component:
               component = component + get_connected(graph, node)
            last_component = component
        all_components.append(component)

    return component

def connected_components(graph):
    trips = list(graph.triples((None, None, None)))

    nodes = set([subject[0] for subject in trips] + [object[2] for object in trips])

    visited = []
    component = []
    all_components = []

    for node in nodes:
        if node not in visited:
            component = component + node
            component = get_component(graph, component)
        all_components.append(component)
        component = []
        visited = visited + component

    print(all_components)

    return all_components

sources = ["downloads/dip_fix", "downloads/biogrid_fix"]

dip = Graph()
dip.parse(sources[0], format='nt')

cc = connected_components(dip)



