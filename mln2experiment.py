from derivedClasses import *
import extractRelations

def separateTPandSI(tPSI):
    tP = re.split(r"###", tPSI)[0]
    sI = re.split(r"###", tPSI)[1]
    return tP, sI

def sentenceIncluded(sentence, all_TP_WS_S_S_Fs):
    for TP_WS_S_S_F in all_TP_WS_S_S_Fs:
        if sentence == TP_WS_S_S_F[2]:
            return True
    return False

def getFeature(feature, TP_WS_S_S_F):
    for featureValue in TP_WS_S_S_F[4:]:
        if feature in featureValue:
            return featureValue
    return None

def getWordSensesThatShareSameVerbAsTPs(c2, addedTPs):
    wSs = []
    for tP in addedTPs:
        wSs += c2.getWordSense(tP, all=True)
        tPsWithSameVerb = c2.getTPsWithSameVerbButNothingElseOfATP(tP)
        for tPWithSameVerb in tPsWithSameVerb:
            wSs += c2.getWordSense(tPWithSameVerb, all=True)
        wSs = list(set(wSs))
    return wSs

def getTuplesForMLN2(c2, wSs):
    all_TP_WS_S_S_Fs = []
    for wS in wSs:
        tPs = c2.getTPsOfAWordSense(wS)
        for tP in tPs:
            TP_WS_S_S_F_List = c2.getListOfTPsAndWSsAndSentencesAndSupportAndFeatures(tP, wS)
            for TP_WS_S_S_F in TP_WS_S_S_F_List:
                sentence = TP_WS_S_S_F[2]
                if not sentenceIncluded(sentence, all_TP_WS_S_S_Fs):
                    all_TP_WS_S_S_Fs.append(TP_WS_S_S_F)
    return all_TP_WS_S_S_Fs

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

def getZDifference(l): #assumes l is already sorted
    #return the z score difference between the two highest values of the list
    if (len(l) > 1) and (len(list(set(l))) > 1):
        firstZScore = (l[-2:-1][0] - numpy.mean(l)) / numpy.std(l)
        secondZScore = (l[-1:][0] - numpy.mean(l)) / numpy.std(l)
        return secondZScore - firstZScore
    else:
        return 0.0

def determineIfWSShouldMerge(wS1, dictOwnerWSResultWStoProbs, allWordSenses):
    #find percents
    numberOfTuples = 0
    sumOfPercentsGoingElsewhere = 0.0
    sumOfPercentsGoingToSelf = 0.0
    for wS2 in allWordSenses:
        try:
            dictOwnerWSResultWStoProbs[(wS1, wS2)]
        except:
            return None #combination of owner to result ws doesn't exist, therefore ignore that possible merge
        listOfPercents = dictOwnerWSResultWStoProbs[(wS1, wS2)]
        numberOfTuples = len(listOfPercents)
        if wS1 == wS2:
            for percent in listOfPercents:
                sumOfPercentsGoingToSelf += percent
        else:
            for percent in listOfPercents:
                sumOfPercentsGoingElsewhere += percent
    try:
        percentageGoingElseWhere = sumOfPercentsGoingElsewhere / (sumOfPercentsGoingElsewhere + sumOfPercentsGoingToSelf)
    except:
        percentageGoingElseWhere = 0.0
    #find out closestWS
    closestWS = [None, 0.0]
    allW2Percents = []
    for wS2 in allWordSenses:
        listOfPercents = dictOwnerWSResultWStoProbs[(wS1, wS2)]
        sumOfPercentsGoingW2 = 0.0
        for percent in listOfPercents:
            sumOfPercentsGoingW2 += percent
        try:
            percentageGoingW2 = sumOfPercentsGoingW2 / sumOfPercentsGoingElsewhere
        except:
            percentageGoingW2 = 0.0
        if wS1 != wS2:
            allW2Percents.append(percentageGoingW2)
            if percentageGoingW2 > closestWS[1]:
                closestWS = [wS2, percentageGoingW2]
    allW2Percents.sort()
    zDiff = getZDifference(allW2Percents)
    if closestWS[0]:
        if (zDiff > 0.0) and (closestWS[1] > 0.00035):
            return closestWS[0]
    return None
    """#evaluate each wS2
    for wS2 in allWordSenses:
        listOfPercents = dictOwnerWSResultWStoProbs[(wS1, wS2)]
        sumOfPercentsGoingW2 = 0.0
        for percent in listOfPercents:
            sumOfPercentsGoingW2 += percent
        try:
            percentageGoingW2 = sumOfPercentsGoingW2 / sumOfPercentsGoingElsewhere
        except:
            percentageGoingW2 = 0.0
        zDiff = getZDifference(allW2Percents)
        print("wS1: " + str(wS1))
        print("numberOfTuples: " + str(numberOfTuples))
        print("wS2: " + str(wS2))
        print("percentageGoingW2: " + str(percentageGoingW2))
        print("percentageGoingElseWhere: " + str(percentageGoingElseWhere))
        print("closestWS: " + str(closestWS))
        print("zDiff: " + str(zDiff))"""

def createunivMLN():
    f = open("univ.mln", "w+")
    f.write("""
//predicate declarations
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
(featCONJCOUNT(tPSIO, +v_f1) ^ featDEPENSUBARG1(tPSIO, +v_f2)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featDEPENSUBARG2(tPSIO, +v_f3)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featDEPENSUBARG3(tPSIO, +v_f4)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featDEPENHEADARG1(tPSIO, +v_f5)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featDEPENHEADARG2(tPSIO, +v_f6)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featDEPENHEADARG3(tPSIO, +v_f7)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featNEARG1(tPSIO, +v_f8)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featNEARG2(tPSIO, +v_f9)) => wordSense(tPSIO, +v_ws)
(featCONJCOUNT(tPSIO, +v_f1) ^ featNEARG3(tPSIO, +v_f10)) => wordSense(tPSIO, +v_ws)

featDEPENSUBARG1(tPSIO, +v_f2) ^ featDEPENSUBARG2(tPSIO, +v_f3) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG1(tPSIO, +v_f2) ^ featDEPENSUBARG3(tPSIO, +v_f4) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG1(tPSIO, +v_f2) ^ featDEPENHEADARG1(tPSIO, +v_f5) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG1(tPSIO, +v_f2) ^ featDEPENHEADARG2(tPSIO, +v_f6) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG1(tPSIO, +v_f2) ^ featDEPENHEADARG3(tPSIO, +v_f7) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG1(tPSIO, +v_f2) ^ featNEARG1(tPSIO, +v_f8) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG1(tPSIO, +v_f2) ^ featNEARG2(tPSIO, +v_f9) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG1(tPSIO, +v_f2) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

featDEPENSUBARG2(tPSIO, +v_f3) ^ featDEPENSUBARG3(tPSIO, +v_f4) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG2(tPSIO, +v_f3) ^ featDEPENHEADARG1(tPSIO, +v_f5) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG2(tPSIO, +v_f3) ^ featDEPENHEADARG2(tPSIO, +v_f6) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG2(tPSIO, +v_f3) ^ featDEPENHEADARG3(tPSIO, +v_f7) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG2(tPSIO, +v_f3) ^ featNEARG1(tPSIO, +v_f8) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG2(tPSIO, +v_f3) ^ featNEARG2(tPSIO, +v_f9) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG2(tPSIO, +v_f3) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

featDEPENSUBARG3(tPSIO, +v_f4) ^ featDEPENHEADARG1(tPSIO, +v_f5) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG3(tPSIO, +v_f4) ^ featDEPENHEADARG2(tPSIO, +v_f6) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG3(tPSIO, +v_f4) ^ featDEPENHEADARG3(tPSIO, +v_f7) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG3(tPSIO, +v_f4) ^ featNEARG1(tPSIO, +v_f8) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG3(tPSIO, +v_f4) ^ featNEARG2(tPSIO, +v_f9) => wordSense(tPSIO, +v_ws)
featDEPENSUBARG3(tPSIO, +v_f4) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

featDEPENHEADARG1(tPSIO, +v_f5) ^ featDEPENHEADARG2(tPSIO, +v_f6) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG1(tPSIO, +v_f5) ^ featDEPENHEADARG3(tPSIO, +v_f7) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG1(tPSIO, +v_f5) ^ featNEARG1(tPSIO, +v_f8) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG1(tPSIO, +v_f5) ^ featNEARG2(tPSIO, +v_f9) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG1(tPSIO, +v_f5) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

featDEPENHEADARG2(tPSIO, +v_f6) ^ featDEPENHEADARG3(tPSIO, +v_f7) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG2(tPSIO, +v_f6) ^ featNEARG1(tPSIO, +v_f8) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG2(tPSIO, +v_f6) ^ featNEARG2(tPSIO, +v_f9) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG2(tPSIO, +v_f6) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

featDEPENHEADARG3(tPSIO, +v_f7) ^ featNEARG1(tPSIO, +v_f8) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG3(tPSIO, +v_f7) ^ featNEARG2(tPSIO, +v_f9) => wordSense(tPSIO, +v_ws)
featDEPENHEADARG3(tPSIO, +v_f7) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

featNEARG1(tPSIO, +v_f8) ^ featNEARG2(tPSIO, +v_f9) => wordSense(tPSIO, +v_ws)
featNEARG1(tPSIO, +v_f8) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

featNEARG2(tPSIO, +v_f9) ^ featNEARG3(tPSIO, +v_f10) => wordSense(tPSIO, +v_ws)

""")
    f.close()

def writeMLN2TrainingTuplesToFile(all_TP_WS_S_S_Fs):
    f = open("univ-train.db", "w+")
    incr = 0
    for TP_WS_S_S_F in all_TP_WS_S_S_Fs:
        incr += 1
        if getFeature("featCONJCOUNT", TP_WS_S_S_F):
            f.write(""" featCONJCOUNT("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featCONJCOUNT", TP_WS_S_S_F) ) )
        else:
            f.write(""" featCONJCOUNT("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featCONJCOUNT_None" ) )
        if getFeature("featDEPENSUBARG1", TP_WS_S_S_F):
            f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featDEPENSUBARG1", TP_WS_S_S_F) ) )
        else:
            f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featDEPENSUBARG1_None" ) )
        if getFeature("featDEPENSUBARG2", TP_WS_S_S_F):
            f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featDEPENSUBARG2", TP_WS_S_S_F) ) )
        else:
            f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featDEPENSUBARG2_None" ) )
        if getFeature("featDEPENSUBARG3", TP_WS_S_S_F):
            f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featDEPENSUBARG3", TP_WS_S_S_F) ) )
        else:
            f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featDEPENSUBARG3_None" ) )
        if getFeature("featDEPENHEADARG1", TP_WS_S_S_F):
            f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featDEPENHEADARG1", TP_WS_S_S_F) ) )
        else:
            f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featDEPENHEADARG1_None" ) )
        if getFeature("featDEPENHEADARG2", TP_WS_S_S_F):
            f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featDEPENHEADARG2", TP_WS_S_S_F) ) )
        else:
            f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featDEPENHEADARG2_None" ) )
        if getFeature("featDEPENHEADARG3", TP_WS_S_S_F):
            f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featDEPENHEADARG3", TP_WS_S_S_F) ) )
        else:
            f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featDEPENHEADARG3_None" ) )
        if getFeature("featNEARG1", TP_WS_S_S_F):
            f.write(""" featNEARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featNEARG1", TP_WS_S_S_F) ) )
        else:
            f.write(""" featNEARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featNEARG1_None" ) )
        if getFeature("featNEARG2", TP_WS_S_S_F):
            f.write(""" featNEARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featNEARG2", TP_WS_S_S_F) ) )
        else:
            f.write(""" featNEARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featNEARG2_None" ) )
        if getFeature("featNEARG3", TP_WS_S_S_F):
            f.write(""" featNEARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), getFeature("featNEARG3", TP_WS_S_S_F) ) )
        else:
            f.write(""" featNEARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "featNEARG3_None" ) )
        f.write(""" wordSense("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3] + str(incr), "Ws" + str(TP_WS_S_S_F[1])) )
        f.write("\n")

def writeMLN2TestingTuplesToFile(all_TP_WS_S_S_Fs, wSs):
    testQuery =  ""
    f = open("univ-test.db", "w+")
    for TP_WS_S_S_F in all_TP_WS_S_S_Fs:
        if getFeature("featCONJCOUNT", TP_WS_S_S_F):
            f.write(""" featCONJCOUNT("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featCONJCOUNT", TP_WS_S_S_F) ) )
        if getFeature("featDEPENSUBARG1", TP_WS_S_S_F):
            f.write(""" featDEPENSUBARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featDEPENSUBARG1", TP_WS_S_S_F) ) )
        if getFeature("featDEPENSUBARG2", TP_WS_S_S_F):
            f.write(""" featDEPENSUBARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featDEPENSUBARG2", TP_WS_S_S_F) ) )
        if getFeature("featDEPENSUBARG3", TP_WS_S_S_F):
            f.write(""" featDEPENSUBARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featDEPENSUBARG3", TP_WS_S_S_F) ) )
        if getFeature("featDEPENHEADARG1", TP_WS_S_S_F):
            f.write(""" featDEPENHEADARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featDEPENHEADARG1", TP_WS_S_S_F) ) )
        if getFeature("featDEPENHEADARG2", TP_WS_S_S_F):
            f.write(""" featDEPENHEADARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featDEPENHEADARG2", TP_WS_S_S_F) ) )
        if getFeature("featDEPENHEADARG3", TP_WS_S_S_F):
            f.write(""" featDEPENHEADARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featDEPENHEADARG3", TP_WS_S_S_F) ) )
        if getFeature("featNEARG1", TP_WS_S_S_F):
            f.write(""" featNEARG1("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featNEARG1", TP_WS_S_S_F) ) )
        if getFeature("featNEARG2", TP_WS_S_S_F):
            f.write(""" featNEARG2("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featNEARG2", TP_WS_S_S_F) ) )
        if getFeature("featNEARG3", TP_WS_S_S_F):
            f.write(""" featNEARG3("%s", "%s")\n """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], getFeature("featNEARG3", TP_WS_S_S_F) ) )
        for wordSense in wSs:
            testQuery += r""" wordSense(\"%s\",\"%s\") ; """ % (TP_WS_S_S_F[0] + "###" + TP_WS_S_S_F[3], "Ws" + str(wordSense))
        f.write("\n")
    return testQuery

def createUnivTrain(c2, addedTPs):
    wSs = getWordSensesThatShareSameVerbAsTPs(c2, addedTPs)
    all_TP_WS_S_S_Fs = getTuplesForMLN2(c2, wSs)
    writeMLN2TrainingTuplesToFile(all_TP_WS_S_S_Fs)
    return wSs

def createUnivTestAndGetTestQuery(c2, addedTPs):
    wSs = getWordSensesThatShareSameVerbAsTPs(c2, addedTPs)
    all_TP_WS_S_S_Fs = getTuplesForMLN2(c2, wSs)
    testQuery = writeMLN2TestingTuplesToFile(all_TP_WS_S_S_Fs, wSs)
    return testQuery

def trainMLN2(c2, addedTPs):
    print("training MLN2...")
    createunivMLN()
    wordSenses = createUnivTrain(c2, addedTPs)
    if len(wordSenses) == 1:
        subprocess.call([r""" alchemy/bin/learnwts -i univ.mln -o univ-out.mln -t univ-train.db -g -gNoEqualPredWt 1 -ne wordSense -maxSteps 30 -gMaxIter 150 > trainMLN2Output.txt """], shell=True)
    else:
        #subprocess.call([r"""alchemy/bin/learnstruct -i univ.mln -o univ-out.mln -t univ-train.db -ne wordSense > trainMLN2Output.txt """], shell=True)
        subprocess.call([r""" alchemy/bin/learnwts -i univ.mln -o univ-out.mln -t univ-train.db -ne wordSense -maxSteps 20 -gMaxIter 100 > trainMLN2Output.txt """], shell=True)
        #subprocess.call([r""" alchemy/bin/learnwts -i univ.mln -o univ-out.mln -t univ-train.db -d -ne wordSense -maxSteps 20 -dNumIter 20 > trainMLN1Output.txt """], shell=True)
    return wordSenses

def testMLN2(c2, addedTPs):
    print("testing MLN2...")
    testQuery = createUnivTestAndGetTestQuery(c2, addedTPs)
    if testQuery:
        print("testQuery: (" + str(len(testQuery)) + ") " + testQuery)
        subprocess.call(r""" alchemy/bin/infer -i univ-out.mln -e univ-test.db -r univ.results -q " """ + testQuery + r""" " -lazy -maxSteps 20 -mwsMaxSteps 200 > testMLN2Output.txt """, shell=True)
        #subprocess.call(r""" alchemy/bin/infer -i univ-out.mln -e univ-test.db -r univ.results -q " """ + testQuery + r""" " -maxSteps 10 -mwsMaxSteps 100 """, shell=True)
    else:
        print("no testing will be done, because there is no query")
        open("univ.results", "w+").close()

def moveTuplesBasedOnMLN2Clustering(c2, c3):
    changesToTupleAssignments = False
    #look at univ.results,
    print("move and/or delete TP-tuples based on MLN2...")
    removeDuplicateResultEntries("univ.results")
    results = open("univ.results", "r+")
    #populate the tpSI to probs dictionary
    dictTPSItoProbs = dict()
    dictTPSIProbsToWSs = dict()
    dictOwnerWSResultWStoProbs = dict()  #ex dictWSToWSsProbs[1409,1409] = [.25, .5]
    #merge wordSenses
    #who owns that tuple. based on that for each result add that prob of the wordsense to that wordsense
    allWordSenses = []
    for result in results:
        predicate, args, prob = getResultsTokens(result)
        resultWS = int(args[1][2:])
        allWordSenses.append(resultWS)
        allWordSenses = list(set(allWordSenses))
        tpSI = args[0]
        inputTP, inputSI = separateTPandSI(tpSI)
        ownerWS = int(c2.getWordSenseBasedOnUI(inputTP, inputSI))
        if (ownerWS,resultWS) in dictOwnerWSResultWStoProbs.keys():
            dictOwnerWSResultWStoProbs[(ownerWS,resultWS)].append(prob)
        else:
            dictOwnerWSResultWStoProbs[(ownerWS,resultWS)] = [prob]
    results.seek(0)
    #if one of wS wants to merge with another, return that wS
    print("dictOwnerWSResultWStoProbs keys: " + str(dictOwnerWSResultWStoProbs.keys()))
    wSsNotToMoveTo = [] #don't allow a wSToMergeTo to also move (but another wS can move to an already modified wSToMergeTo (bigger is ok in a single iteration so-to-speak, but smaller isn't)
    for wS in allWordSenses:
        wSToMergeTo = determineIfWSShouldMerge(wS, dictOwnerWSResultWStoProbs, allWordSenses)
        if wSToMergeTo and (not (wSToMergeTo in wSsNotToMoveTo)):
            changesToTupleAssignments = True
            wSsNotToMoveTo.append(wS)
            print("WSs MERGE:  for wS: " + str(wS) + " found wSToMergeTo: " + str(wSToMergeTo))
            for tPSI in c2.getTPsSIsOfAWordSense(wS):
                tP = tPSI[0]
                sI = tPSI[1]
                c3.execute(""" INSERT OR IGNORE INTO support (support_col, occurrences) VALUES ("%s", %s) """ % (sI, "1"))
                c3.execute(""" INSERT OR IGNORE INTO wordSenses (id_col) VALUES (%s) """ % wS)
                c3.execute(""" INSERT OR IGNORE INTO textualPattern (pattern_type) VALUES ("%s") """ % tP)
                c3.execute(""" INSERT OR IGNORE INTO deleteWSTPSupport (wordSense_col, pattern_type, support_col) VALUES (%s, "%s", "%s") """ % (wS, tP, sI)) #requires deleteNecessaryRows() to be called later (currently server is doing that)
                c2.updateRowsBasedOnUIwWSAndCopyOver(wSToMergeTo, tP, sI, c3)
    if changesToTupleAssignments:
        return True
    ########
    #move tuples to best fitting wordSense
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
    #update c3 based on any changes (moves needed)
    for key in dictTPSItoProbs.keys():
        l = dictTPSItoProbs[key]
        tpSI = key
        prob = l[-1:][0]
        wordSense = dictTPSIProbsToWSs[(tpSI,prob)]
        inputTP, inputSI = separateTPandSI(tpSI)
        #if the highest probability word sense is different than what the tuple is already assigned to, then add the WS-TP-Support to deleteWSTPSupport table and then make/copy over tuple changes. Otherwise do nothing
        orginalWS = str(c2.getWordSenseBasedOnUI(inputTP, inputSI))
        if orginalWS != str(wordSense):
            changesToTupleAssignments = True
            print("Tuple change for: " + str(inputTP) + str(inputSI) + ".  OrginalWS: " + str(orginalWS) + " gotoWS: " + str(wordSense))
            c3.execute(""" INSERT OR IGNORE INTO support (support_col, occurrences) VALUES ("%s", %s) """ % (inputSI, "1"))
            c3.execute(""" INSERT OR IGNORE INTO wordSenses (id_col) VALUES (%s) """ % orginalWS)
            c3.execute(""" INSERT OR IGNORE INTO textualPattern (pattern_type) VALUES ("%s") """ % inputTP)
            c3.execute(""" INSERT OR IGNORE INTO deleteWSTPSupport (wordSense_col, pattern_type, support_col) VALUES (%s, "%s", "%s") """ % (orginalWS, inputTP, inputSI)) #requires deleteNecessaryRows() to be called later (currently server is doing that)
            c2.updateRowsBasedOnUIwWSAndCopyOver(wordSense, inputTP, inputSI, c3)
        if changesToTupleAssignments:
            return True
    #no moves or merges
    return False

def uniqueTPsBasedOnVerb(c2, addedTPs):
    uniqueTPs = addedTPs[:]
    uniqueTPs = list(set(uniqueTPs))
    for tP1 in uniqueTPs:
        for tP2 in uniqueTPs:
            if c2.sameVerb(tP1, tP2, identicalOk=False):
                uniqueTPs.remove(tP2)
    return uniqueTPs


def run(addedTPs):
    conn2 = sqlite3.connect("taxonomyRelations.db")
    c2 = conn2.cursor(cursor)
    c2.execute("pragma foreign_keys = ON")
    conn3, c3 = extractRelations.createDB("transportedTR.db")
    c3.execute("pragma foreign_keys = ON")
    #####
    print("running mln2...")
    for tP in uniqueTPsBasedOnVerb(c2, addedTPs):
        trainMLN2(c2, [tP])
        testMLN2(c2, [tP])
        moveOrMerge = moveTuplesBasedOnMLN2Clustering(c2, c3)
    #####
    conn2.commit()
    c2.close()
    conn3.commit()
    c3.close()




"""
tPs = c2.getTPs()
tPs.sort()
for tP in tPs:
    if len(getWordSensesThatShareSameVerbAsTPs(c2, [tP])) > 7:
        print(tP + " : " + str(getWordSensesThatShareSameVerbAsTPs(c2, [tP])))

import pdb ; pdb.set_trace()

def x(wSs):
    for wS in wSs:
        c2.execute(r"select * from patterns where wordSense_col=%s" % wS)
        for i in c2.getRows():
            print i
        print("")
"""
