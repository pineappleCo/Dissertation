import rdf_parser

#finding field lengths for sql schema

filename = ["dip.txt", "biogrid.txt", "intact.txt"]
source = ['dip', 'biogrid', 'intact']

for file, db in zip(filename, source):
    filtered = rdf_parser.parse(file, db)

    lengths = [len(field) for field in filtered[0]]

    print(len(lengths))

    for entry in filtered[1:]:
        for i in range(len(entry)):
            if len(entry[i]) > lengths[i]:
                lengths[i] = len(entry[1])

    print(db)
    print(lengths)