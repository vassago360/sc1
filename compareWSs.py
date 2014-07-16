from derivedClasses import *

conn = sqlite3.connect("taxonomyRelations.db")
c = conn.cursor(cursor)
wSs = c.getWordSenses()

for wS in wSs:
    if (len(c.getTPsOfAWordSense(wS)) < 1):
        wSs.remove(wS)

dictWSToTPs = dict()
for wS in wSs:
    tps = c.getTPsOfAWordSense(wS)
    dictWSToTPs[wS] = tps

for i, wS1 in enumerate(wSs):
    wSs.remove(wS1)
    print("wS " + str(wS1) + ":")
    for tP in dictWSToTPs[wS1]:
        supportOCAndSentences = c.getListOfSupportOCAndSentences(tP, wS1)
        for supportOCAndSentence in supportOCAndSentences:
            print("\t%s | %s " % (tP, supportOCAndSentence[2]) )
    for wS2 in wSs[i:]:
        if c.sameVerb(dictWSToTPs[wS1][0], dictWSToTPs[wS2][0]):
            wSs.remove(wS2)
            print("wS " + str(wS2) + ":")
            for tP in dictWSToTPs[wS2]:
                supportOCAndSentences = c.getListOfSupportOCAndSentences(tP, wS2)
                for supportOCAndSentence in supportOCAndSentences:
                    print("\t%s | %s " % (tP, supportOCAndSentence[2]) )
    print("")
    print("")