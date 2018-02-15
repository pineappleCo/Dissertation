from rdf_parser import parse

#(Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrix),

def interaction_to_cypher(interaction):
    interactorA = '(' + interaction[0].replace('-', '') + ':Interactor {tax:' + interaction[5] + '})'
    interactorB = '(' + interaction[1].replace('-', '') + ':Interactor {tax:' + interaction[6] + '})'
    interactionEdge = '(' + interaction[0].replace('-', '') + ')' \
                      '-[:INTERACTS_WITH {' \
                                           "detectionMethod:'" + interaction[2] + "', "  \
                                           "author:'" + interaction[3] + "', " \
                                           "pubId:" + str(interaction[4]) + ", " \
                                           "interactionType:'" + interaction[7] + "', " \
                                           "source:'" + interaction[8] + "', " \
                                           "interactionId:'" + interaction[9] + '}]' \
                      '->(' + interaction[1].replace('-', '') + ')'
    return [interactorA, interactorB, interactionEdge]

if __name__ == '__main__':
    parse = parse('dip.txt', 'dip')

    schema = []
    for interaction in parse:
        schema.extend(interaction_to_cypher(interaction))

    out = open("dip_cypher.txt", "w")
    out.write('begin')
    out.write("\n")
    out.write('CREATE')
    out.write("\n")
    i = 0
    for line in schema:
        i = i + 1
        # write line to output file
        if i == 500:
            out.write("\t" + line)
            out.write("\n")
            out.write("commit")
            out.write("\n")
            out.write("exit")
            out.write("\n")
            out.write('begin')
            out.write("\n")
        else:
            out.write("\t" + line + ",")
            out.write("\n")

    out.close()

