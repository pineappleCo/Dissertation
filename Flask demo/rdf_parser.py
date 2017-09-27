import sys
from rdflib import Graph, Literal
from rdflib.namespace import Namespace, RDF, URIRef, RDFS, OWL

def store_rdf(data_lines, genename_dict):

	ppi = Namespace("http://ppi2rdf.org/proteins#")
	pmed = Namespace("http://www.ncbi.nlm.nih.gov/pubmed/")
	# Note: ppi.attribute vs. ppi[item]

	g = Graph()

	sys.stderr.write("Storing RDF")

	for i, line in enumerate(data_lines):

		if (i % 10000 == 0):
			sys.stderr.write(".")
		# Add classes
        # \t for horizontal tab
		interaction_id = line.split('\t')[10]
		pubmed_id = line.split('\t')[5]
		entrez_1 = line.split('\t')[0]
		entrez_2 = line.split('\t')[1]

		interaction = URIRef(ppi[interaction_id])
		reference = URIRef(pmed[pubmed_id])
		gene1 = URIRef(ppi[entrez_1])
		gene2 = URIRef(ppi[entrez_2])

		g.add( (interaction, RDF.type, ppi.interaction) )
		g.add( (reference, RDF.type, ppi.primaryRef) )
		g.add( (gene1, RDF.type, ppi.interactor) )
		g.add( (gene2, RDF.type, ppi.interactor) )

		# Bind to interaction
		method_name = line.split('\t')[2]
		method_id = line.split('\t')[3]
		source = line.split('\t')[9]
		interaction_type = line.split('\t')[8]

		g.add( (interaction, ppi.hasInteractor, gene1) )

		# if self-loop, add type
		if (interaction, ppi.hasInteractor, gene2) in g:
			g.add( (interaction, RDF.type, ppi.selfInteractor) )
		else:
			g.add( (interaction, ppi.hasInteractor, gene2) )

		g.add( (interaction, ppi.hasReference, reference) )

		g.add( (interaction, ppi.methodName, Literal(method_name)) )
		g.add( (interaction, ppi.methodID, Literal(method_id)) )
		g.add( (interaction, ppi.source, Literal(source)) )
		g.add( (interaction, ppi.interactionType, Literal(interaction_type)) )

		# Bind to reference
		author = line.split('\t')[4]

		g.add( (reference, ppi.firstAuthor, Literal(author)) )
		g.add( (reference, ppi.pubmed, Literal(pubmed_id)) )

		# Bind to interactor
		taxid_1 = line.split('\t')[6]
		taxid_2 = line.split('\t')[7]

		g.add( (gene1, ppi.taxId, Literal(taxid_1)) )
		g.add( (gene2, ppi.taxId, Literal(taxid_2)) )
		g.add( (gene1, ppi.entrez, Literal(entrez_1)) )
		g.add( (gene2, ppi.entrez, Literal(entrez_2)) )


		if entrez_1 in genename_dict:
			genename_1 = genename_dict[entrez_1]
			g.add( (gene1, ppi.geneName, Literal(genename_1)) )
		if entrez_2 in genename_dict:
			genename_2 = genename_dict[entrez_2]
			g.add( (gene2, ppi.geneName, Literal(genename_2)) )

	return g

def create_schema():
    schema = Graph() # create new schema

	# Import Namespaces and Schema
	ppi = Namespace("http://ppi2rdf.org/proteins#")
	xmls = Namespace("http://www.w3.org/2001/XMLSchema#")

	# Classes
	schema.add( (ppi.interaction, RDF.type, OWL.Class) ) 	# the interaction id
	schema.add( (ppi.interactor, RDF.type, OWL.Class) ) 	# the entrez id
	schema.add( (ppi.primaryRef, RDF.type, OWL.Class) ) 	# the pubmed id

	# Subclasses
	schema.add( (ppi.psdGene, RDF.type, OWL.Class) ) # post-synaptic density gene
	schema.add( (ppi.psdGene, RDFS.subClassOf, ppi.interactor) )

	schema.add( (ppi.selfInteractor, RDF.type, OWL.Class) )
	schema.add( (ppi.selfInteractor, RDFS.subClassOf, ppi.interaction) )

	# Interaction Properties
	schema.add( (ppi.hasInteractor, RDF.type, OWL.ObjectProperty) )
	schema.add( (ppi.hasInteractor, RDFS.domain, ppi.interaction) )
	schema.add( (ppi.hasInteractor, RDFS.range, ppi.interactor) )

	schema.add( (ppi.hasReference, RDF.type, OWL.ObjectProperty) )
	schema.add( (ppi.hasReference, RDFS.domain, ppi.interaction) )
	schema.add( (ppi.hasReference, RDFS.range, ppi.primaryRef) )

	schema.add( (ppi.methodName, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.methodName, RDFS.domain, ppi.interaction) )
	schema.add( (ppi.methodName, RDFS.range, xmls.string) )

	schema.add( (ppi.methodId, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.methodId, RDFS.domain, ppi.interaction) )
	schema.add( (ppi.methodId, RDFS.range, xmls.string) )

	schema.add( (ppi.source, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.source, RDFS.domain, ppi.interaction) )
	schema.add( (ppi.source, RDFS.range, xmls.string) )

	schema.add( (ppi.interactionType, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.interactionType, RDFS.domain, ppi.interaction) )
	schema.add( (ppi.interactionType, RDFS.range, xmls.string) )

	# Interactor Properties

	schema.add( (ppi.entrez, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.entrez, RDFS.domain, ppi.interactor) )
	schema.add( (ppi.entrez, RDFS.range, xmls.string) )

	schema.add( (ppi.taxId, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.taxId, RDFS.domain, ppi.interactor) )
	schema.add( (ppi.taxId, RDFS.range, xmls.string) )

	schema.add( (ppi.geneName, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.geneName, RDFS.domain, ppi.interactor) )
	schema.add( (ppi.geneName, RDFS.range, xmls.string) )

	# homologene  (interactor) <--> (interactor)
	schema.add( (ppi.hasHomologene, RDF.type, OWL.ObjectProperty) )
	schema.add( (ppi.hasHomologene, RDFS.domain, ppi.interactor) )
	schema.add( (ppi.hasHomologene, RDFS.range, ppi.interactor) )

	# PrimaryRef Properties

	schema.add( (ppi.pubmed, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.pubmed, RDFS.domain, ppi.primaryRef) )
	schema.add( (ppi.pubmed, RDFS.range, xmls.string) )

	schema.add( (ppi.firstAuthor, RDF.type, OWL.DatatypeProperty) )
	schema.add( (ppi.firstAuthor, RDFS.domain, ppi.primaryRef) )
	schema.add( (ppi.firstAuthor, RDFS.range, xmls.string) )

    return schema

def parse(filepath):
    data_lines = []
    genename_dict = {}
    gh = Graph()
    gpsd = Graph()
    schema = create_schema()
    if data_lines != []:
        g = store_rdf(data_lines, genename_dict)
    graph = gs + g + gh + gpsd
    graph.serialize("downloads", format='nt')