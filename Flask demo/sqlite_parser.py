import sqlite3
import sys
import rdf_parser

def build_dbs(source, dbs_name):
    dbs = sqlite3.connect(dbs_name)
    cursor = dbs.cursor()
    if source == 'dip':
        dip_schema(cursor)
    elif source == 'biogrid':
        biogrid_schema(cursor)
    elif source == 'intact':
        intact_schema(cursor)
    dbs.commit()

def dip_schema(cursor):
    cursor.execute('''
        CREATE TABLE interactions(
            id TEXT,
            interactorA TEXT,
            interactorB TEXT,
            interactionType TEXT,
            reference TEXT,
            methodName TEXT,
            source TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE interactors(
            entrez TEXT,
            taxId INTEGER)
    ''')

    cursor.execute('''
        CREATE TABLE refs(
            pubmedId TEXT,
            firstAuthor TEXT)
    ''')

def biogrid_schema(cursor):
    cursor.execute('''
        CREATE TABLE interactions(
            id TEXT,
            interactorA TEXT,
            interactorB TEXT,
            interactionType TEXT,
            reference TEXT,
            methodName TEXT,
            source TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE interactors(
            entrez TEXT,
            taxId INTEGER)
    ''')

    cursor.execute('''
        CREATE TABLE refs(
            pubmedId TEXT,
            firstAuthor TEXT,
            year INTEGER)
    ''')

def intact_schema(cursor):
    cursor.execute('''
        CREATE TABLE interactions(
            id TEXT,
            interactorA TEXT,
            interactorB TEXT,
            interactionType TEXT,
            reference TEXT,
            methodName TEXT,
            source TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE interactors(
            entrez TEXT,
            taxId INTEGER,
            bioRole TEXT,
            experimentRole TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE refs(
            pubmedId TEXT,
            firstAuthor TEXT,
            year INTEGER)
    ''')

def populate(filtered, source, dbs_name):
    dbs = sqlite3.connect(dbs_name)
    cursor = dbs.cursor()
    if source == 'dip':
        dip_pop(cursor, filtered)
    elif source == 'biogrid':
        biogrid_pop(cursor, filtered)
    elif source == 'intact':
        intact_pop(cursor, filtered)
    dbs.commit()

def dip_pop(cursor, filtered):

    interactions = [(entry[9], entry[0], entry[1], entry[7], entry[4][0], entry[2], entry[8]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactions(
            id,
            interactorA,
            interactorB,
            interactionType,
            reference,
            methodName,
            source) VALUES (?,?,?,?,?,?,?)
    ''', interactions)

    interactors = [(entry[0], entry[5]) for entry in filtered] + [(entry[1], entry[6]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactors(
            entrez,
            taxId) VALUES (?,?)
    ''', interactors)

    references = [(entry[4][0], entry[3]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO refs(
            pubmedId,
            firstAuthor) VALUES (?,?)
    ''', references)

def biogrid_pop(cursor, filtered):

    interactions = [(entry[9], entry[0], entry[1], entry[7], entry[4], entry[2], entry[8]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactions(
            id,
            interactorA,
            interactorB,
            interactionType,
            reference,
            methodName,
            source) VALUES (?,?,?,?,?,?,?)
    ''', interactions)

    interactors = [(entry[0], entry[5]) for entry in filtered] + [(entry[1], entry[6]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactors(
            entrez,
            taxId) VALUES (?,?)
    ''', interactors)

    references = [(entry[4], entry[3], entry[10]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO refs(
            pubmedId,
            firstAuthor,
            year) VALUES (?,?,?)
    ''', references)

def intact_pop(cursor, filtered):
    interactions = [(entry[9], entry[0], entry[1], entry[7], entry[4][0], entry[2], entry[8]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactions(
            id,
            interactorA,
            interactorB,
            interactionType,
            reference,
            methodName,
            source) VALUES (?,?,?,?,?,?,?)
    ''', interactions)

    interactors = [(entry[0], entry[5][0], entry[10], entry[12]) for entry in filtered] + [(entry[1], entry[6][0], entry[11], entry[13]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO interactors(
            entrez,
            taxId,
            bioRole,
            experimentRole) VALUES (?,?,?,?)
    ''', interactors)

    references = [(entry[4][0], entry[3], entry[len(entry)-1]) for entry in filtered]

    cursor.executemany('''
        INSERT INTO refs(
            pubmedId,
            firstAuthor,
            year) VALUES (?,?,?)
    ''', references)

if __name__ == '__main__':
    filename = sys.argv[1]
    source = sys.argv[2]
    dbs_name = sys.argv[3]
    filtered = rdf_parser.parse(filename, source)
    build_dbs(source, dbs_name)
    populate(filtered, source, dbs_name)
