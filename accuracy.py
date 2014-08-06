from derivedClasses import *
from sentences import *

"""
from gold standard- for each verb: remove any sentences not found in test case

from gold standard-  sort groups from largest to smallest:
        for each item in group, find the group that has the most items in common. (that's not a group already taken)
            if no group can be found or no items in common count all sentences
        after selecting that group, count number of sentences not included

accuracy is (total sentence count of gold standard - count)/(total sentence count of gold standard)
"""

import sys

conn1 = sqlite3.connect(sys.argv[1])
c1 = conn1.cursor(cursor)

wSs1 = c1.getWordSenses()

dictWSToTPs1 = dict()
for wS in wSs1:
    tps = c1.getTPsOfAWordSense(wS)
    if (len(tps) >= 1):
        dictWSToTPs1[wS] = tps

print("1st part done.")

dictVerbToWSs1 = c1.getDictVerbToWSs()

print("2nd part done.")

verbs = dictVerbToGoldStandardSentences.keys()
dictVerbToTestSentences = dict()

for verb in verbs:
    if verb in dictVerbToWSs1.keys():
        dictVerbToTestSentences[verb] = []
        #print("\n----------------- " + str(verb) + " -----------------")
        #print("results:")
        for wS in dictVerbToWSs1[verb]:
            sentences = []
            for tP in dictWSToTPs1[wS]:
                supportOCAndSentences = c1.getListOfSupportOCAndSentences(tP, wS)
                for supportOCAndSentence in supportOCAndSentences:
                    sentence = supportOCAndSentence[2]
                    sentence = re.sub(r"""[+]""", ' ', sentence)
                    sentence = re.sub(r"(-LRB-)(.|[+]){0,40}(-RRB-)", '', sentence)
                    for sents in dictVerbToGoldStandardSentences[verb]:
                        if sentence in sents:
                            sentences.append(sentence)
                            break
                    #print("%s" % (sentence) )
            dictVerbToTestSentences[verb].append(sentences)
            dictVerbToTestSentences[verb] = sorted(dictVerbToTestSentences[verb], key=len)
            dictVerbToTestSentences[verb].reverse()

dictVerbToComparableGoldStandardSentences = dict()
for verb in verbs:
    dictVerbToComparableGoldStandardSentences[verb] = []
    for sents in dictVerbToGoldStandardSentences[verb]:
        sentsToAdd = []
        for sent in sents:
            for sentences in dictVerbToTestSentences[verb]:
                if sent in sentences:
                    sentsToAdd.append(sent)
                    break
        dictVerbToComparableGoldStandardSentences[verb].append(sentsToAdd)
        dictVerbToComparableGoldStandardSentences[verb] = sorted(dictVerbToComparableGoldStandardSentences[verb], key=len)
        dictVerbToComparableGoldStandardSentences[verb].reverse()


def getAmountInCommon(group1, group2):
    return len(set(group1).intersection(set(group2)))

def findGroup(sentsInQuestion, listOfSents, groupsTaken):
    maxAmountInCommon = 0
    bestGroup = None
    for i, sents in enumerate(listOfSents):
        if not (i in groupsTaken):
            if getAmountInCommon(sentsInQuestion, sents) > maxAmountInCommon:
                maxAmountInCommon = getAmountInCommon(sentsInQuestion, sents)
                bestGroup = i
    if bestGroup != None:
        groupsTaken.append(bestGroup)
    return bestGroup, groupsTaken



numberNotIncluded = 0
totalSentences = 0
for verb in verbs:
    #print("\nverb: " + verb)
    groupsTaken = []
    for sents in dictVerbToComparableGoldStandardSentences[verb]:
        totalSentences += len(set(sents))
        bestGroup, groupsTaken = findGroup(sents, dictVerbToTestSentences[verb], groupsTaken)
        #print bestGroup, groupsTaken
        if bestGroup == None:
            #print('could not find bestGroup')
            numberNotIncluded += len(set(sents))
        else:
            numberNotIncluded += len(set(sents) - set(dictVerbToTestSentences[verb][bestGroup]))
            #print('goldstandard:')
            #for sent in sents:
                #print sent
            #print("")
            #print("test:")
            #for sent in dictVerbToTestSentences[verb][bestGroup]:
                #print sent
            #print("numberNotIncluded: " + str(len(set(sents) - set(dictVerbToTestSentences[verb][bestGroup]))))
            #print("total in this group: " + str(len(sents)))
            #import pdb ; pdb.set_trace()

accuracy = float(totalSentences - numberNotIncluded) / float(totalSentences)
print("\n\nAccuracy: " + str(accuracy) + " : " + "totalSentences (" + str(totalSentences) + ") numberNotIncluded (" + str(numberNotIncluded) + ")")


"""for verb in verbs:
    print("\n----------------- " + str(verb) + " -----------------")
    print("results:")
    for sents in dictVerbToTestSentences[verb]:
        for sent in sents:
            print(sent)
        print("")
    print("\ngold standard:")
    listOfSentences = dictVerbToComparableGoldStandardSentences[verb]
    for sents in listOfSentences:
        for sent in sents:
            print(sent)
        print("")
"""

c1.close()
conn1.commit()


