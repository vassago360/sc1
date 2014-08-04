from derivedClasses import *
import extractRelations

def getPairs(listOfItems):
    listOfPairs = []
    for i in range(len(listOfItems)):
        item1 = listOfItems[i]
        for item2 in listOfItems[i+1:]:
            listOfPairs.append([item1, item2])
    return listOfPairs

def removeQuotesFrontOrBack(l):
    for index, val in enumerate(l):
        if val:
            if val[0] == '"':
                val = val[1:]
            if val[-1:] == '"':
                val = val[:-1]
            l[index] = val
    return l

def removeBlanksFront(s):
    startIndex = 0
    for index, val in enumerate(s):
        if val == " ":
            startIndex = index+1
        else:
            return s[startIndex:]

def removeDuplicateResultEntries(fileName):
    results = open(fileName, "r+")
    newUniqueResults = []
    for result in results:
        resultPred, resultArgs, resultProb = getResultsTokens(result)
        foundMatch = False
        for newUniqueResult in newUniqueResults:
            uPred, uArgs, uProb = getResultsTokens(newUniqueResult)
            if uArgs == resultArgs:
                foundMatch = True
        if not foundMatch:
            newUniqueResults.append(result)
    ###########
    results.close()
    results = open(fileName, "w+")
    for line in newUniqueResults:
        results.write(line)
    results.close()

def getResultsTokens(line):
    #go from sameWordSense(tpX, tpY) probabilityValue to ["sameWordSense", [tpX, tpY], probabilityValue]
    predicate = re.split(r'\(', line)[0]
    predicate = removeBlanksFront(predicate)
    args = line[line.find("(")+1:line.find(")")]
    args = re.split(r'","', args)
    args = removeQuotesFrontOrBack(args)
    prob = re.split(r' ', line)[-1:]
    prob = float(prob[0])
    return predicate, args, prob

def separateTPandSI(tPSI):
    tP = re.split(r"###", tPSI)[0]
    sI = re.split(r"###", tPSI)[1]
    return tP, sI

def getZDifference(l): #assumes l is already sorted
    #return the z score difference between the two highest values of the list
    if (len(l) > 1) and (list(set(l)) > 1):
        firstZScore = (l[-2:-1][0] - numpy.mean(l)) / numpy.std(l)
        secondZScore = (l[-1:][0] - numpy.mean(l)) / numpy.std(l)
        return secondZScore - firstZScore
    else:
        return 0.0

def createunivMLN():
    f = open("univ.mln", "w+")
    f.write("""
//predicate declarations
featUNNORMALIZEDVERB(textualPatternSupportItemOccurrence, value_featUNNORMALIZEDVERB!)
featCONJCOUNT(textualPatternSupportItemOccurrence, value_featCONJCOUNT!)
featDEPENSUBARG1(textualPatternSupportItemOccurrence, value_featDEPENSUBARG1!)
featDEPENSUBARG2(textualPatternSupportItemOccurrence, value_featDEPENSUBARG2!)
featDEPENSUBARG3(textualPatternSupportItemOccurrence, value_featDEPENSUBARG3!)
featDEPENHEADARG1(textualPatternSupportItemOccurrence, value_featDEPENHEADARG1!)
featDEPENHEADARG2(textualPatternSupportItemOccurrence, value_featDEPENHEADARG2!)
featDEPENHEADARG3(textualPatternSupportItemOccurrence, value_featDEPENHEADARG3!)
featNEARG1(textualPatternSupportItemOccurrence, value_featNEARG1!)
featNEARG2(textualPatternSupportItemOccurrence, value_featNEARG2!)
featNEARG3(textualPatternSupportItemOccurrence, value_featNEARG3!)
wordSense(textualPatternSupportItemOccurrence, value_wordSense!)

//formulas
wordSense(tPSIO, +v_ws) ^ featUNNORMALIZEDVERB(tPSIO, +v_f1)
wordSense(tPSIO, +v_ws) ^ featCONJCOUNT(tPSIO, +v_f2)
wordSense(tPSIO, +v_ws) ^ featDEPENSUBARG1(tPSIO, +v_f3)
wordSense(tPSIO, +v_ws) ^ featDEPENSUBARG2(tPSIO, +v_f4)
wordSense(tPSIO, +v_ws) ^ featDEPENSUBARG3(tPSIO, +v_f5)
wordSense(tPSIO, +v_ws) ^ featDEPENHEADARG1(tPSIO, +v_f6)
wordSense(tPSIO, +v_ws) ^ featDEPENHEADARG2(tPSIO, +v_f7)
wordSense(tPSIO, +v_ws) ^ featDEPENHEADARG3(tPSIO, +v_f8)
wordSense(tPSIO, +v_ws) ^ featNEARG1(tPSIO, +v_f9)
wordSense(tPSIO, +v_ws) ^ featNEARG2(tPSIO, +v_f10)
wordSense(tPSIO, +v_ws) ^ featNEARG3(tPSIO, +v_f11)
""")
    f.close()

def getFeature(feature, tPSF):
    for featureValue in tPSF:
        if feature in featureValue:
            return featureValue
    return None

def biasedWordSense(inputTP, wordSense, c1, c2, condition):
    if condition == "zuegma":
        tPListsWithSameVerb = c2.getTPsWithSameVerbButNothingElseAsWhatsInTheOtherDB(c1, includeWordSense=True, otherCHasWordSenses=False)
        for tPListWithSameVerb in tPListsWithSameVerb: #ex. [ws1, tp1]
            wS = tPListWithSameVerb[0]
            tP = tPListWithSameVerb[1]
            if (str(wordSense) == str(wS)) and (c1.sameVerb(inputTP, tP, identicalOk=False)):
                return True
    if condition == "reduction":
        tPListsWithSameTP = c2.getTPsWithSameTPButNothingElse(c1, includeWordSense=True, otherCHasWordSenses=False)
        for tPListWithSameTP in tPListsWithSameTP: #ex. [ws1, tp1]
            wS = tPListWithSameTP[0]
            tP = tPListWithSameTP[1]
            if (str(wordSense) == str(wS)) and (inputTP == tP):
                return True

def reduceTPsAWs(tPLists, maxTPs, maxWSs):
    #ex. tPLists = [ [ws1, tp1], [ws1, tp2], [ws2, t6], [ws2, t7] ... ]
    #ex. maxTPs = 5
    reducedLists = []
    count = 0
    wS = None
    wsCount = 0
    for tPPair in tPLists:
        if wS == None:
            wS = tPPair[0]
            wsCount += 1
        if count < maxTPs:
            reducedLists.append(tPPair)
            count += 1
        if (count >= maxTPs) and (tPPair[0] == wS):
            pass
        if (count >= maxTPs) and (tPPair[0] != wS):
            wS = tPPair[0]
            reducedLists.append(tPPair)
            count = 1
            wsCount += 1
            if wsCount >= maxWSs:
                return reducedLists
    return reducedLists

def createunivTestAndGetTestQuery(c1, c2, wordSenses):
    testQuery = r""
    f = open("univ-test.db", "w+")
    #for each textual pattern in the input relations, 1) if two TPs have same verb, but nothing else. include zeugma test predicates  2)  if two TPs match, but nothing else, include reduction test predicates
    #for each sameWordSense(tpX, tpY) based on wordSense_col in taxonomyRelations: 1) if two TPs have same verb, but nothing else. include zeugma test predicates  2)  if two TPs match, but nothing else, include reduction test predicates
    #zeugma
    f.write(""" //Zeugma predicates\n """)
    tPListWithSameVerb = c1.getTPsWithSameVerbButNothingElseAsWhatsInTheOtherDB(c2, includeWordSense=False, otherCHasWordSenses=True)  #getting the input--c1 TPs .  c1 wordSenses not included (there are no c1 wordSenses)
    print("tPListWithSameVerb: (" + str(len(tPListWithSameVerb)) + ") " + str(tPListWithSameVerb))
    for tP in tPListWithSameVerb: #ex. tp1
        tPSFList = c1.getListOfSupportAndSentenceFeatures(tP)
        for tPSF in tPSFList:
            if getFeature("featUNNORMALIZEDVERB", tPSF):
                f.write(""" featUNNORMALIZEDVERB("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featUNNORMALIZEDVERB", tPSF) ) )
            if getFeature("featCONJCOUNT", tPSF):
                f.write(""" featCONJCOUNT("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featCONJCOUNT", tPSF) ) )
            if getFeature("featDEPENSUBARG1", tPSF):
                f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENSUBARG1", tPSF) ) )
            if getFeature("featDEPENSUBARG2", tPSF):
                f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENSUBARG2", tPSF) ) )
            if getFeature("featDEPENSUBARG3", tPSF):
                f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENSUBARG3", tPSF) ) )
            if getFeature("featDEPENHEADARG1", tPSF):
                f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENHEADARG1", tPSF) ) )
            if getFeature("featDEPENHEADARG2", tPSF):
                f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENHEADARG2", tPSF) ) )
            if getFeature("featDEPENHEADARG3", tPSF):
                f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENHEADARG3", tPSF) ) )
            if getFeature("featNEARG1", tPSF):
                f.write(""" featNEARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featNEARG1", tPSF) ) )
            if getFeature("featNEARG2", tPSF):
                f.write(""" featNEARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featNEARG2", tPSF) ) )
            if getFeature("featNEARG3", tPSF):
                f.write(""" featNEARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featNEARG3", tPSF) ) )
            f.write("\n")
            for wordSense in wordSenses:
                testQuery += r""" wordSense(\"%s\",\"%s\") ; """ % (tP + "###" + tPSF[0], "Ws" + str(wordSense))
    #reduction
    f.write(""" //Reduction predicates\n """)
    tPListWithSameTP = c1.getTPsWithSameTPButNothingElse(c2, includeWordSense=False, otherCHasWordSenses=True)
    print("tPListWithSameTP: (" + str(len(tPListWithSameTP)) + ") " + str(tPListWithSameTP))
    for tP in tPListWithSameTP: #ex. tp1
        tPSFList = c1.getListOfSupportAndSentenceFeatures(tP)
        for tPSF in tPSFList:
            if getFeature("featUNNORMALIZEDVERB", tPSF):
                f.write(""" featUNNORMALIZEDVERB("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featUNNORMALIZEDVERB", tPSF) ) )
            if getFeature("featCONJCOUNT", tPSF):
                f.write(""" featCONJCOUNT("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featCONJCOUNT", tPSF) ) )
            if getFeature("featDEPENSUBARG1", tPSF):
                f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENSUBARG1", tPSF) ) )
            if getFeature("featDEPENSUBARG2", tPSF):
                f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENSUBARG2", tPSF) ) )
            if getFeature("featDEPENSUBARG3", tPSF):
                f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENSUBARG3", tPSF) ) )
            if getFeature("featDEPENHEADARG1", tPSF):
                f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENHEADARG1", tPSF) ) )
            if getFeature("featDEPENHEADARG2", tPSF):
                f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENHEADARG2", tPSF) ) )
            if getFeature("featDEPENHEADARG3", tPSF):
                f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featDEPENHEADARG3", tPSF) ) )
            if getFeature("featNEARG1", tPSF):
                f.write(""" featNEARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featNEARG1", tPSF) ) )
            if getFeature("featNEARG2", tPSF):
                f.write(""" featNEARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featNEARG2", tPSF) ) )
            if getFeature("featNEARG3", tPSF):
                f.write(""" featNEARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0], getFeature("featNEARG3", tPSF) ) )
            f.write("\n")
            for wordSense in wordSenses:
                testQuery += r""" wordSense(\"%s\",\"%s\") ; """ % (tP + "###" + tPSF[0], "Ws" + str(wordSense))
    f.close()
    return testQuery

def createunivTrain(c1, c2):
    wordSenses = [] #ex. [1,4,6,7,8,9]
    f = open("univ-train.db", "w+")
    totalTupleCounts = []
    #for each sameWordSense(tpX, tpY) based on wordSense_col in taxonomyRelations: 1) if two TPs have same verb, but nothing else. include zeugma test predicates  2)  if two TPs match, but nothing else, include reduction test predicates
    #zeugma
    f.write(""" //Zeugma predicates\n """)
    tPListsWithSameVerb = c2.getTPsWithSameVerbButNothingElseAsWhatsInTheOtherDB(c1, includeWordSense=True, otherCHasWordSenses=False) #getting the tax-c2 TPs .  c2 wordSenses included
    tPListsWithSameVerb = reduceTPsAWs(tPListsWithSameVerb, 5, 1000)
    if len(tPListsWithSameVerb) > 150:
        print("training: will need to compare input tps to a smaller set of taxonomy wordSenses (too many zeugma situations)..")
        tPListsWithSameVerb = tPListsWithSameVerb[:150]
    incr = 0
    for tPListWithSameVerb in tPListsWithSameVerb: #ex. [ws1, tp1]
        wordSense = tPListWithSameVerb[0]
        wordSenses.append(wordSense)
        tP = tPListWithSameVerb[1]
        tPSFList = c2.getListOfSupportAndSentenceFeatures(tP, wordSense)
        count = 0
        for tPSF in tPSFList:
            incr += 1
            count += 1
            if count <= 2:
                if getFeature("featUNNORMALIZEDVERB", tPSF):
                    f.write(""" featUNNORMALIZEDVERB("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featUNNORMALIZEDVERB", tPSF) ) )
                else:
                    f.write(""" featUNNORMALIZEDVERB("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featUNNORMALIZEDVERB_None" ) )
                if getFeature("featCONJCOUNT", tPSF):
                    f.write(""" featCONJCOUNT("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featCONJCOUNT", tPSF) ) )
                else:
                    f.write(""" featCONJCOUNT("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featCONJCOUNT_None" ) )
                if getFeature("featDEPENSUBARG1", tPSF):
                    f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENSUBARG1", tPSF) ) )
                else:
                    f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENSUBARG1_None" ) )
                if getFeature("featDEPENSUBARG2", tPSF):
                    f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENSUBARG2", tPSF) ) )
                else:
                    f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENSUBARG2_None" ) )
                if getFeature("featDEPENSUBARG3", tPSF):
                    f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENSUBARG3", tPSF) ) )
                else:
                    f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENSUBARG3_None" ) )
                if getFeature("featDEPENHEADARG1", tPSF):
                    f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENHEADARG1", tPSF) ) )
                else:
                    f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENHEADARG1_None" ) )
                if getFeature("featDEPENHEADARG2", tPSF):
                    f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENHEADARG2", tPSF) ) )
                else:
                    f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENHEADARG2_None" ) )
                if getFeature("featDEPENHEADARG3", tPSF):
                    f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENHEADARG3", tPSF) ) )
                else:
                    f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENHEADARG3_None" ) )
                if getFeature("featNEARG1", tPSF):
                    f.write(""" featNEARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featNEARG1", tPSF) ) )
                else:
                    f.write(""" featNEARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featNEARG1_None" ) )
                if getFeature("featNEARG2", tPSF):
                    f.write(""" featNEARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featNEARG2", tPSF) ) )
                else:
                    f.write(""" featNEARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featNEARG2_None" ) )
                if getFeature("featNEARG3", tPSF):
                    f.write(""" featNEARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featNEARG3", tPSF) ) )
                else:
                    f.write(""" featNEARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featNEARG3_None" ) )
                f.write(""" wordSense("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "Ws" + str(wordSense)) )
                f.write("\n")
    totalTupleCounts.append(incr)
    #reduction
    f.write(""" //Reduction predicates\n """)
    tPListsWithSameTP = c2.getTPsWithSameTPButNothingElse(c1, includeWordSense=True, otherCHasWordSenses=False)
    tPListsWithSameTP = reduceTPsAWs(tPListsWithSameTP, 5, 1000)
    if len(tPListsWithSameTP) > 150:
        print("training: will need to compare input tps to a smaller set of taxonomy wordSenses (too many reduction situations)..")
        tPListsWithSameTP = tPListsWithSameTP[:150]
    incr = 0
    for tPListWithSameTP in tPListsWithSameTP: #ex. [ws1, tp1]
        wordSense = tPListWithSameTP[0]
        wordSenses.append(wordSense)
        tP = tPListWithSameTP[1]
        tPSFList = c2.getListOfSupportAndSentenceFeatures(tP, wordSense)
        count = 0
        for tPSF in tPSFList:
            incr += 1
            count += 1
            if count <= 2:
                if getFeature("featUNNORMALIZEDVERB", tPSF):
                    f.write(""" featUNNORMALIZEDVERB("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featUNNORMALIZEDVERB", tPSF) ) )
                else:
                    f.write(""" featUNNORMALIZEDVERB("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featUNNORMALIZEDVERB_None" ) )
                if getFeature("featCONJCOUNT", tPSF):
                    f.write(""" featCONJCOUNT("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featCONJCOUNT", tPSF) ) )
                else:
                    f.write(""" featCONJCOUNT("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featCONJCOUNT_None" ) )
                if getFeature("featDEPENSUBARG1", tPSF):
                    f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENSUBARG1", tPSF) ) )
                else:
                    f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENSUBARG1_None" ) )
                if getFeature("featDEPENSUBARG2", tPSF):
                    f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENSUBARG2", tPSF) ) )
                else:
                    f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENSUBARG2_None" ) )
                if getFeature("featDEPENSUBARG3", tPSF):
                    f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENSUBARG3", tPSF) ) )
                else:
                    f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENSUBARG3_None" ) )
                if getFeature("featDEPENHEADARG1", tPSF):
                    f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENHEADARG1", tPSF) ) )
                else:
                    f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENHEADARG1_None" ) )
                if getFeature("featDEPENHEADARG2", tPSF):
                    f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENHEADARG2", tPSF) ) )
                else:
                    f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENHEADARG2_None" ) )
                if getFeature("featDEPENHEADARG3", tPSF):
                    f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featDEPENHEADARG3", tPSF) ) )
                else:
                    f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featDEPENHEADARG3_None" ) )
                if getFeature("featNEARG1", tPSF):
                    f.write(""" featNEARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featNEARG1", tPSF) ) )
                else:
                    f.write(""" featNEARG1("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featNEARG1_None" ) )
                if getFeature("featNEARG2", tPSF):
                    f.write(""" featNEARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featNEARG2", tPSF) ) )
                else:
                    f.write(""" featNEARG2("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featNEARG2_None" ) )
                if getFeature("featNEARG3", tPSF):
                    f.write(""" featNEARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), getFeature("featNEARG3", tPSF) ) )
                else:
                    f.write(""" featNEARG3("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "featNEARG3_None" ) )
                f.write(""" wordSense("%s", "%s")\n """ % (tP + "###" + tPSF[0] + str(incr), "Ws" + str(wordSense)) )
                f.write("\n")
    totalTupleCounts.append(incr)
    print("training tuple counts: zeugma tuples: " + str(totalTupleCounts[0]) + " reduction tuples: " + str(totalTupleCounts[1]))
    f.close()
    return list(set(wordSenses))

def findAndAddUncomparableWordSenses(c1,c2, c3):
    #import pdb ; pdb.set_trace()
    #find tPs in c1 that are not going to go through reduction or zeugma testing
    tPsToAddSameTPAndSI = c1.getTPsWithSameTPAndSameSupportItem(c2)
    tPsToAddNoMatch = c1.getTPsWithNoMatch(c2)
    print("tPsToAddSameTPAndSI: (" + str(len(tPsToAddSameTPAndSI)) + ") " + str(tPsToAddSameTPAndSI))
    print("tPsToAddNoMatch: (" + str(len(tPsToAddNoMatch)) + ") " + str(tPsToAddNoMatch))
    #add input textualpatterns that match up exactly
    for tPToAdd in tPsToAddSameTPAndSI:
        wS = c2.getWordSense(tPToAdd)
        c1.updateRowsBasedOnUIwWSAndCopyOver(wS, tPToAdd, None, c3)
        c1.deleteRowsBasedOnUI(tPToAdd)
    #add input textualpatterns that haven't been seen before
    for tPToAdd in tPsToAddNoMatch:
        wS = c1.createNewWordSense(c3.getNextAvailableWordSenseMin1000000())
        c1.updateRowsBasedOnUIwWSAndCopyOver(wS, tPToAdd, None, c3) #identical TPs with different support will be assigned same wordSense :s
        c1.deleteRowsBasedOnUI(tPToAdd)
    return tPsToAddSameTPAndSI

def trainMLN1(c1, c2):
    print("training MLN1...")
    createunivMLN()
    wordSenses = createunivTrain(c1, c2)
    if len(wordSenses) == 1:
        subprocess.call([r""" alchemy/bin/learnwts -i univ.mln -o univ-out.mln -t univ-train.db -g -gNoEqualPredWt 1 -ne wordSense -maxSteps 20 -gMaxIter 100 > trainMLN1Output.txt """], shell=True)
    else:
        subprocess.call([r""" alchemy/bin/learnwts -i univ.mln -o univ-out.mln -t univ-train.db -lazy 1 -lazyNoApprox 1 -ne wordSense -maxSteps 20 -gMaxIter 100 > trainMLN1Output.txt """], shell=True)
        #subprocess.call([r""" alchemy/bin/learnwts -i univ.mln -o univ-out.mln -t univ-train.db -d -ne wordSense -maxSteps 20 -dNumIter 20 > trainMLN1Output.txt """], shell=True)
    return wordSenses

def findLastIndex(s, subString):
    index = -1
    while(True):
        if s.find(subString, index+1) == -1:
            return index
        else:
            index = s.find(subString, index+1)

def findFirstIndex(s, subString):
    return s.find(subString, 0)

def separateQueryIntoParts(query, numberOfQueryParts):
    queryIntoParts = []
    lengthOfEachQueryPart = int(len(query)/numberOfQueryParts)
    for i in range(numberOfQueryParts):
        queryPart = query[lengthOfEachQueryPart*i:lengthOfEachQueryPart*(i+1)]
        if (findFirstIndex(queryPart, ";") != -1) and (findLastIndex(queryPart, ";") != -1):
            queryPart = queryPart[findFirstIndex(queryPart, ";")+1:findLastIndex(queryPart, ";")+1]
        queryIntoParts.append(queryPart)
    return queryIntoParts

def testMLN1(c1, c2, wordSenses, testQueryPartToDo):
    print("testing MLN1...")
    testQuery = createunivTestAndGetTestQuery(c1, c2, wordSenses)
    if testQuery:
        print("testQuery total: (" + str(len(testQuery)) + ") ")
        if len(testQuery) > 125000:
            numberOfQueryParts = int(len(testQuery)/110000.0)+1
            testQuery = separateQueryIntoParts(testQuery, numberOfQueryParts)[testQueryPartToDo]
            print("testQuery to be evaluated: (" + str(len(testQuery)) + ") " + " part " + str(testQueryPartToDo) + "of " + str(numberOfQueryParts-1) + " (max)")
            subprocess.call(r""" alchemy/bin/infer -i univ-out.mln -e univ-test.db -r univ.results -q " """ + testQuery + r""" " -lazy 1 -lazyNoApprox 1 > testMLN1Output.txt """, shell=True)
            if numberOfQueryParts == testQueryPartToDo+1:
                testQueryPartToDo = -1
                return testQueryPartToDo
            else:
                testQueryPartToDo += 1
                return testQueryPartToDo
        else:
            subprocess.call(r""" alchemy/bin/infer -i univ-out.mln -e univ-test.db -r univ.results -q " """ + testQuery + r""" " -lazy 1 -lazyNoApprox 1 > testMLN1Output.txt """, shell=True)
            testQueryPartToDo = -1
            return testQueryPartToDo
        #subprocess.call(r""" alchemy/bin/infer -i univ-out.mln -e univ-test.db -r univ.results -q " """ + testQuery + r""" " -maxSteps 10 -mwsMaxSteps 100 """, shell=True)
    else:
        print("no testing will be done, because there is no query")
        open("univ.results", "w+").close()
        testQueryPartToDo = -1
        return testQueryPartToDo

def addHighProbableWordSenses(c1, c2, c3):
    #look at univ.results, get high probable belongsIn() or sameWordSense(), get and look at the tokens and add them to taxonomyRelations db
    #for every relation, if it is a high probability do the following:
    #if sameWordSense:  add run mergeWordSense(tp1, tp2) on tpX or tpY.
    #if belongsIn add tpX, siX, and associated features to taxonomy
    print("add high probable wordSenses...")
    removeDuplicateResultEntries("univ.results")
    results = open("univ.results", "r+")
    #populate the tpSI to probs dictionary
    dictTPSItoProbs = dict()
    dictTPSIProbsToWSs = dict()
    for result in results:
        predicate, args, prob = getResultsTokens(result)
        tpSI = args[0]
        wordSense = args[1][2:]
        dictTPSItoProbs[tpSI] = []
        dictTPSIProbsToWSs[(tpSI,prob)] = wordSense
    results.seek(0)
    for result in results:
        predicate, args, prob = getResultsTokens(result)
        tpSI = args[0]
        dictTPSItoProbs[tpSI].append(prob)
        dictTPSItoProbs[tpSI].sort()
    #get difference in z scores between the two highest probabilities
    tPsToDelete = []
    tPsThatChangeC2 = []
    for key in dictTPSItoProbs.keys():
        l = dictTPSItoProbs[key]
        zDiff = getZDifference(l)
        #additional prep
        tpSI = key
        prob = l[-1:][0]
        wordSense = dictTPSIProbsToWSs[(tpSI,prob)]
        inputTP, inputSI = separateTPandSI(tpSI)
        tPsWithSameVerb = c2.getTPsWithSameVerbButNothingElseOfATP(inputTP)
        tPsWithSameTP = c2.getTPsWithSameTPButNothingElseOfATP(c1, inputTP)
        #there are situations when a tp has both zuegma and reduction (multiple tps in taxonomy db that satify both conditions).  First do reduction, then zeugma, then if strictly reduction remove it, otherwise add a new wordsense
        if zDiff >= 0.0:
            if biasedWordSense(inputTP, wordSense, c1, c2, "reduction"):
                print("high prob reduction situation: " + "inputTP added: " + str(inputTP) + " wordSense: " + str(wordSense) + " zDiff: " + str(zDiff) + " comparable probabilities: " + str(l[-3:]))
                c1.updateRowsBasedOnUIwWSAndCopyOver(wordSense, inputTP, inputSI, c3)
                tPsToDelete.append(inputTP)
                tPsThatChangeC2.append(inputTP)
            elif biasedWordSense(inputTP, wordSense, c1, c2, "zuegma"):
                print("high prob zeugma situation: " + "inputTP added: " + str(inputTP) + " wordSense: " + str(wordSense) + " zDiff: " + str(zDiff) + " comparable probabilities: " + str(l[-3:]))
                c1.updateRowsBasedOnUIwWSAndCopyOver(wordSense, inputTP, inputSI, c3)
                tPsToDelete.append(inputTP)
                tPsThatChangeC2.append(inputTP)
            elif tPsWithSameTP and not tPsWithSameVerb:
                #import pdb ; pdb.set_trace()
                print("low prob reduction situation (wrong bias): extracted textualPattern isn't accurate, therefore it will not be added to taxonomy.  " + "inputTP added: " + str(inputTP) + " wordSense: " + str(wordSense) + " zDiff: " + str(zDiff) + " comparable probabilities: " + str(l[-3:]))
                tPsToDelete.append(inputTP)
            elif tPsWithSameVerb:
                #import pdb ; pdb.set_trace()
                wordSense = c1.createNewWordSense(c3.getNextAvailableWordSenseMin1000000())
                print("low prob zeugma situation (wrong bias):  " + "inputTP added: " + str(inputTP) + " new wordSense: " + str(wordSense)  + " zDiff: " + str(zDiff) + " comparable probabilities: " + str(l[-3:]))
                c1.updateRowsBasedOnUIwWSAndCopyOver(wordSense, inputTP, inputSI, c3)
                tPsToDelete.append(inputTP)
                tPsThatChangeC2.append(inputTP)
        else:
            if tPsWithSameTP and not tPsWithSameVerb:
                #import pdb ; pdb.set_trace()
                print("low prob reduction situation (low zDiff: " + str(zDiff) + "): extracted textualPattern isn't accurate, therefore it will not be added to taxonomy.  " + "inputTP added: " + str(inputTP) + " wordSense: " + str(wordSense) + " zDiff: " + str(zDiff) + " comparable probabilities: " + str(l[-3:]))
                tPsToDelete.append(inputTP)
            elif tPsWithSameVerb:
                wordSense = c1.createNewWordSense(c3.getNextAvailableWordSenseMin1000000())
                print("low prob zeugma situation, (low zDiff: " + str(zDiff) + "): " + "inputTP added: " + str(inputTP) + " new wordSense: " + str(wordSense)  + " zDiff: " + str(zDiff) + " comparable probabilities: " + str(l[-3:]))
                c1.updateRowsBasedOnUIwWSAndCopyOver(wordSense, inputTP, inputSI, c3)
                tPsToDelete.append(inputTP)
                tPsThatChangeC2.append(inputTP)
    for tp in tPsToDelete:
        c1.deleteRowsBasedOnUI(tp)
    return tPsThatChangeC2

def run():
    #prep
    conn1 = sqlite3.connect('inputRelations.db')
    c1 = conn1.cursor(cursor)
    c1.execute("pragma foreign_keys = ON")
    conn2 = sqlite3.connect('taxonomyRelations.db')
    c2 = conn2.cursor(cursor)
    c2.execute("pragma foreign_keys = ON")
    conn3, c3 = extractRelations.createDB("transportedTR.db")
    ####################################
    #do stuff
    #print("-----Input Beforehand-----")
    #c1.printDB()
    #print("-----Database Beforehand-----")
    #c2.printDB()
    tPsThatChangeC2 = []
    tPsThatChangeC2 += findAndAddUncomparableWordSenses(c1,c2, c3)
    wordSenses = trainMLN1(c1, c2)
    conn1.commit()
    c1.close()
    #test and add high probable word senses
    testQueryPartToDo = 0
    while testQueryPartToDo != -1:
        conn1 = sqlite3.connect('inputRelations.db')
        c1 = conn1.cursor(cursor)
        testQueryPartToDo = testMLN1(c1, c2, wordSenses, testQueryPartToDo)
        tPsThatChangeC2 += addHighProbableWordSenses(c1, c2, c3)
        c1.close()
    conn1 = sqlite3.connect('inputRelations.db')
    c1 = conn1.cursor(cursor)
    c1.copyOverURLsProcessed(c3)
    #display taxonomy.db and close
    #print("-----Input Afterwards-----")
    #c1.printDB()
    #print("-----Database Afterwards-----")
    #c2.printDB()
    print("")
    ####################################
    conn1.commit()
    c1.close()
    conn2.commit()
    c2.close()
    conn3.commit()
    c3.close()
    return tPsThatChangeC2

def main():
    pass

if __name__ == '__main__':
    main()