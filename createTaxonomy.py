#------------------------------create taxonomy
# prefix tree ->
#     nodes created and connected based on each textual pattern (synset) and it's support (each support item is a node)

from derivedClasses import *

def createGraphAndRoot():
    g = graph(directed=True)
    g.add_vertex()
    g.vs[0]["occurrencesSum"] = 0
    g.vs[0]["label"] = "ROOT"
    return g, 0

def quotes(string):
    return "\"" + string + "\""

def getAllItems(c):
    items = []
    for row in c:
        for item in row:
            items.append(item)
    return items

def getRows(c):
    rows = []
    for row in c:
        rows.append(row)
    return rows

def getSupportItemsOfTP(c, textualPattern, sortHighest=True, TPOccurrencePair=False):
    if TPOccurrencePair:
        c.execute(""" SELECT DISTINCT occurrences, support_col FROM patterns NATURAL JOIN support WHERE pattern_type="%s" ORDER BY occurrences DESC """ % (textualPattern))
    else:
        c.execute(""" SELECT DISTINCT support_col FROM patterns NATURAL JOIN support WHERE pattern_type="%s" ORDER BY occurrences DESC """ % (textualPattern))
    supportItems = getRows(c)
    return supportItems

def getOccurrences(supportItem):
    conn = sqlite3.connect("taxonomyRelations.db")
    c = conn.cursor(cursor)
    #print("supportItem:  " + str(supportItem))
    #print(type(supportItem))
    try:
        c.execute(""" SELECT occurrences FROM support WHERE support_col=%s """ % (quotes(supportItem)))
    except:
        #import pdb ; pdb.set_trace()
        c.execute(""" SELECT occurrences FROM support WHERE support_col=%s """ % (quotes(supportItem)))
    for row in c:
        for item in row:
            return int(item)
    return "ERROR"

def getVertexID(vertex):
    return int(re.split(r',+', vertex.__str__())[1])

def includeWSOrCreateVertex(g, vertexID, supportItem, wordSense):
    #look at the children to see if its appropriate to include TP or if it is not appropriate create a new child
    #print("Current vertexID where the children will be looked at: " + str(vertexID))
    #print("Number of children: " + str(len(g.vs[vertexID].successors())))
    #print(g.vs[vertexID].successors())
    #print("before: " + str(g))
    for successor in g.vs[vertexID].successors():
        if successor["supportItem"] == supportItem:
            wordSenseList = successor["wordSenseList"]
            if wordSenseList.count(wordSense) != 0:
                print("ERROR in includeWSOrCreateVertex")
                return None
            else:
                successor["wordSenseList"]  += [wordSense]
                successor["label"]  += [wordSense]
                #print("Added " + str(wordSense) + " to " + str(successor) + " which is ID " + str(getVertexID(successor)))
                #print("after: " + str(g))
                #print("")
                return getVertexID(successor)
    #couldn't find a child that's got the same supportItem
    newVertexID = len(g.vs)
    g.add_vertex()
    g.add_edges([(vertexID, newVertexID)])
    g.vs[newVertexID]["supportItem"] = supportItem
    g.vs[newVertexID]["occurrencesSum"] = g.vs[vertexID]["occurrencesSum"] + getOccurrences(supportItem)
    g.vs[newVertexID]["wordSenseList"] = [wordSense]
    g.vs[newVertexID]["label"] = [supportItem[:5], wordSense]
    #print("newVertexID: " + str(newVertexID))
    #print(g.vs[newVertexID])
    #print("after: " + str(g))
    #print("")
    return newVertexID

def getWordSenses(c):
    c.execute(""" SELECT id_col FROM wordSenses  """)
    return getAllItems(c)

def getTextualPatternsOfWordSense(c, wordSense):
    c.execute(""" SELECT DISTINCT pattern_type FROM patterns WHERE wordSense_col=%s """ % (wordSense))
    return getAllItems(c)

def insertionSort(A):
    ALength = len(A)
    for j in range(1, ALength):
        key = A[j]
        i = j - 1
        while ((i >= 0) and (A[i][0] > key[0])):
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = key

def getSupportItemsOfWS(c, wordSense, sortHighest=True):
    textualPatterns = getTextualPatternsOfWordSense(c, wordSense)
    supportItems = []
    for textualPattern in textualPatterns:
        tPSupportItems= getSupportItemsOfTP(c, textualPattern, TPOccurrencePair=True)
        supportItems += tPSupportItems
    supportItems = list(set(supportItems))
    insertionSort(supportItems)
    supportItems.reverse()
    supportItems = map(lambda x: x [1], supportItems)
    return supportItems

def createPrefixTree(c):
    graph, RootVertexID = createGraphAndRoot()
    wordSenseVertexIDs = [] #tuple of textualPattern and Ending VertexID (last support item)
    for wordSense in getWordSenses(c):
        vertexID = RootVertexID
        for supportItem in getSupportItemsOfWS(c, wordSense):
            vertexID = includeWSOrCreateVertex(graph, vertexID, supportItem, wordSense)
        wordSenseVertexIDs.append((wordSense, vertexID))
    return graph, wordSenseVertexIDs

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

def getOtherWSsFirstOccurrence(g, wordSense, vertexID, pastWSsPresence):
    otherWSsPresent = g.vs[vertexID]["wordSenseList"][:]
    otherWSsPresent.remove(wordSense)
    for pastWSPresence in pastWSsPresence:
        otherWSsPresent.remove(pastWSPresence)
    pastWSsPresence += otherWSsPresent
    return otherWSsPresent, pastWSsPresence

def createDictOfCardinalities(g, wordSenseVertexIDs):
    dictOfCardinalities = dict()
    for wordSenseVertexID in wordSenseVertexIDs:
        wordSense = wordSenseVertexID[0]
        baseVertexID = wordSenseVertexID[1]
        dictOfCardinalities[wordSense] = g.vs[baseVertexID]["occurrencesSum"] # |B|
        pastWSsPresence = []
        for vertexID in verticesGoingToRoot(g, baseVertexID):
            otherWSsPresent, pastWSsPresence = getOtherWSsFirstOccurrence(g, wordSense, vertexID, pastWSsPresence)
            if otherWSsPresent:
                #print("otherWSsPresent: " + str(otherWSsPresent))
                #calculate |S intersect B| / |S| .    |S intersect B|  is the occurrencesSum at the point of first occurrence of S.  |S| remains to be discovered,
                #so to make that calculation, |B| and |S intersect B| have to be stored in a dictionary for quick lookup.
                #we are storing intersects as dictOfCardinalities[(wordSenseS,"intersect", wordSenseB)] = 23 and single cardinalities as dictOfCardinalities[wordSenseS] = 30
                for otherWS in otherWSsPresent:
                    dictOfCardinalities[(otherWS, "intersect", wordSense)] = g.vs[vertexID]["occurrencesSum"] # |S intersect B|
    #print(dictOfCardinalities)
    return dictOfCardinalities

def firstTupleValue(x):
    y = []
    for i in x:
        y.append(i[0])
    return y

def subsumptionEval(key, dictOfCardinalities):
    ISintersectBI = dictOfCardinalities[key]
    IBI = dictOfCardinalities[key[2]]
    ISI = dictOfCardinalities[key[0]]
    if IBI >= ISI:
        return float(ISintersectBI) / float(ISI)
    else:
        return 0

def createSubsumptionGraph(g, dictOfCardinalities, wordSenseVertexIDs):
    g = graph(directed=True) #delete existing g (prefix tree) to save memory
    wordSensesNames = firstTupleValue(wordSenseVertexIDs)
    g.add_vertices(len(wordSensesNames))
    g.vs["label"] = wordSensesNames
    #create edges between textualPattern Vertices based on subsumption evaluator
    for key in dictOfCardinalities.keys():
        if type(key) == tuple: #key is of the form (otherWS, "intersect", wordSense)
            if subsumptionEval(key, dictOfCardinalities):
                firstVertex = getVertexID(g.vs.select(lambda vertex: vertex['label'] == key[2])[0])
                secondVertex = getVertexID(g.vs.select(lambda vertex: vertex['label'] == key[0])[0])
                print("Subsumption detected.  Key is " + str(key))
                print("first vertex:\t\t" + str(firstVertex))
                print("connected to vertex:\t" + str(secondVertex))
                g.add_edges([(firstVertex, secondVertex)])
    return g

def feedbackArcSetRemoval(g):
    g.delete_edges(g.feedback_arc_set())
    return g

def genVisualStyle(g):
    visual_style = {}
    visual_style["vertex_size"] = 12
    visual_style["vertex_label_size"] = 8
    visual_style["vertex_shape"] = "hidden"
    visual_style["vertex_label"] = g.vs["label"]
    visual_style["edge_color"] = "red"
    visual_style["edge_arrow_size"] = .5
    visual_style["edge_arrow_width"] = .5
    visual_style["layout"] = g.layout("rt_circular")
    visual_style["bbox"] = (1100, 650)
    visual_style["margin"] = 20
    return visual_style

def run():
    print("creating taxonomy...")
    conn = sqlite3.connect('taxonomyRelations.db')
    c = conn.cursor(cursor)
    c.execute("pragma foreign_keys = ON")
    ########################################
    g, wordSenseVertexIDs = createPrefixTree(c)
    print("prefix tree has " + str(len(g.vs)) + " nodes")
    dictOfCardinalities = createDictOfCardinalities(g, wordSenseVertexIDs)
    g = createSubsumptionGraph(g, dictOfCardinalities, wordSenseVertexIDs)
    print("subsumption graph has " + str(len(g.vs)) + " nodes")
    g = feedbackArcSetRemoval(g)
    print("taxonomy has " + str(len(g.vs)) + " nodes")
    print('-------------------------------------------------------')
    print(g)
    print('-------------------------------------------------------')
    igraph.plot(g, **genVisualStyle(g))
    ########################################
    #attempt to do the application
    dictVerbsToSupportItems = c.getDictVerbsToSupportItems()

    ########################################
    conn.commit()
    c.close()


def main():
    pass

if __name__ == "__main__":
    pass
