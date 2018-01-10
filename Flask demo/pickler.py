import pickle
from rdflib.graph import Graph

def read_graph(filename):
    rdf_db = Graph()
    rdf_db.parse(filename, format='nt')
    return rdf_db

def pickler(filename, to_pickle):
    file = open(filename, 'wb')
    pickle.dump(to_pickle, file)
    file.close()
    print(str(to_pickle) + " pickled to " + filename)

def unpickle(filename):
    file = open(filename, 'rb')
    return pickle.load(file)

#sources = ["downloads/dip_fix", "downloads/biogrid_fix"]

#for db in sources:
    #rdf_graph = read_graph(db)
    #pickler('pickles/' + db[10:], rdf_graph)
