from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
import time
import sys

def query(sparql_query, source):
    rdf = Graph()
    rdf.parse(source, format='nt')
    start = time.time()
    result = rdf.query(prepareQuery("""SELECT ?id
                                       WHERE {
                                        ?id <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ppi2rdf.org/proteins#interactor> .
                                        ?id <http://ppi2rdf.org/proteins#taxId> "7227" .
                                       }"""))
    end = time.time()
    for result_part in result:
        print(result_part)
    runtime = end - start
    print(result)
    print(runtime)

if __name__ == '__main__':
    sparql_query = sys.argv[1]
    source = sys.argv[2]
    query(sparql_query, source)

    '''
    qres = g.query(
    """SELECT DISTINCT ?aname ?bname
       WHERE {
          ?a foaf:knows ?b .
          ?a foaf:name ?aname .
          ?b foaf:name ?bname .
       }""")
    '''

