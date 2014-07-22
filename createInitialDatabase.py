from derivedClasses import *
import extractRelations

def quotes(string):
    return "\"" + string + "\""

def addSupportItem(supportItem, cursor):
    cursor.execute("""SELECT occurrences FROM support WHERE support_col="%s" """ % (supportItem))
    occurrences = 0
    for row in cursor:
        for item in row:
            occurrences = int(item)
    if occurrences:
        cursor.execute("""UPDATE support SET occurrences=%s WHERE support_col="%s" """ % (str(occurrences+1), supportItem))
    else:
        cursor.execute("""INSERT OR REPLACE INTO support
        VALUES ("%s",
          COALESCE(
            (SELECT occurrences FROM support
               WHERE support_col="%s"),
            0) + 1);""" % (supportItem, supportItem))

def addHypotheticalExtraSQLEntries(c):
    #Henry Marshall Tory#PER,,SUBJ:Alexander Cameron Rutherford#PER  for found
    #USE some of the features above to be inserted and make up a sentence (unique)
    #for zeugma training
    c.execute("""INSERT OR IGNORE INTO textualPattern VALUES('found_hypotecicaltextualpatternZeugma')""")
    addSupportItem('hypotecicalsupportItem1_', c)
    c.execute("""INSERT OR IGNORE INTO sentence VALUES ("sentence1")""")
    c.execute("""INSERT OR IGNORE INTO feature VALUES ('featDEPENSUBARG3_det_')""")
    c.execute("""INSERT OR IGNORE INTO feature VALUES ('featNEARG0_person')""")
    c.execute("""INSERT OR IGNORE INTO feature VALUES ('featNEARG1_person')""")
    c.execute("""INSERT OR IGNORE INTO feature VALUES ('featNEARG2_person')""")
    c.execute(""" INSERT OR IGNORE INTO feature VALUES ('featNEARG0_None') """)
    c.execute(""" INSERT OR IGNORE INTO feature VALUES ('featNEARG1_None') """)
    c.execute(""" INSERT OR IGNORE INTO feature VALUES ('featNEARG2_None') """)
    c.execute(""" INSERT OR IGNORE INTO feature VALUES ('featPOSARG3_NP') """)
    c.execute(""" INSERT OR IGNORE INTO feature VALUES ('featDEPENSUBARG1_det_') """)
    c.execute(""" INSERT OR IGNORE INTO feature VALUES ('featDEPENSUBARG2_nn_prep_as_') """)
    print("initial db creation: adding hypo patterns...")
    #for zeugma training                                                                                                                                                                   #SUBJ:Henry Marshall Tory#PER,,SUBJ:Alexander Cameron Rutherford#PER
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES("found_hypotecicaltextualpatternZeugma", 'hypotecicalsupportItem1_', "featPOSARG1_NP", "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featPOSARG2_NP', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featPOSARG3_NP', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featCONJCOUNT_1', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featDEPENSUBARG1_det_', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featDEPENSUBARG2_nn_prep_as_', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featDEPENSUBARG3_det_', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featNEARG0_person', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featNEARG1_None', "sentence1")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featNEARG2_person', "sentence1")""")
    #for reduction training
    c.execute("""INSERT OR IGNORE INTO sentence VALUES ("sentence2")""")
    c.execute("""INSERT OR IGNORE INTO feature VALUES ('featNEARG0_None')""")#                                                        #SUBJ:Henry Marshall Tory#PER,,SUBJ:Alexander Cameron Rutherford#PER
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featPOSARG1_NP', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featPOSARG2_NP', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featPOSARG3_NP', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featCONJCOUNT_2', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featDEPENSUBARG1_det_', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featDEPENSUBARG2_det_', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featDEPENSUBARG3_det_', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featNEARG0_None', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featNEARG1_None', "sentence2")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternZeugma', 'hypotecicalsupportItem1_', 'featNEARG2_person', "sentence2")""")
    #for demoing subsumption through same support item
    c.execute("""INSERT OR IGNORE INTO textualPattern VALUES('found_hypotecicaltextualpatternSubConcept')""")
    addSupportItem(u'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', c)
    c.execute("""INSERT OR IGNORE INTO sentence VALUES ("sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featPOSARG1_NP', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featPOSARG2_NP', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featPOSARG3_NP', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featCONJCOUNT_2', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featDEPENSUBARG1_det_', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featDEPENSUBARG2_det_', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featDEPENSUBARG3_det_', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featNEARG0_None', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featNEARG1_None', "sentence3")""")
    c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSubConcept', 'Henry+Marshall+Tory_Alexander+Cameron+Rutherford_', 'featNEARG2_person', "sentence3")""")
    #addSupportItem('hypotecicalsupportItem2_', c)
    #c.execute("""INSERT OR IGNORE INTO sentence VALUES ("sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featPOSARG1_NP', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featPOSARG2_NP', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featPOSARG3_NP', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featCONJCOUNT_2', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featDEPENSUBARG1_det_', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featDEPENSUBARG2_det_', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featDEPENSUBARG3_det_', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featNEARG0_None', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featNEARG1_None', "sentence4")""")
    #c.execute("""INSERT OR IGNORE INTO patterns (pattern_type, support_col, feature_col, sentence_col) VALUES('found_hypotecicaltextualpatternSuperConcept', 'hypotecicalsupportItem2_', 'featNEARG2_PERSON', "sentence4")""")


#add all things from taxonomyRelations.db.  This means that I need to satisfy the MLN equations minus inInput()- i can and probably should lie and say whatever tpX is is also inInput().
#tpX (we'll make one up) and tpY (exists already) will be zeugma test sucessfully which is two different textualPatterns with same verb, and we'll just say satisfies all the other predicates.
#for reduction formula tpX (we'll make one up) has a different support than tpY (exists already), but supposedly satisfies the other predicates

def addWordSenseTable(cursor):
    cursor.execute("""CREATE TABLE wordSenses(
    id_col INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
    ) """)

def getTextualPatterns(c):
    textualPatterns = []
    c.execute("select pattern_type from textualPattern")
    for row in c:
        for item in row:
            textualPatterns.append(item)
    return textualPatterns

def getFirstItem(c):
    for row in c:
        for item in row:
            return item

def getWordSense(c, textualPattern):
    c.execute(""" SELECT wordSense_col FROM patterns WHERE pattern_type="%s" AND wordSense_col NOT NULL   """ % (textualPattern))
    return getFirstItem(c)

def mergeWordSense(c, textualPattern, textualPatternWithSameVerb):
    #check if both have wordSense entries.
    #if neither do, create wordSense and insert  an entry into patterns for both TPs
    #if one does and the other doesn't, use the wordSense of one and insert  an entry into patterns for that TP
    #if both have same, do nothing
    #if both are different, then this raises a question--a problem that may be considered a clustering situation.  I don't think this will ever happen.
    wordSense1 = getWordSense(c, textualPattern)
    wordSense2 = getWordSense(c, textualPatternWithSameVerb)
    if (wordSense1 == None) and (wordSense2 == None):
        c.execute(""" INSERT INTO wordSenses DEFAULT VALUES """)
        c.execute(""" SELECT max(id_col) FROM wordSenses """)
        wordSenseID = getFirstItem(c)
        c.execute(""" INSERT INTO patterns (wordSense_col, pattern_type) VALUES (%s, "%s")  """ % (str(wordSenseID), textualPattern))
        c.execute(""" INSERT INTO patterns (wordSense_col, pattern_type) VALUES (%s, "%s")  """ % (str(wordSenseID), textualPatternWithSameVerb))
    elif (wordSense1) and (wordSense2 == None):
        c.execute(""" INSERT INTO patterns (wordSense_col, pattern_type) VALUES (%s, "%s")  """ % (str(wordSense1), textualPatternWithSameVerb))
    elif (wordSense1 == None) and (wordSense2):
        c.execute(""" INSERT INTO patterns (wordSense_col, pattern_type) VALUES (%s, "%s")  """ % (str(wordSense2), textualPattern))
    elif (wordSense1) and (wordSense2) and (wordSense1 == wordSense2):
        pass
    else:
        print("ERROR: It is unexpected that both TPs have a wordSense")

def assignWordSense(c, textualPattern):
    c.execute(""" INSERT INTO wordSenses DEFAULT VALUES """)
    c.execute(""" SELECT max(id_col) FROM wordSenses """)
    wordSenseID = getFirstItem(c)
    c.execute(""" INSERT INTO patterns (wordSense_col, pattern_type) VALUES (%s, "%s")  """ % (str(wordSenseID), textualPattern))

def removeSubFoundAndAssignItAWordSense(c, tPListsOfSameVerb):
    for tPListOfSameVerb in tPListsOfSameVerb:
        if u'found_hypotecicaltextualpatternSubConcept' in tPListOfSameVerb:
            tPListOfSameVerb.remove(u'found_hypotecicaltextualpatternSubConcept')
    wS = c.createNewWordSense()
    c.updateRowsBasedOnUIwWSAndCopyOver(wS, u'found_hypotecicaltextualpatternSubConcept', sI=None, otherC=None)
    return tPListsOfSameVerb

def getTPsWithSameVerb(c):
    textualPatternsWithSameVerb = [] #ex. [ [tp1, tp2], [t6], ... ]
    tPs = c.getTPs()
    for tP1 in tPs:
        tPVerbList = []
        for tP2 in tPs:
            if c.sameVerb(tP1, tP2, identicalOk=True):
                tPVerbList.append(tP2)
        tPVerbList = list(set(tPVerbList))
        if tPVerbList:
            alreadyThere = False
            for tPList in textualPatternsWithSameVerb:
                if set(tPList) == set(tPVerbList):
                    alreadyThere = True
            if not alreadyThere:
                textualPatternsWithSameVerb.append(tPVerbList)
    return textualPatternsWithSameVerb

def assignAllTPsWordSenses(c):
    #for each tp that's a sameverb createWS and update rows where the UI is TP; But do "subconcept" independently
    tPListsOfSameVerb = getTPsWithSameVerb(c)
    tPListsOfSameVerb = removeSubFoundAndAssignItAWordSense(c, tPListsOfSameVerb)
    for tPListOfSameVerb in tPListsOfSameVerb:
        wS = c.createNewWordSense()
        for tP in tPListOfSameVerb:
            c.updateRowsBasedOnUIwWSAndCopyOver(wS, tP, sI=None, otherC=None)

def run():
    #extractRelations.run(['wikiUofA.txt'], checkIfURLsHaveAlreadyBeenProcessed=False)
    conn, c = extractRelations.createDB("inputRelations.db")
    c.close()
    conn.commit()
    shutil.copyfile("inputRelations.db", "taxonomyRelations.db")
    ######################
    conn = sqlite3.connect("taxonomyRelations.db")
    c = conn.cursor(cursor)
    c.execute("pragma foreign_keys = ON")
    #addHypotheticalExtraSQLEntries(c)
    assignAllTPsWordSenses(c)
    ######################
    #c.execute("select * from patterns")
    #for row in c:
    #    print(row)
    conn.commit()
    c.close()

def main():
    pass

if __name__ == "__main__":
    pass