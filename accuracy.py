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

conn1 = sqlite3.connect("taxonomyRelations.db")
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

dictVerbToTestSentences = dict()
verbs = dictVerbToGoldStandardSentences.keys()

for verb in verbs:
    if verb in dictVerbToWSs1.keys():
        dictVerbToTestSentences[verb] = []
        print("\n----------------- " + str(verb) + " -----------------")
        print("results:")
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
                    print("%s" % (sentence) )
            dictVerbToTestSentences[verb].append(sentences)
            print("")
        #print("\ngold standard:")
        for sents in dictVerbToGoldStandardSentences[verb]:
            for sent in sents:
                pass
                #print(sent)
            #print("")

"""
for verb in verbs:
    print("\n----------------- " + str(verb) + " -----------------")
    print("results:")
    for sents in dictVerbToTestSentences[verb]:
        for sent in sents:
            print(sent)
        print("")
    print("\ngold standard:")
    for sents in dictVerbToGoldStandardSentences[verb]:
        for sent in sents:
            print(sent)
        print("")
"""

c1.close()
conn1.commit()


