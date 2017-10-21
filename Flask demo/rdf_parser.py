import sys
from rdflib.namespace import Namespace, RDF, URIRef, RDFS, OWL
from rdflib import Graph, Literal, BNode

def parse(filename, source):
    #read each line is a string in list of strings
    with open(filename) as f:
        datalines = f.read().splitlines()
    datalines.pop(0) #remove first list item
    print(datalines)
    tabsplit_datalines = [line.split('\t') for line in datalines]
    print(tabsplit_datalines)
    if source == "biogrid":
        filtered = [biogrid_filter(line) for line in tabsplit_datalines]
    elif source == "dip":
        filtered = [dip_filter(line) for line in tabsplit_datalines]
    elif source == "intact":
        filtered = [intact_filter(line) for line in tabsplit_datalines]
    else:
        return "not a supported source, supported sources are biogrid, intact and dip"
    return filtered

def biogrid_filter(tab_split):
    interactorAId = tab_split[0][22:]
    interactorBId = tab_split[1][22:]
    detectionMethod = tab_split[6].split('(')[1][:-1]
    author = tab_split[7]
    pubId = tab_split[8][7:]
    taxA = tab_split[9][6:]
    taxB = tab_split[10][6:]
    interactionType = tab_split[11].split('(')[1][:-1]
    source = "biogrid"
    interactionId = tab_split[13][8:]
    return [interactorAId, interactorBId, detectionMethod, author, pubId, taxA, taxB, interactionType, source, interactionId]

def dip_filter(tab_split):
    interactorAId = tab_split[0].split('|')[0]
    interactorBId = tab_split[1].split('|')[0]
    detectionMethod = tab_split[6].split('(')[1][:-1]
    author = tab_split[7]
    pubId = list(set([pub[7:] for pub in tab_split[8].split('|')]))
    taxA = tab_split[9][6:].split('(')[0][:-1]
    taxB = tab_split[10][6:].split('(')[0][:-1]
    interactionType = tab_split[11].split('(')[1][:-1]
    source = "dip"
    interactionId = tab_split[13]
    return [interactorAId, interactorBId, detectionMethod, author, pubId, taxA, taxB, interactionType, source, interactionId]

def intact_filter(tab_split):
    interactorAId = tab_split[0][10:]
    interactorBId = tab_split[1][10:]
    detectionMethod = tab_split[6].split('(')[1][:-1]
    author = tab_split[7]
    pubId = list(set([pub.split(':')[1] for pub in tab_split[8].split('|')]))
    taxA = list(set([pub.split(':')[1].split('(')[0] for pub in tab_split[9].split('|')]))
    taxB = list(set([pub.split(':')[1].split('(')[0] for pub in tab_split[10].split('|')]))
    interactionType = tab_split[11].split('(')[1][:-1]
    source = "intact"
    interactionId = list(set([id.split(':')[1] for id in tab_split[13].split('|')]))
    bioRoleA = tab_split[16].split('(')[1][:-1]
    bioRoleB = tab_split[17].split('(')[1][:-1]
    experimentRoleA = tab_split[18].split('(')[1][:-1]
    experimentRoleB = tab_split[19].split('(')[1][:-1]
    hostOrganism = list(set([tax.split(':')[1].split('(')[0] for tax in tab_split[28].split('|')]))
    creation = tab_split[30]
    update = tab_split[31]
    featuresA = tab_split[36].split('(')[1][:-1]
    featuresB = tab_split[37].split('(')[1][:-1]
    stoichiometryA = tab_split[38]
    stoichiometryB = tab_split[39]
    idMethodA = tab_split[40].split('(')[1][:-1]
    idMethodB = tab_split[41].split('(')[1][:-1]
    return [interactorAId, interactorBId, detectionMethod, author, pubId, taxA, taxB, interactionType, source, interactionId,
            bioRoleA, bioRoleB, experimentRoleA, experimentRoleB, hostOrganism, creation, update, featuresA, featuresB,
            stoichiometryA, stoichiometryB, idMethodA, idMethodB]

def schema(source):
    schema = Graph()

    ppi = Namespace("http://ppi2rdf.org/proteins#")
    xmls = Namespace("http://www.w3.org/2001/XMLSchema")

    #Classes
    schema.add((ppi.interaction, RDF.type, OWL.Class))
    schema.add((ppi.interactor, RDF.type, OWL.Class))
    schema.add((ppi.primaryRef, RDF.type, OWL.Class))

    #Interaction Properties
    schema.add((ppi.interactionId, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.interactionId, RDFS.domain, ppi.interaction))
    schema.add((ppi.interactionId, RDFS.range, xmls.string))

    schema.add((ppi.hasInteractor, RDF.type, OWL.ObjectProperty))
    schema.add((ppi.hasInteractor, RDFS.domain, ppi.interaction))
    schema.add((ppi.hasInteractor, RDFS.range, ppi.interactor))

    schema.add((ppi.hasReference, RDF.type, OWL.ObjectProperty))
    schema.add((ppi.hasReference, RDFS.domain, ppi.interaction))
    schema.add((ppi.hasReference, RDFS.range, ppi.primaryRef))

    schema.add((ppi.methodName, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.methodName, RDFS.domain, ppi.interaction))
    schema.add((ppi.methodName, RDFS.range, xmls.string))

    schema.add((ppi.methodId, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.methodId, RDFS.domain, ppi.interaction))
    schema.add((ppi.methodId, RDFS.range, xmls.string))

    schema.add((ppi.source, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.source, RDFS.domain, ppi.interaction))
    schema.add((ppi.source, RDFS.range, xmls.string))

    schema.add((ppi.interactionType, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.interactionType, RDFS.domain, ppi.interactor))
    schema.add((ppi.interactionType, RDFS.range, xmls.string))

    if source == "intact":
        schema.add((ppi.hostOrganism, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.hostOrganism, RDFS.domain, ppi.interaction))
        schema.add((ppi.hostOrganism, RDFS.range, xmls.string))

        schema.add((ppi.creation, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.creation, RDFS.domain, ppi.interaction))
        schema.add((ppi.creation, RDFS.range, xmls.string))

        schema.add((ppi.update, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.update, RDFS.domain, ppi.interaction))
        schema.add((ppi.update, RDFS.range, xmls.string))

    #Interactor Properties
    schema.add((ppi.entrez, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.entrez, RDFS.domain, ppi.interactor))
    schema.add((ppi.entrez, RDFS.range, xmls.string))

    schema.add((ppi.taxId, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.taxId, RDFS.domain, ppi.interactor))
    schema.add((ppi.taxId, RDFS.range, xmls.string))

    schema.add((ppi.geneName, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.geneName, RDFS.domain, ppi.interactor))
    schema.add((ppi.geneName, RDFS.range, xmls.string))

    schema.add((ppi.hasHomologene, RDF.type, OWL.ObjectProperty))
    schema.add((ppi.hasHomologene, RDFS.domain, ppi.interactor))
    schema.add((ppi.hasHomologene, RDFS.range, ppi.interactor))

    if source == "intact":
        schema.add((ppi.bioRole, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.bioRole, RDFS.domain, ppi.interactor))
        schema.add((ppi.bioRole, RDFS.range, xmls.string))

        schema.add((ppi.experimentRole, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.experimentRole, RDFS.domain, ppi.interaction))
        schema.add((ppi.experimentRole, RDFS.range, xmls.string))

        schema.add((ppi.features, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.features, RDFS.domain, ppi.interaction))
        schema.add((ppi.features, RDFS.range, xmls.string))

        schema.add((ppi.stoichiometry, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.stoichiometry, RDFS.domain, ppi.interaction))
        schema.add((ppi.stoichiometry, RDFS.range, xmls.string))

        schema.add((ppi.idMethod, RDF.type, OWL.DatatypeProperty))
        schema.add((ppi.idMethod, RDFS.domain, ppi.interaction))
        schema.add((ppi.idMethod, RDFS.range, xmls.string))

    #PrimaryRef Properties
    schema.add((ppi.pubmed, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.pubmed, RDFS.domain,ppi.primaryRef))
    schema.add((ppi.pubmed, RDFS.range, xmls.string))

    schema.add((ppi.firstAuthor, RDF.type, OWL.DatatypeProperty))
    schema.add((ppi.firstAuthor, RDFS.domain, ppi.primaryRef))
    schema.add((ppi.firstAuthor, RDFS.range, xmls.string))

    return schema

#for testing
if __name__ == '__main__':
    filename = sys.argv[1]
    source = sys.argv[2]
    schema = schema(source)
    print(parse(filename, source))