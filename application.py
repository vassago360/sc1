from derivedClasses import *

def createGraphAndRoot():
    g = graph(directed=True)
    g.add_vertex()
    g.vs[0]["occurrencesSum"] = 0
    g.vs[0]["label"] = "ROOT"
    return g, 0

def getNamedEntities(supportItem):
    namedEntities = re.split(r"_", supportItem)
    if namedEntities.count(''):
        namedEntities.remove('')
    return namedEntities

def getVerbEveryOtherSupport(namedEntity, verb, supportItem):
    namedEntities = getNamedEntities(supportItem)
    namedEntities.remove(namedEntity)
    return verb + "_" + str(namedEntities)

def getNecessaryDicts(c):
    #dicts i want to create
    dictNEtoVerbEveryOtherSupport = dict()
    dictVerbEveryOtherSupporttoOccurrences = dict()
    #fill in the dicts
    dictVerbsToSupportItems = c.getDictVerbsToSupportItems()
    for verb in dictVerbsToSupportItems.keys():
        supportItems = dictVerbsToSupportItems[verb]
        for supportItem in supportItems:
            namedEntities = getNamedEntities(supportItem)
            for namedEntity in namedEntities:
                verbEveryOtherSupport = getVerbEveryOtherSupport(namedEntity, verb, supportItem)
                if namedEntity in dictNEtoVerbEveryOtherSupport.keys():
                    dictNEtoVerbEveryOtherSupport[namedEntity].append(verbEveryOtherSupport)
                else:
                    dictNEtoVerbEveryOtherSupport[namedEntity] = [verbEveryOtherSupport]
                if verbEveryOtherSupport in dictVerbEveryOtherSupporttoOccurrences.keys():
                    dictVerbEveryOtherSupporttoOccurrences[verbEveryOtherSupport] += 1
                else:
                    dictVerbEveryOtherSupporttoOccurrences[verbEveryOtherSupport] = 1
    return dictNEtoVerbEveryOtherSupport, dictVerbEveryOtherSupporttoOccurrences

def getVertexID(vertex):
    return int(re.split(r',+', vertex.__str__())[1])

def includeNEOrCreateVertex(g, vertexID, verbEveryOtherSupport, nE, dictVerbEveryOtherSupporttoOccurrences):
    #look at the children to see if its appropriate to include TP or if it is not appropriate create a new child
    #print("Current vertexID where the children will be looked at: " + str(vertexID))
    #print("Number of children: " + str(len(g.vs[vertexID].successors())))
    #print(g.vs[vertexID].successors())
    #print("before: " + str(g))
    for successor in g.vs[vertexID].successors():
        if successor["verbEveryOtherSupport"] == verbEveryOtherSupport:
            namedEntityList = successor["namedEntityList"]
            if namedEntityList.count(nE) != 0:
                print("ERROR in appIncludeWSOrCreateVertex")
                return None
            else:
                successor["namedEntityList"]  += [nE]
                successor["label"]  += [nE]
                #print("Added " + str(nE) + " to " + str(successor) + " which is ID " + str(getVertexID(successor)))
                #print("after: " + str(g))
                #print("")
                return getVertexID(successor)
    #couldn't find a child that's got the same verbEveryOtherSupport
    newVertexID = len(g.vs)
    g.add_vertex()
    g.add_edges([(vertexID, newVertexID)])
    g.vs[newVertexID]["verbEveryOtherSupport"] = verbEveryOtherSupport
    g.vs[newVertexID]["occurrencesSum"] = g.vs[vertexID]["occurrencesSum"] + dictVerbEveryOtherSupporttoOccurrences[verbEveryOtherSupport]
    g.vs[newVertexID]["namedEntityList"] = [nE]
    g.vs[newVertexID]["label"] = [verbEveryOtherSupport[:5], nE]
    #print("newVertexID: " + str(newVertexID))
    #print(g.vs[newVertexID])
    #print("after: " + str(g))
    #print("")
    return newVertexID

def createPrefixTree(c, dictNEtoVerbEveryOtherSupport, dictVerbEveryOtherSupporttoOccurrences):
    graph, RootVertexID = createGraphAndRoot()
    nEVertexIDs = [] #tuple of textualPattern and Ending VertexID (last support item)
    for nE in dictNEtoVerbEveryOtherSupport.keys():
        vertexID = RootVertexID
        for verbEveryOtherSupport in dictNEtoVerbEveryOtherSupport[nE]:
            vertexID = includeNEOrCreateVertex(graph, vertexID, verbEveryOtherSupport, nE, dictVerbEveryOtherSupporttoOccurrences)
        nEVertexIDs.append((nE, vertexID))
    return graph, nEVertexIDs

def verticesGoingToRoot(g, baseVertexID):
    vectices = [baseVertexID]
    vertexID = baseVertexID
    didNotFindPredecessor = False
    while not didNotFindPredecessor:
        didNotFindPredecessor = True
        if len(g.vs[vertexID].predecessors()) != 0:
            if len(g.vs[vertexID].predecessors()) != 1:
                print("ERROR in verticesGoingToRoot")
            else:
                didNotFindPredecessor = False
                vertexID = getVertexID(g.vs[vertexID].predecessors()[0])
                vectices.append(vertexID)
    vectices.remove(0) #Remove root
    return vectices

def getOtherWSsFirstOccurrence(g, namedEntity, vertexID, pastNEsPresence):
    otherNEsPresent = g.vs[vertexID]["namedEntityList"][:]
    otherNEsPresent.remove(namedEntity)
    for pastNEPresence in pastNEsPresence:
        otherNEsPresent.remove(pastNEPresence)
    pastNEsPresence += otherNEsPresent
    return otherNEsPresent, pastNEsPresence

def createDictOfCardinalities(g, nEVertexIDs):
    dictOfCardinalities = dict()
    for nEVertexID in nEVertexIDs:
        namedEntity = nEVertexID[0]
        baseVertexID = nEVertexID[1]
        dictOfCardinalities[namedEntity] = g.vs[baseVertexID]["occurrencesSum"] # |B|
        pastNEsPresence = []
        for vertexID in verticesGoingToRoot(g, baseVertexID):
            otherNEsPresent, pastNEsPresence = getOtherWSsFirstOccurrence(g, namedEntity, vertexID, pastNEsPresence)
            if otherNEsPresent:
                #print("otherWSsPresent: " + str(otherWSsPresent))
                #calculate |S intersect B| / |S| .    |S intersect B|  is the occurrencesSum at the point of first occurrence of S.  |S| remains to be discovered,
                #so to make that calculation, |B| and |S intersect B| have to be stored in a dictionary for quick lookup.
                #we are storing intersects as dictOfCardinalities[(wordSenseS,"intersect", wordSenseB)] = 23 and single cardinalities as dictOfCardinalities[wordSenseS] = 30
                for otherNE in otherNEsPresent:
                    dictOfCardinalities[(otherNE, "intersect", namedEntity)] = g.vs[vertexID]["occurrencesSum"] # |S intersect B|
    #print(dictOfCardinalities)
    return dictOfCardinalities

def subsumptionEval(key, dictOfCardinalities):
    ISintersectBI = dictOfCardinalities[key]
    IBI = dictOfCardinalities[key[2]]
    ISI = dictOfCardinalities[key[0]]
    if (key[2], "intersect", key[0]) in dictOfCardinalities.keys():
        IBintersectSI = dictOfCardinalities[(key[2], "intersect", key[0])]
        return (float(IBI) * float(ISintersectBI) + float(ISI) * float(IBintersectSI))  / (2.0 * float(IBI) * float(ISI))
    else:
        return 0

def generateListOfSemanticallyEquivalentNEs(dictOfCardinalities):
    for key in dictOfCardinalities.keys():
        if type(key) == tuple: #key is of the form (otherWS, "intersect", wordSense)
            if subsumptionEval(key, dictOfCardinalities):
                print(key[0] + " is equivant to " + key[2])

def run():
    conn = sqlite3.connect('taxonomyRelations.db')
    c = conn.cursor(cursor)
    c.execute("pragma foreign_keys = ON")
    #####
    dictNEtoVerbEveryOtherSupport, dictVerbEveryOtherSupporttoOccurrences = getNecessaryDicts(c)
    g, nEVertexIDs = createPrefixTree(c, dictNEtoVerbEveryOtherSupport, dictVerbEveryOtherSupporttoOccurrences)
    print("prefix tree has " + str(len(g.vs)) + " nodes")
    dictOfCardinalities = createDictOfCardinalities(g, nEVertexIDs)
    generateListOfSemanticallyEquivalentNEs(dictOfCardinalities)

run()



