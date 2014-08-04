from derivedClasses import *
from sentences import *

conn1 = sqlite3.connect("cleanWikiBrownRefinedVerbsTaxRelations1.db")
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

verbs = dictVerbToSentences.keys()

for verb in verbs:
    if verb in dictVerbToWSs1.keys():
        print("\n----------------- " + str(verb) + " -----------------")
        print("results:")
        for wS in dictVerbToWSs1[verb]:
            count = 0
            for tP in dictWSToTPs1[wS]:
                supportOCAndSentences = c1.getListOfSupportOCAndSentences(tP, wS)
                for supportOCAndSentence in supportOCAndSentences:
                    count += 1
                    sentence = supportOCAndSentence[2]
                    sentence = re.sub(r"""[+]""", ' ', sentence)
                    sentence = re.sub(r"(-LRB-)(.|[+]){0,40}(-RRB-)", '', sentence)
                    print("%s" % (sentence) )
            print("")
        print("\ngold standard:")
        for sents in dictVerbToSentences[verb]:
            for sent in sents:
                print(sent)
            print("")




