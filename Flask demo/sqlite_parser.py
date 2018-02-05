import sqlite3
import sys
import rdf_parser

def build_dbs(source, dbs_name):
    dbs = sqlite3.connect(dbs_name)
    cursor = dbs.cursor()
    if source == 'dip' or source == 'biogrid':
        dip_and_biogrid_schema(cursor)
    elif source == 'intact':
        intact_schema(cursor)
    dbs.commit()

def dip_and_biogrid_schema(cursor):
    cursor.execute('''
        CREATE TABLE interactions(
            id TEXT,
            interactorA TEXT,
            interactorB TEXT,
            reference TEXT,
            methodName TEXT,
            source TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE interactors(
            entrez TEXT,
            taxId INTEGER,
            interactionType TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE refs(
            pubmedId TEXT,
            firstAuthor TEXT)
    ''')

def intact_schema(cursor):
    cursor.execute('''
        CREATE TABLE interactions(
            id TEXT,
            interactorA TEXT,
            interactorB TEXT,
            reference TEXT,
            methodName TEXT,
            source TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE interactors(
            entrez TEXT,
            taxId INTEGER,
            interactionType TEXT,
            bioRole TEXT,
            experimentRole TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE refs(
            pubmedId TEXT,
            firstAuthor TEXT)
    ''')

def populate(filtered, source, dbs_name):
    dbs = sqlite3.connect(dbs_name)
    cursor = dbs.cursor()
    if source == 'dip' or source == 'biogrid':
        dip_and_biogrid_pop(cursor, filtered)
    elif source == 'intact':
        intact_pop(cursor, filtered)
    dbs.commit()

def dip_and_biogrid_pop(cursor, filtered):

    interactions = [(entry[9], entry[0], entry[1], entry[4][0], entry[2], entry[8]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactions(
            id,
            interactorA,
            interactorB,
            reference,
            methodName,
            source) VALUES (?,?,?,?,?,?)
    ''', interactions)

    interactors = [(entry[0], entry[5], entry[7]) for entry in filtered] + [(entry[1], entry[6], entry[7]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactors(
            entrez,
            taxId,
            interactionType) VALUES (?,?,?)
    ''', interactors)

    references = [(entry[4][0], entry[3]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO refs(
            pubmedId,
            firstAuthor) VALUES (?,?)
    ''', references)

def intact_pop(cursor, filtered):
    interactions = [(entry[9], entry[0], entry[1], entry[4][0], entry[2], entry[8]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactions(
            id,
            interactorA,
            interactorB,
            reference,
            methodName,
            source) VALUES (?,?,?,?,?,?)
    ''', interactions)

    interactors = [(entry[0], entry[5][0], entry[7], entry[10], entry[12]) for entry in filtered] + [(entry[1], entry[6][0], entry[7], entry[11], entry[13]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactors(
            entrez,
            taxId,
            interactionType,
            bioRole,
            experimentRole) VALUES (?,?,?,?,?)
    ''', interactors)

    references = [(entry[4][0], entry[3]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO refs(
            pubmedId,
            firstAuthor) VALUES (?,?)
    ''', references)

if __name__ == '__main__':
    filename = sys.argv[1]
    source = sys.argv[2]
    dbs_name = sys.argv[3]
    filtered = rdf_parser.parse(filename, source)
    build_dbs(source, dbs_name)
    populate(filtered, source, dbs_name)
