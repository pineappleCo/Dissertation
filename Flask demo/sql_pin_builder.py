import sqlite3
import sys

def get_all_taxids(cursor):
    cursor.execute('''
        SELECT DISTINCT taxId
        FROM interactors
    ''')

    distinct_taxids = cursor.fetchall()

    return [entry[0] for entry in distinct_taxids]

def get_interactors_per_taxid(distinct_taxids, cursor):
    ints_per_tax = []
    for id in distinct_taxids:
        cursor.execute('''
            SELECT entrez
            FROM interactors
            WHERE taxId = ?
        ''', (id,))
        interactors = [entry[0] for entry in cursor.fetchall()]
        ints_per_tax.append((id, interactors))
    return ints_per_tax

def get_interactors_per_interaction(cursor):
    ints_per_action = []
    cursor.execute('''
        SELECT id
        FROM interactions
    ''')
    interactions = [entry[0] for entry in cursor.fetchall()]
    for i in interactions:
        cursor.execute('''
            SELECT interactorA, interactorB
            FROM interactions
            WHERE id = ?
        ''', (i,))
        interactors_q = cursor.fetchall()
        interactors = [actor for actor in interactors_q[0]]
        ints_per_action.append((i, interactors))
    return ints_per_action

def interactions_with_taxid(ints_per_tax, ints_per_action):
    interactions_labelled_tax = []
    for reaction in ints_per_action:
        for tax in ints_per_tax:
            if set(reaction[1]).issubset(set(tax[1])):
                interactions_labelled_tax.append((reaction[0], reaction[1], tax[0]))
    return interactions_labelled_tax

def tax_dict(tax_ids, ints_with_tax):
    tax_dict = {}
    for id in tax_ids:
        species_interactome = [(trip[0], trip[1]) for trip in ints_with_tax if trip[2] == id]
        tax_dict[id] = species_interactome
    return tax_dict

if __name__ == '__main__':
    filename = sys.argv[1]
    source = sys.argv[2]

    dbs = sqlite3.connect(filename)
    cursor = dbs.cursor()

    distinct_taxids = get_all_taxids(cursor)
    interactors_per_taxid = get_interactors_per_taxid(distinct_taxids, cursor)
    interactors_per_interaction = get_interactors_per_interaction(cursor)
    ints_with_tax = interactions_with_taxid(interactors_per_taxid, interactors_per_interaction)
    interactomes = tax_dict(distinct_taxids, ints_with_tax)
    print('DONE')
