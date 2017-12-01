import sys
from rdflib.graph import Graph
from rdflib.namespace import URIRef

def validate(filename, final):
    #read each line is a string in list of strings
    with open(filename) as f:
        datalines = f.read().splitlines()
    f.close()
    datalines.pop(0) #remove first list item
    tabsplit_datalines = [line.split('\t') for line in datalines]
    interactor_triples = list(final.triples((None, URIRef('http://ppi2rdf.org/proteins#hasInteractor'), None)))
    print(interactor_triples)
    interaction_count = len(set([trip[0] for trip in interactor_triples]))
    print(set([trip[0] for trip in interactor_triples]))
    print("There are " + str(interaction_count) + " interactions in the generated RDF.")
    print("There are " + str(len(tabsplit_datalines)) + " interactions in the chosen dataset: " + filename)

def validate_serialized(source, rdf):
    rdf_db = Graph()
    rdf_db.parse(rdf, format='nt')
    with open(source) as f:
        datalines = f.read().splitlines()
    f.close()
    datalines.pop(0) #remove first list item
    tabsplit_datalines = [line.split('\t') for line in datalines]
    interactor_triples = list(rdf_db.triples((None, URIRef('http://ppi2rdf.org/proteins#hasInteractor'), None)))
    interaction_count = len(set([trip[0] for trip in interactor_triples]))
    print("There are " + str(interaction_count) + " interactions in the generated RDF.")
    print("There are " + str(len(tabsplit_datalines)) + " interactions in the chosen dataset: " + source)
    print("Therefore " + str(len(tabsplit_datalines) - interaction_count) + " rows dropped.")

def get_trip_list(filename):
    with open(filename) as f:
        datalines = f.read().splitlines()
    f.close()
    datalines.pop(0) #remove first list item
    triple_store = [line.split('\n') for line in datalines]
    #print(triple_store)
    #todo: use different split for literals
    seperated_triples = [trip[0].split(" ")[:3] for trip in triple_store] # list of lists of 3 strings (one rdf triple)
    print(seperated_triples)
    return seperated_triples

def find(triples, target, not_target=''):
    enumerated_triples = enumerate(triples)
    if not_target == '':
        print("just target")
        subject_contains = [trip for trip in enumerated_triples if trip[1][0].find(target) != -1]
        predicate_contains = [trip for trip in enumerated_triples if trip[1][1].find(target) != -1]
        object_contains = [trip for trip in enumerated_triples if trip[1][2].find(target) != -1]
    else:
        print("not target included")
        subject_contains = [trip for trip in enumerated_triples if trip[1][0].find(target) != -1 and trip[1][0].find(not_target) == -1]
        predicate_contains = [trip for trip in enumerated_triples if trip[1][1].find(target) != -1 and trip[1][1].find(not_target) == -1]
        object_contains = [trip for trip in enumerated_triples if trip[1][2].find(target) != -1 and trip[1][2].find(not_target) == -1]
    print("Triples found with target in subject: ")
    for trip in subject_contains:
        print(trip)
    print("Triples found with target in predicate: ")
    for trip in predicate_contains:
        print(trip)
    print("Triples found with target in object: ")
    for trip in object_contains:
        print(trip)

if __name__ == '__main__':
    source = sys.argv[1]
    trips = get_trip_list(source)
    target = sys.argv[2]
    if len(sys.argv) == 4:
        not_target = sys.argv[3]
        find(trips, target, not_target=not_target)
    else:
        find(trips, target)