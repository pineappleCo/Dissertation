import sys

def parse(filename, source):
    #read each line is a string in list of strings
    with open(filename) as f:
        datalines = f.read().splitlines()
    datalines.pop(0) #remove first list item
    print(datalines)
    tabsplit_datalines = [line.split('\t') for line in datalines]
    print(tabsplit_datalines)
    print("HERE IT IS --->>" + str(tabsplit_datalines[0][35]))
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
    pubId = [pub[7:] for pub in tab_split[8].split('|')]
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
    pubId = [pub.split(':')[1] for pub in tab_split[8].split('|')]
    taxA = [pub.split(':')[1].split('(')[0] for pub in tab_split[9].split('|')]
    taxB = [pub.split(':')[1].split('(')[0] for pub in tab_split[10].split('|')]
    interactionType = tab_split[11].split('(')[1][:-1]
    source = "intact"
    interactionId = [id.split(':')[1] for id in tab_split[13].split('|')]
    bioRoleA = tab_split[16].split('(')[1][:-1]
    bioRoleB = tab_split[17].split('(')[1][:-1]
    experimentRoleA = tab_split[18].split('(')[1][:-1]
    experimentRoleB = tab_split[19].split('(')[1][:-1]
    hostOrganism = [tax.split(':')[1].split('(')[0] for tax in tab_split[28].split('|')]
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

#for testing
if __name__ == '__main__':
    filename = sys.argv[1]
    source = sys.argv[2]
    print(parse(filename, source))