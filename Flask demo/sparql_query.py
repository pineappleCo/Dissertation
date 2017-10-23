import rdflib

def query(sparql_query, rdf_graph):
    result = rdf_graph.query(sparql_query)
    for result_part in result:
        print(result_part)
    return result

