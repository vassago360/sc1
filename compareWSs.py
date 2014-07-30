from derivedClasses import *

"""wSs = c2.getWordSenses()

for wS in wSs[:]:
    if (len(c2.getTPsOfAWordSense(wS)) < 1):
        wSs.remove(wS)

dictWSToTPs = dict()
for wS in wSs:
    tps = c2.getTPsOfAWordSense(wS)
    dictWSToTPs[wS] = tps

for i, wS1 in enumerate(wSs):
    wSs.remove(wS1)
    print("wS " + str(wS1) + ":")
    for tP in dictWSToTPs[wS1]:
        supportOCAndSentences = c2.getListOfSupportOCAndSentences(tP, wS1)
        for supportOCAndSentence in supportOCAndSentences:
            print("\t%s | %s " % (tP, supportOCAndSentence[2]) )
    for wS2 in wSs[i:]:
        if c2.sameVerb(dictWSToTPs[wS1][0], dictWSToTPs[wS2][0]):
            wSs.remove(wS2)
            print("wS " + str(wS2) + ":")
            for tP in dictWSToTPs[wS2]:
                supportOCAndSentences = c2.getListOfSupportOCAndSentences(tP, wS2)
                for supportOCAndSentence in supportOCAndSentences:
                    print("\t%s | %s " % (tP, supportOCAndSentence[2]) )
    print("")
    print("")"""

conn1 = sqlite3.connect("dirtyLargeBrownTaxRelations.db")
c1 = conn1.cursor(cursor)

conn2 = sqlite3.connect("dirtyLargeTaxRelations.db")
c2 = conn2.cursor(cursor)

wSs1 = c1.getWordSenses()
wSs2 = c2.getWordSenses()

dictWSToTPs1 = dict()
for wS in wSs1:
    tps = c1.getTPsOfAWordSense(wS)
    if (len(tps) >= 1):
        dictWSToTPs1[wS] = tps

dictWSToTPs2 = dict()
for wS in wSs2:
    tps = c2.getTPsOfAWordSense(wS)
    if (len(tps) >= 1):
        dictWSToTPs2[wS] = tps

print("1st part done.")

dictVerbToWSs1 = c1.getDictVerbToWSs()
dictVerbToWSs2 = c2.getDictVerbToWSs()

print("2nd part done.")

verbs = []
verbSiblings = []
for verb in (dictVerbToWSs2.keys() + dictVerbToWSs1.keys()):
    if ("+" in verb) and not (verb in verbSiblings):
        verbSiblings.append(verb)
        firstWord = re.split(r"[+]", verb)[0]
        if not (firstWord in verbs):
            verbs.append(firstWord)
verbs.sort()

verbs = ["argue","base","be","begin","bring","call","conduct","do","enter","follow","give","have","head","introduce","know","lead","live","make","move","operate","place","play","run","serve","succeed","take"]
sentences = []

for verb in verbs:
    printVerb = False
    if verb in dictVerbToWSs1.keys():
        sentCount = 0
        for wS in dictVerbToWSs1[verb]:
            for tP in dictWSToTPs1[wS]:
                supportOCAndSentences = c1.getListOfSupportOCAndSentences(tP, wS)
                for supportOCAndSentence in supportOCAndSentences:
                    sentCount += 1
        if sentCount > 1:
            if not printVerb:
                    print("\n----------------- " + str(verb) + " -----------------")
                    printVerb = True
            for wS in dictVerbToWSs1[verb]:
                count = 0
                for tP in dictWSToTPs1[wS]:
                    supportOCAndSentences = c1.getListOfSupportOCAndSentences(tP, wS)
                    for supportOCAndSentence in supportOCAndSentences:
                        count += 1
                        sentence = supportOCAndSentence[2]
                        sentence = re.sub(r"""[+]""", ' ', sentence)
                        sentences.append(sentence)
                        sentence = re.sub(r"(-LRB-)(.|[+]){0,40}(-RRB-)", '', sentence)
                        print("%s%s.%s   %s" % ("1", wS, count, sentence) )
    if verb in dictVerbToWSs2.keys():
        sentCount = 0
        for wS in dictVerbToWSs2[verb]:
            for tP in dictWSToTPs2[wS]:
                supportOCAndSentences = c2.getListOfSupportOCAndSentences(tP, wS)
                for supportOCAndSentence in supportOCAndSentences:
                    sentCount += 1
        if sentCount > 1:
            if not printVerb:
                    print("\n----------------- " + str(verb) + " -----------------")
                    printVerb = True
            for wS in dictVerbToWSs2[verb]:
                count = 0
                for tP in dictWSToTPs2[wS]:
                    supportOCAndSentences = c2.getListOfSupportOCAndSentences(tP, wS)
                    for supportOCAndSentence in supportOCAndSentences:
                        count += 1
                        sentence = supportOCAndSentence[2]
                        sentence = re.sub(r"""[+]""", ' ', sentence)
                        sentences.append(sentence)
                        sentence = re.sub(r"(-LRB-)(.|[+]){0,40}(-RRB-)", '', sentence)
                        print("%s%s.%s   %s" % ("2", wS, count, sentence) )

pickle.dump( sentences, open('ambigiousSentences.p', 'wb'))
#import pdb ; pdb.set_trace()

"""for verb in dictVerbToWSs2.keys():
    print("\n----------------- " + str(verb) + " -----------------")
    for wS in dictVerbToWSs2[verb]:
        count = 0
        for tP in dictWSToTPs2[wS]:
            supportOCAndSentences = c2.getListOfSupportOCAndSentences(tP, wS)
            for supportOCAndSentence in supportOCAndSentences:
                count += 1
                sentence = supportOCAndSentence[2]
                sentence = re.sub(r"(-LRB-)(.|[+]){0,40}(-RRB-)", '', sentence)
                sentence = re.sub(r"[+]", ' ', sentence)
                print("%s.%s |  %s " % (wS, count, sentence) )"""



