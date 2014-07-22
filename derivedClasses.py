import sqlite3, re, shutil, subprocess, exemplarExtract, stanfordDepen, stanfordPOS, figerNER, boilerpipe.extract, pickle, os, urllib2, time, sys,  nltk, random, numpy
#import igraph

#class graph(igraph.Graph):
#    pass

class cursor(sqlite3.Cursor):
    def removeDuplicates(self, listOfLists):
            for i, l1 in enumerate(listOfLists):
                for j, l2 in enumerate(listOfLists):
                    if (l1 == l2) and (i != j):
                        listOfLists[j] = []
            while [] in listOfLists:
                listOfLists.remove([])
            return listOfLists
    def sameOfLOL(self, lol1, lol2):
        for l1 in lol1:
            if not (l1 in lol2):
                return False
        return True
    def convertRowsToBeInsertable(self, rows):
        rows = list(rows)
        for i in range(len(rows)):
            rows[i] = list(rows[i])
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if rows[i][j] == None:
                    rows[i][j] = u"NULL"
                else:
                    rows[i][j] = "\"" + str(rows[i][j]) + "\""
        for i in range(len(rows)):
            rows[i] = tuple(rows[i])
        return rows
    def getFirstItem(self):
        for row in self:
            for item in row:
                return [item]
        return [None]
    def getAllItems(self):
        items = []
        for row in self:
            for item in row:
                items.append(item)
        return items
    def getRows(self):
        rows = []
        for row in self:
            rows.append(list(row))
        return rows
    def queryProducedAResponse(self):
        for row in self:
            return True
        return False
    def getSupportFromRows(self, rows):
        #from a list of lists get 3rd element which is the support
        support = []
        for row in rows:
            support.append(row[2])
        support = list(set(support))
        return support
    def removeSingleEntries(self, listOfLists):
        lolCopy = listOfLists[:]
        for l in   lolCopy:
            if len(l) == 1:
                listOfLists.remove(l)
    def sameVerb(self, tP1, tP2, identicalOk=False):
        if (re.split(r'_+', tP1.__str__())[0] == re.split(r'_+', tP2.__str__())[0]) and (tP1 != tP2):
            return True
        else:
            if identicalOk and (re.split(r'_+', tP1.__str__())[0] == re.split(r'_+', tP2.__str__())[0]):
                return True
            else:
                return False
    def sameSupport(self, tPOfAWordSense, otherC, tPInQuestion):
        self.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and support_col NOT NULL """ % (tPOfAWordSense))
        tP1Support = self.getAllItems()
        otherC.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and support_col NOT NULL """ % (tPInQuestion))
        tP2Support = otherC.getAllItems()
        for tP1SI in tP1Support:
            if tP2Support.count(tP1SI):
                return True
        return False
    def sameSupportDifferentDB(self, tP, otherC):
        self.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and support_col NOT NULL """ % (tP))
        selfSupport = self.getAllItems()
        otherC.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and support_col NOT NULL """ % (tP))
        otherSupport = otherC.getAllItems()
        for selfSI in selfSupport:
            if otherSupport.count(selfSI):
                return True
        return False
    def sameWordSense(self, wsTP1, wsTP2):
        #ex. wsTP1 = [ws1, tp1]    wsTP2 = [ws1, tp5]      -> return true
        if (wsTP1[0] == wsTP2[0]) and (wsTP1[1] != wsTP2[1]):
            return True
        else:
            return False
    def rowIsIn(self, values, schema):
        #check to see if the row is already in patterns table
        executionString = "SELECT * FROM patterns WHERE "
        length = len(schema)
        for i in range(len(schema)):
            if values[i] == "NULL":
                executionString += schema[i] + " is NULL"
            else:
                executionString += schema[i] + "=" + values[i]
            if i < (length - 1):
                executionString += " AND "
        #executionString = "SELECT * FROM patterns WHERE wordSense_col is NULL"
        #print("executionString: " + executionString)
        self.execute(executionString)
        if self.getRows():
            return True
        else:
            return False
    def uRLProcessed(self, url):
        self.execute(""" SELECT url_col FROM urlsProcessed WHERE url_col="%s" """ % (url))
        for item in self.getAllItems():
            if item == url:
                return True
            else:
                return False
    def addURL(self, url):
        self.execute(""" INSERT OR IGNORE INTO urlsProcessed (url_col) VALUES ("%s") """ % (url))
    def checkIfTPSIIsBeingUsed(self, tP, sI):
        self.execute(""" SELECT * FROM PATTERNS WHERE pattern_type="%s" and support_col="%s"  """ % (tP, sI))
        if self.getAllItems():
            return True
        else:
            return False
    def checkIfTwoRowsShareTPSISentence(self, row1, row2): #assumes the order of the columns index 2 is TP; index 3 is SI index5 is sentence ; index 1 is wordSense
        if (row1[5] == row2[5]) and (row1[3] == row2[3]) and (row1[2] == row2[2]) and (row1[1] != row2[1]):
            return True
        else:
            return False
    def copyOverURLsProcessed(self, otherC):
        #copy self's urls processed over to otherC
        self.execute(""" SELECT url_col FROM urlsProcessed """)
        for url in self.getAllItems():
            otherC.addURL(url)
    def getTPs(self):
        self.execute("select pattern_type from textualPattern")
        textualPatterns = self.getAllItems()
        return textualPatterns
    def getWordSenses(self):
        self.execute(""" SELECT id_col FROM wordSenses  """)
        return self.getAllItems()
    def getWordSense(self, textualPattern, all=False):
        self.execute(""" SELECT DISTINCT wordSense_col FROM patterns WHERE pattern_type="%s" AND wordSense_col NOT NULL   """ % (textualPattern))
        wordSenses = self.getAllItems()
        if len(wordSenses) == 0:
            print("ERROR: No wordSense found for tP: " + str(textualPattern))
            raise NameError("ERROR: No wordSense found for tP: " + str(textualPattern))
        if (len(wordSenses) > 1) and (not all):
            print("WARNING: Multiple wordSenses found for tP: " + str(textualPattern) + "  There are: " + str(wordSenses))
        if all:
            return wordSenses
        else:
            return wordSenses[0]
    def getWordSenseBasedOnUI(self, tP, sI):
        self.execute(""" SELECT wordSense_col FROM patterns WHERE pattern_type="%s" and support_col="%s" """ % (tP, sI))
        wordSense = self.getFirstItem()
        return wordSense[0]
    def getDictVerbToWSs(self):
        wSs = self.getWordSenses()
        dictVerbToWSs = dict()
        for wS in wSs[:]:
            tps = self.getTPsOfAWordSense(wS)
            if len(tps) < 1:
                wSs.remove(wS)
            else:
                verb = re.split(r'_+', tps[0].__str__())[0]
                if verb in dictVerbToWSs.keys():
                    dictVerbToWSs[verb].append(wS)
                else:
                    dictVerbToWSs[verb] = [wS]
        return dictVerbToWSs
    def getDictWSToTPs(self):
        wSs = self.getWordSenses()
        ###
        dictWSToTPs = dict()
        for wS in wSs:
            tps = self.getTPsOfAWordSense(wS)
            if (len(tps) >= 1):
                dictWSToTPs[wS] = tps
        return dictWSToTPs
    def getDictVerbsToSupportItems(self):
        dictVerbsToSupportItems = dict()
        dictWSToTPs = self.getDictWSToTPs()
        dictVerbToWSs = self.getDictVerbToWSs()
        print('first part done')
        for verb in dictVerbToWSs.keys():
            for wS in dictVerbToWSs[verb]:
                for tP in dictWSToTPs[wS]:
                    supportOCAndSentences = self.getListOfSupportOCAndSentences(tP, wS)
                    for supportOCAndSentence in supportOCAndSentences:
                        support = supportOCAndSentence[0]
                        if verb in dictVerbsToSupportItems.keys():
                            dictVerbsToSupportItems[verb].append(support)
                        else:
                            dictVerbsToSupportItems[verb] = [support]
        return dictVerbsToSupportItems
    def getTPsSIsOfAWordSense(self, wordSense):
        self.execute("select pattern_type, support_col from patterns where wordSense_col=%s" % wordSense)
        return self.getRows()
    def getWSsAndTheirTPs(self):
        self.execute(""" SELECT DISTINCT wordSense_col, pattern_type FROM patterns WHERE wordSense_col NOT NULL  """)
        wSsAndTheirTPs = self.getRows()
        return wSsAndTheirTPs
    def getEverythingOfATPSI(self, tP, sI=None):
        if sI == None:
            self.execute(""" SELECT * FROM patterns WHERE pattern_type="%s" """ % (tP))
        else:
            self.execute(""" SELECT * FROM patterns WHERE pattern_type="%s" and support_col="%s" """ % (tP, sI))
        rows = self.getRows()
        rows = self.convertRowsToBeInsertable(rows)
        return rows
    def getTPsOfAWordSense(self, wordSense):
        self.execute("select distinct pattern_type from patterns where wordSense_col=%s" % wordSense)
        return self.getAllItems()
    def getTPsWithSameWordSense(self, removeSingleEntries=True, includeWordSense=False):
        #handle includeWordSense=false.  self has wordSenses
        tPsWithSameWordSense = [] #ex. [ [tp1, tp1, t2, t2], [t6, t7] ... ] or  [ [ws, tp1, tp1, t2, t2], [ws, t6, t7] ... ]
        wSsAndTheirTPs = self.getWSsAndTheirTPs()
        #do the combining of tPs
        for wsTP1 in wSsAndTheirTPs:
            wsTPList = wsTP1[:]
            for wsTP2 in wSsAndTheirTPs:
                if self.sameWordSense(wsTP1, wsTP2):
                    wsTPList.append(wsTP2[1])
            wsTPList = self.removeDuplicates(wsTPList)
            if wsTPList:
                alreadyThere = False
                for tPList in tPsWithSameWordSense:
                    if self.sameOfLOL(tPList, wsTPList):
                        alreadyThere = True
                if not alreadyThere:
                    tPsWithSameWordSense.append(wsTPList)
        #end the combining of tPs
        #sort wordSenses
        tPsWithSameWordSense.sort()
        #remove wordSenses if not includeWordSense
        if not includeWordSense:
            for i, tPList in enumerate(tPsWithSameWordSense):
                tPsWithSameWordSense[i] = tPsWithSameWordSense[i][1:]
        if removeSingleEntries:
            self.removeSingleEntries(tPsWithSameWordSense)
        return tPsWithSameWordSense
    def getTPsWithNoMatch(self, otherC): #note: x.getTPsWithNoMatch(y) != y.getTPsWithNoMatch(x)
        #assumes self is c1 and otherC is c2
        tPListWithSameVerb = self.getTPsWithSameVerbButNothingElseAsWhatsInTheOtherDB(otherC, includeWordSense=False, otherCHasWordSenses=True)
        tPListWithSameVerb = list(set(tPListWithSameVerb))
        tPs = self.getTPs()
        otherTPs = otherC.getTPs()
        tPsWithNoExactMatch = list(set(tPs) - set(otherTPs))
        tPsWithNoMatch = tPsWithNoExactMatch[:]
        for tP in tPListWithSameVerb:
            if tP in tPsWithNoMatch:
                tPsWithNoMatch.remove(tP)
        return tPsWithNoMatch
    def getTPsWithSameTPAndSameSupportItem(self, otherC):
        tPs = self.getTPs()
        otherTPs = otherC.getTPs()
        tPsWithSameTP = list(set(tPs).intersection(set(otherTPs)))
        tPsWithSameTPAndSameSI = []
        for tPWithSameTP in tPsWithSameTP:
            if self.sameSupportDifferentDB(tPWithSameTP, otherC):
                tPsWithSameTPAndSameSI.append(tPWithSameTP)
        return tPsWithSameTPAndSameSI
    def getTPsWithSameVerb(self):
        textualPatternsWithSameVerb = [] #ex. [ [tp1, tp2], [t6], ... ]
        tPs = self.getTPs()
        for tP1 in tPs:
            tPVerbList = []
            for tP2 in tPs:
                if self.sameVerb(tP1, tP2,  identicalOk=True):
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
    def getTPsWithSameVerbButNothingElseAsWhatsInTheOtherDB(self, otherC, includeWordSense=False, otherCHasWordSenses=True):
        textualPatternsWithSameVerb = [] #ex. [ tp1, tp2, t6, t7 ... ] or  [ [ws1, tp1], [ws1, tp2], [ws2, t6], [ws2, t7] ... ]
        if includeWordSense and (not otherCHasWordSenses): #training where self is c2 and otherC is c1
            tPsWithSameWordSense = self.getTPsWithSameWordSense(removeSingleEntries=False, includeWordSense=True) #important needs to be able to use wordSenses, but it is equally important not to use wordSenses when includeWordSense=False  ex. [ [ws1, tp1], [ws1, tp2], [ws1, tp3], [w3, t4], [w4, t6] ]
            otherTPsWithSameWordSense = otherC.getTPsWithSameVerb() #ex. [ [tp8], [t9, t10], [t1] ... ]
            for tPsOfAWordSense in tPsWithSameWordSense:
                for tP in tPsOfAWordSense[1:]:
                    for otherTPsOfAWordSense in otherTPsWithSameWordSense:
                        for otherTP in otherTPsOfAWordSense:
                            if self.sameVerb(tP, otherTP):
                                if not ([tPsOfAWordSense[0], tP] in textualPatternsWithSameVerb):
                                    textualPatternsWithSameVerb.append( [tPsOfAWordSense[0], tP] )
        if (not includeWordSense) and otherCHasWordSenses: #testing where self is c1 and otherC is c2
            tPsWithSameWordSense = self.getTPsWithSameVerb() #ex. [ [tp8], [t9, t10], [t1] ... ] #tPsWithSameWordSense suggests that we're working with wordSenses, but if includeWordSense=False it's because self is the inputDB that doesn't have wordSenses
            otherTPsWithSameWordSense = otherC.getTPsWithSameWordSense(removeSingleEntries=False, includeWordSense=False) #ex. [ [tp8], [t9, t10], [t1] ... ]
            for tPsOfAWordSense in tPsWithSameWordSense:
                for tP in tPsOfAWordSense:
                    for otherTPsOfAWordSense in otherTPsWithSameWordSense:
                        for otherTP in otherTPsOfAWordSense:
                            if self.sameVerb(tP, otherTP):
                                if not (tP in textualPatternsWithSameVerb):
                                    textualPatternsWithSameVerb.append( tP )
        return textualPatternsWithSameVerb
    def getTPsWithSameTPButNothingElse(self, otherC, includeWordSense=False, otherCHasWordSenses=True):
        tPsWithSameTP = [] #ex. [ tp1, tp2, t6, t7 ... ] or  [ [ws1, tp1], [ws1, tp2], [ws2, t6], [ws2, t7] ... ]
        if includeWordSense and (not otherCHasWordSenses): #training where self is c2 and otherC is c1
            tPsWithSameWordSense = self.getTPsWithSameWordSense(removeSingleEntries=False, includeWordSense=True) #ex. [ [ws1, tp1, tp1, t2, t2], [ws2, t6, t7] ... ]
            otherTPsWithSameWordSense = otherC.getTPsWithSameVerb() #ex. [ [tp8], [t9, t10], [t1] ... ]
            for tPsOfAWordSense in tPsWithSameWordSense:
                for tP in tPsOfAWordSense[1:]:
                    for otherTPsOfAWordSense in otherTPsWithSameWordSense:
                        for otherTP in otherTPsOfAWordSense:
                            if (tP == otherTP) and (not self.sameSupport(tP, otherC, otherTP)):
                                if not ([tPsOfAWordSense[0], tP] in tPsWithSameTP):
                                    tPsWithSameTP.append( [tPsOfAWordSense[0], tP] )
        if (not includeWordSense) and otherCHasWordSenses: #testing where self is c1 and otherC is c2
            tPsWithSameWordSense = self.getTPsWithSameVerb() #ex. [ [tp8], [t9, t10], [t1] ... ] #tPsWithSameWordSense suggests that we're working with wordSenses, but if includeWordSense=False it's because self is the inputDB that doesn't have wordSenses
            otherTPsWithSameWordSense = otherC.getTPsWithSameWordSense(removeSingleEntries=False, includeWordSense=False) #ex. [ [tp8], [t9, t10], [t1] ... ]
            for tPsOfAWordSense in tPsWithSameWordSense:
                for tP in tPsOfAWordSense:
                    for otherTPsOfAWordSense in otherTPsWithSameWordSense:
                        for otherTP in otherTPsOfAWordSense:
                            if (tP == otherTP) and (not self.sameSupport(tP, otherC, otherTP)):
                                if not (tP in tPsWithSameTP):
                                    tPsWithSameTP.append( tP )
        return tPsWithSameTP
    def getTPsWithSameVerbButNothingElseOfATP(self, tP):
        textualPatternsWithSameVerb = []
        self.execute(""" SELECT pattern_type FROM textualPattern """)
        tPsToCompare = self.getAllItems()
        for tPToCompare in tPsToCompare:
            if self.sameVerb(tPToCompare, tP):
                textualPatternsWithSameVerb.append(tPToCompare)
        return textualPatternsWithSameVerb
    def getTPsWithSameTPButNothingElseOfATP(self, otherC, tP):
        tPsWithSameTP = []
        self.execute(""" SELECT pattern_type FROM textualPattern """)
        tPsToCompare = self.getAllItems()
        for tPToCompare in tPsToCompare:
            if (tPToCompare == tP) and not self.sameSupport(tPToCompare, otherC, tP):
                tPsWithSameTP.append(tPToCompare)
        return tPsWithSameTP
    def getListOfSupportAndSentenceFeatures(self, textualPattern, wordSense=None):  #wordSense is None when getting support and sentence features from inputDB c1.  Otherwise for the taxonomyDB including a wordSense gets more accurate features.
        supportAndSentenceFeatures = [] #ex. [ [supportItem, feature1, .... featureN], ... ]
        if wordSense == None:
            self.execute(""" SELECT DISTINCT sentence_col FROM patterns WHERE pattern_type="%s" and sentence_col NOT NULL ORDER BY sentence_col DESC """ % (textualPattern))
            sentences = self.getAllItems()
            for sentence in sentences:
                self.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and sentence_col="%s" and support_col NOT NULL """ % (textualPattern, sentence))
                support = self.getFirstItem()
                self.execute(""" SELECT feature_col FROM patterns WHERE pattern_type="%s" and sentence_col="%s" and feature_col NOT NULL """ % (textualPattern, sentence))
                features = self.getAllItems()
                supportAndSentenceFeatures.append(support + features)
        if wordSense:
            self.execute(""" SELECT DISTINCT sentence_col FROM patterns WHERE pattern_type="%s" and wordSense_col=%s and sentence_col NOT NULL ORDER BY sentence_col DESC """ % (textualPattern, wordSense))
            sentences = self.getAllItems()
            for sentence in sentences:
                self.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and wordSense_col=%s and sentence_col="%s" and support_col NOT NULL """ % (textualPattern, wordSense, sentence))
                support = self.getFirstItem()
                self.execute(""" SELECT feature_col FROM patterns WHERE pattern_type="%s" and wordSense_col=%s and sentence_col="%s" and feature_col NOT NULL """ % (textualPattern, wordSense, sentence))
                features = self.getAllItems()
                supportAndSentenceFeatures.append(support + features)
        return supportAndSentenceFeatures
    def getListOfTPsAndWSsAndSentencesAndSupportAndFeatures(self, textualPattern, wordSense):
        tPsAndWSsAndSentencesAndSupportAndSentenceFeatures = [] #ex. [ [tp, ws, sentence, supportItem, feature1, .... featureN], ... ]
        self.execute(""" SELECT DISTINCT sentence_col FROM patterns WHERE pattern_type="%s" and wordSense_col=%s and sentence_col NOT NULL ORDER BY sentence_col DESC """ % (textualPattern, wordSense))
        sentences = self.getAllItems()
        for sentence in sentences:
            self.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and wordSense_col=%s and sentence_col="%s" and support_col NOT NULL """ % (textualPattern, wordSense, sentence))
            support = self.getFirstItem()
            self.execute(""" SELECT feature_col FROM patterns WHERE pattern_type="%s" and wordSense_col=%s and sentence_col="%s" and feature_col NOT NULL """ % (textualPattern, wordSense, sentence))
            features = self.getAllItems()
            tPsAndWSsAndSentencesAndSupportAndSentenceFeatures.append([textualPattern] + [wordSense] + [sentence] + support + features)
        return tPsAndWSsAndSentencesAndSupportAndSentenceFeatures
    def getListOfSupportOCAndSentences(self, textualPattern, wordSense=None):
        supportOCAndSentences = [] #ex. [ [supportItem, occurrenceCount, sentence], ... ]
        if wordSense:
            self.execute(""" SELECT DISTINCT sentence_col FROM patterns WHERE pattern_type="%s" and wordSense_col=%s and sentence_col NOT NULL ORDER BY sentence_col DESC """ % (textualPattern, wordSense))
        else:
            self.execute(""" SELECT DISTINCT sentence_col FROM patterns WHERE pattern_type="%s" and sentence_col NOT NULL ORDER BY sentence_col DESC """ % (textualPattern))
        sentences = self.getAllItems()
        for sentence in sentences:
            self.execute(""" SELECT support_col FROM patterns WHERE pattern_type="%s" and sentence_col="%s" and support_col NOT NULL """ % (textualPattern, sentence))
            support = self.getFirstItem()[0]
            self.execute(""" SELECT occurrences FROM support WHERE support_col="%s"  """ % (support))
            occurrenceCount = self.getFirstItem()[0]
            supportOCAndSentences.append([support, occurrenceCount, sentence])
        return supportOCAndSentences
    def getNextAvailableWordSense(self):
        self.execute(""" SELECT max(id_col) FROM wordSenses """)
        lastWordSense = self.getFirstItem()[0]
        nextAvailableWordSense = lastWordSense + 1
        return nextAvailableWordSense
    def getNextAvailableWordSenseMin1000000(self):
        self.execute(""" SELECT max(id_col) FROM wordSenses """)
        lastWordSense = self.getFirstItem()
        if lastWordSense:
            lastWordSense = lastWordSense[0]
        else:
            lastWordSense = 0
        if lastWordSense < 1000000:
            lastWordSense = 1000000
        nextAvailableWordSense = lastWordSense + 1
        return nextAvailableWordSense
    def createNewWordSense(self, wordSense=None):
        if not wordSense:
            self.execute(""" INSERT INTO wordSenses DEFAULT VALUES """)
            self.execute(""" SELECT max(id_col) FROM wordSenses """)
            wordSenseID = self.getFirstItem()[0]
        if wordSense:
            self.execute(""" INSERT INTO wordSenses (id_col) VALUES (%s) """ % (wordSense))
            wordSenseID = wordSense
        return wordSenseID
    def renameHighWordSensesToNextAvailableWordSenseOfOtherC(self, c2):
        nextWS = c2.getNextAvailableWordSense()
        self.execute(""" select distinct * from wordSenses where id_col >= 1000000 """)
        wordSensesToChange = self.getAllItems()
        for wordSenseToChange in wordSensesToChange:
            self.execute(""" INSERT OR IGNORE INTO wordSenses (id_col) VALUES (%s) """ % (nextWS))
            self.execute(""" UPDATE patterns SET wordSense_col=%s WHERE wordSense_col=%s """ % (nextWS, wordSenseToChange))
            self.execute(""" DELETE FROM wordSenses WHERE id_col=%s """ % (wordSenseToChange))
            nextWS += 1
    def copyOverEverything(self, otherC):
        #copy over processedURLs
        self.copyOverURLsProcessed(otherC)
        #copy over everything else
        self.execute(""" SELECT wordSense_col, pattern_type, support_col, feature_col, sentence_col FROM patterns """)
        rows = self.convertRowsToBeInsertable(self.getRows())
        #add support-- if there are rows, then at least one row is being added.  We only want one update of occurrence, so that's why it's not running in the below for loop
        if rows:
            support = self.getSupportFromRows(rows) #ex. ["Peter+Pond_Fort+Athabasca_", "Roderick+Mackenzie_Fort+Chipewyan_"]
            for sI in support:
                self.execute(""" SELECT occurrences FROM support WHERE support_col= %s """ % (sI))
                sC = self.getFirstItem()[0]
                otherC.execute(""" SELECT occurrences FROM support WHERE support_col= %s """ % (sI))
                oC = otherC.getFirstItem()
                if oC[0]:
                    oC = oC[0]+sC
                    otherC.execute(""" UPDATE support SET occurrences=%s WHERE support_col=%s """ % (str(oC), sI))
                else:
                    oC = sC
                    otherC.execute(""" INSERT INTO support (support_col, occurrences) VALUES (%s, %s) """ % (sI, str(oC)))
        #add other fields
        for row in rows:
            if not otherC.rowIsIn(row, ("wordSense_col", "pattern_type", "support_col", "feature_col", "sentence_col")): #check to see if the row is already in patterns table
                #print("trying to add stuff...")
                otherC.execute(""" INSERT OR IGNORE INTO wordSenses (id_col) VALUES (%s) """ % row[0])
                otherC.execute(""" INSERT OR IGNORE INTO textualPattern (pattern_type) VALUES (%s) """ % row[1])
                otherC.execute(""" INSERT OR IGNORE INTO feature (feature_col) VALUES (%s) """ % row[3])
                otherC.execute(""" INSERT OR IGNORE INTO sentence (sentence_col) VALUES (%s) """ % row[4])
                otherC.execute(""" INSERT OR IGNORE INTO patterns (wordSense_col, pattern_type, support_col, feature_col, sentence_col) VALUES (%s, %s, %s, %s, %s) """ % tuple(row) )
    def updateRowsBasedOnUIwWSAndCopyOver(self, wS, tP, sI=None, otherC=None): #note: it's not as accurate as if UI was sentence and not tP or tPSI
        #It needs to update rows of self with wordSense.  if otherC, copy those rows over.
        #update rows
        if sI == None:
            self.execute(""" INSERT OR IGNORE INTO wordSenses (id_col) VALUES (%s) """ % (wS))
            self.execute(""" UPDATE patterns SET wordSense_col=%s WHERE pattern_type="%s" """ % (wS, tP))
        else:
            self.execute(""" INSERT OR IGNORE INTO wordSenses (id_col) VALUES (%s) """ % (wS))
            self.execute(""" UPDATE patterns SET wordSense_col=%s WHERE pattern_type="%s" and support_col="%s" """ % (wS, tP, sI))
        #copy over those rows (minus the id_col)
        if otherC:
            if sI == None:
                self.execute(""" SELECT wordSense_col, pattern_type, support_col, feature_col, sentence_col FROM patterns WHERE wordSense_col=%s and pattern_type="%s" """ % (wS, tP))
            else:
                self.execute(""" SELECT wordSense_col, pattern_type, support_col, feature_col, sentence_col FROM patterns WHERE wordSense_col=%s and pattern_type="%s" and support_col="%s" """ % (wS, tP, sI))
            rows = self.convertRowsToBeInsertable(self.getRows())
            #add support-- if there are rows, then at least one row is being added.  We only want one update of occurrence, so that's why it's not running in the below for loop
            if rows:
                support = self.getSupportFromRows(rows) #ex. ["Peter+Pond_Fort+Athabasca_", "Roderick+Mackenzie_Fort+Chipewyan_"]
                for sI in support:
                    self.execute(""" SELECT occurrences FROM support WHERE support_col= %s """ % (sI))
                    sC = self.getFirstItem()[0]
                    otherC.execute(""" SELECT occurrences FROM support WHERE support_col= %s """ % (sI))
                    oC = otherC.getFirstItem()
                    if oC[0]:
                        oC = oC[0]+sC
                        otherC.execute(""" UPDATE support SET occurrences=%s WHERE support_col=%s """ % (str(oC), sI))
                    else:
                        oC = sC
                        otherC.execute(""" INSERT INTO support (support_col, occurrences) VALUES (%s, %s) """ % (sI, str(oC)))
            #add other fields
            for row in rows:
                if not otherC.rowIsIn(row, ("wordSense_col", "pattern_type", "support_col", "feature_col", "sentence_col")): #check to see if the row is already in patterns table
                    #print("trying to add stuff...")
                    otherC.execute(""" INSERT OR IGNORE INTO wordSenses (id_col) VALUES (%s) """ % row[0])
                    otherC.execute(""" INSERT OR IGNORE INTO textualPattern (pattern_type) VALUES (%s) """ % row[1])
                    otherC.execute(""" INSERT OR IGNORE INTO feature (feature_col) VALUES (%s) """ % row[3])
                    otherC.execute(""" INSERT OR IGNORE INTO sentence (sentence_col) VALUES (%s) """ % row[4])
                    otherC.execute(""" INSERT OR IGNORE INTO patterns (wordSense_col, pattern_type, support_col, feature_col, sentence_col) VALUES (%s, %s, %s, %s, %s) """ % tuple(row) )
    def deleteRowsBasedOnUI(self, tP, sI=None):
        if sI:
            self.execute(""" DELETE FROM patterns WHERE pattern_type="%s" and support_col="%s" """ % (tP, sI))
        else:
            self.execute(""" DELETE FROM patterns WHERE pattern_type="%s" """ % (tP))
        #wordSenses
        self.execute(""" SELECT id_col FROM wordSenses""")
        for item in self.getAllItems():
            self.execute(""" SELECT * FROM patterns WHERE wordSense_col=%s """ % (item))
            if not self.getAllItems():
                self.execute(""" DELETE FROM wordSenses WHERE id_col=%s """ % (item))
        #textualPattern
        self.execute(""" SELECT pattern_type FROM textualPattern""")
        for item in self.getAllItems():
            self.execute(""" SELECT * FROM patterns WHERE pattern_type="%s" """ % (item))
            if not self.getAllItems():
                self.execute(""" DELETE FROM textualPattern WHERE pattern_type="%s" """ % (item))
        #support
        self.execute(""" SELECT support_col FROM support""")
        for item in self.getAllItems():
            self.execute(""" SELECT * FROM patterns WHERE support_col="%s" """ % (item))
            if not self.getAllItems():
                self.execute(""" DELETE FROM support WHERE support_col="%s" """ % (item))
        #feature
        self.execute(""" SELECT feature_col FROM feature""")
        for item in self.getAllItems():
            self.execute(""" SELECT * FROM patterns WHERE feature_col="%s" """ % (item))
            if not self.getAllItems():
                self.execute(""" DELETE FROM feature WHERE feature_col="%s" """ % (item))
        #sentence
        self.execute(""" SELECT sentence_col FROM sentence""")
        for item in self.getAllItems():
            self.execute(""" SELECT * FROM patterns WHERE sentence_col="%s" """ % (item))
            if not self.getAllItems():
                self.execute(""" DELETE FROM sentence WHERE sentence_col="%s" """ % (item))
    def deleteNecessaryRows(self, otherC):
        #import pdb ; pdb.set_trace()
        #whatever WS-TP-Support rows are in self -- delete those corresponding items in otherC
        self.execute(""" SELECT * FROM deleteWSTPSupport """)
        for row in self.getRows():
            otherC.execute(""" DELETE FROM patterns WHERE wordSense_col=%s and pattern_type="%s" and support_col="%s" """ % tuple(row))
    def findIfThereAnotherSentenceWithSupport(self, sI, sentence):
        self.execute(r'select sentence_col from patterns where support_col="%s" ' % (sI))
        for retrievedSentence in self.getAllItems():
            if retrievedSentence != sentence:
                return True
        return False
    def removeItemsNotBeingUsed(self):
        #textualPattern
        self.execute("""SELECT pattern_type FROM textualPattern""")
        tPs = self.getAllItems()
        for tP in tPs:
            self.execute("""SELECT * FROM patterns WHERE pattern_type="%s" """ % tP)
            if not self.queryProducedAResponse():
                self.execute("""DELETE FROM textualPattern WHERE pattern_type="%s" """ % tP)
        if random.choice([1]):
            #wordSenses
            self.execute("""SELECT id_col FROM wordSenses""")
            wSs = self.getAllItems()
            for wS in wSs:
                self.execute(""" SELECT * FROM patterns WHERE wordSense_col=%s """ % wS)
                if not self.queryProducedAResponse():
                    self.execute(""" DELETE FROM wordSenses WHERE id_col=%s """ % wS)
            #support
            self.execute("SELECT support_col FROM support")
            sIs = self.getAllItems()
            for sI in sIs:
                self.execute(""" SELECT * FROM patterns WHERE support_col="%s" """ % sI)
                if not self.queryProducedAResponse():
                    self.execute(""" DELETE FROM support WHERE support_col="%s" """ % sI)
            #features
            self.execute("SELECT feature_col FROM feature")
            features = self.getAllItems()
            for feature in features:
                self.execute(""" SELECT * FROM patterns WHERE feature_col="%s" """ % feature)
                if not self.queryProducedAResponse():
                    self.execute(""" DELETE FROM feature WHERE feature_col="%s" """ % feature)
            #sentence
            self.execute("SELECT sentence_col FROM sentence")
            sentences = self.getAllItems()
            for sentence in sentences:
                self.execute(""" SELECT pattern_type, support_col, sentence_col FROM patterns WHERE sentence_col="%s" """ % sentence)
                if not self.queryProducedAResponse():
                    self.execute(""" DELETE FROM sentence WHERE sentence_col="%s" """ % sentence)
            #remove duplicate tuples
            self.execute(""" SELECT * FROM patterns """)
            rows = self.getRows()
            uniqueRows = ["foobar"]
            for row in rows:
                for uRow in uniqueRows:
                    if self.checkIfTwoRowsShareTPSISentence(row, uRow):
                        self.execute(""" DELETE FROM patterns WHERE id_col="%s" """ % (row[0]))
                        break
                if not self.checkIfTwoRowsShareTPSISentence(uniqueRows[-1:][0], row):
                    uniqueRows.append(row)
    def printDB(self):
        print("--------------------Database Print Out--------------------")
        print("Statistics: ")
        self.execute(""" SELECT url_col FROM urlsProcessed """)
        print("\tURLs Processed: %s" % len(self.getAllItems()))
        self.execute("select * from patterns")
        print("\tpatterns row count: %s" % len(self.getRows()))
        self.execute("select * from textualPattern")
        print("\ttextualPatterns count: %s" % len(self.getRows()))
        self.execute("select * from wordSenses")
        print("\twordSense count: %s" % len(self.getRows()))
        self.execute("select * from support")
        print("\tsupport count: %s" % len(self.getRows()))
        self.execute(" select occurrences from support ")
        oCTotal = 0
        for oC in self.getAllItems():
            oCTotal += oC
        print("\tsupport total occurrence count: %s" % (oCTotal))
        self.execute("select distinct occurrences from support")
        x = self.getAllItems()
        if x:
            median=sorted(x)[len(x)/2]
        else:
            median = 0
        print("\tmedian support occurrence (distinct occurrence counts used): %s" % (str(median)))
        self.execute("select * from feature")
        print("\tfeature count: %s" % len(self.getRows()))
        self.execute("select * from sentence")
        print("\tsentence count: %s" % len(self.getRows()))
        print("")
        #########################
        tPsWithSameWordSense = self.getTPsWithSameWordSense(removeSingleEntries=False, includeWordSense=True)  #ex. [ [ws, tp1, tp1, t2, t2], [ws, t6, t7] ... ]
        if not tPsWithSameWordSense:
            print("No wordSenses assigned---")
            print("tP\t|\tsI\t|\toC\t|\tSentence")
            print("")
            for tP in self.getTPs():
                supportOCAndSentences = self.getListOfSupportOCAndSentences(tP, wordSense=None) #ex. [ [sI, oC, sentence], ... ]
                for supportOCAndSentence in supportOCAndSentences:
                    print("%s | %s | %s | %s " % (tP, supportOCAndSentence[0], supportOCAndSentence[1], supportOCAndSentence[2]) )
                print("")
        else:
            print("wS:\ttP\t|\tsI\t|\toC\t|\tSentence")
            print("")
            for tPsOfAWordSense in tPsWithSameWordSense: #ex. [ws, tp1, tp1, t2, t2]
                manyOccurrences = False
                wordSense = tPsOfAWordSense[0]
                for tP in tPsOfAWordSense[1:]:
                    supportOCAndSentences = self.getListOfSupportOCAndSentences(tP, wordSense) #ex. [ [sI, oC, sentence], ... ]
                    for supportOCAndSentence in supportOCAndSentences:
                        if (int(supportOCAndSentence[1]) > 1) and self.findIfThereAnotherSentenceWithSupport(supportOCAndSentence[0], supportOCAndSentence[2]):
                            manyOccurrences = True
                            break
                    if manyOccurrences:
                        break
                if manyOccurrences:
                    print("wS " + str(wordSense) + ":")
                    for tP in tPsOfAWordSense[1:]:
                        supportOCAndSentences = self.getListOfSupportOCAndSentences(tP, wordSense) #ex. [ [sI, oC, sentence], ... ]
                        for supportOCAndSentence in supportOCAndSentences:
                                print("\t%s | %s | %s | %s " % (tP, supportOCAndSentence[0], supportOCAndSentence[1], supportOCAndSentence[2]) )
                        print("")
        print("----------------------------------------------------------")
    def printFullDB(self):
        print("--------------------Database Print Out--------------------")
        print("Statistics: ")
        self.execute(""" SELECT url_col FROM urlsProcessed """)
        print("\tURLs Processed: %s" % len(self.getAllItems()))
        self.execute("select * from patterns")
        print("\tpatterns row count: %s" % len(self.getRows()))
        self.execute("select * from textualPattern")
        print("\ttextualPatterns count: %s" % len(self.getRows()))
        self.execute("select * from wordSenses")
        print("\twordSense count: %s" % len(self.getRows()))
        self.execute("select * from support")
        print("\tsupport count: %s" % len(self.getRows()))
        self.execute(" select occurrences from support ")
        oCTotal = 0
        for oC in self.getAllItems():
            oCTotal += oC
        print("\tsupport total occurrence count: %s" % (oCTotal))
        self.execute("select distinct occurrences from support")
        x = self.getAllItems()
        if x:
            median=sorted(x)[len(x)/2]
        else:
            median = 0
        print("\tmedian support occurrence (distinct occurrence counts used): %s" % (str(median)))
        self.execute("select * from feature")
        print("\tfeature count: %s" % len(self.getRows()))
        self.execute("select * from sentence")
        print("\tsentence count: %s" % len(self.getRows()))
        print("")
        #########################
        tPsWithSameWordSense = self.getTPsWithSameWordSense(removeSingleEntries=False, includeWordSense=True)  #ex. [ [ws, tp1, tp1, t2, t2], [ws, t6, t7] ... ]
        if not tPsWithSameWordSense:
            print("No wordSenses assigned---")
            print("tP\t|\tsI\t|\toC\t|\tSentence")
            print("")
            for tP in self.getTPs():
                supportOCAndSentences = self.getListOfSupportOCAndSentences(tP, wordSense=None) #ex. [ [sI, oC, sentence], ... ]
                for supportOCAndSentence in supportOCAndSentences:
                    print("%s | %s | %s | %s " % (tP, supportOCAndSentence[0], supportOCAndSentence[1], supportOCAndSentence[2]) )
                print("")
        else:
            print("wS:\ttP\t|\tsI\t|\toC\t|\tSentence")
            print("")
            for tPsOfAWordSense in tPsWithSameWordSense: #ex. [ws, tp1, tp1, t2, t2]
                wordSense = tPsOfAWordSense[0]
                print("wS " + str(wordSense) + ":")
                for tP in tPsOfAWordSense[1:]:
                    supportOCAndSentences = self.getListOfSupportOCAndSentences(tP, wordSense) #ex. [ [sI, oC, sentence], ... ]
                    for supportOCAndSentence in supportOCAndSentences:
                        print("\t%s | %s | %s | %s " % (tP, supportOCAndSentence[0], supportOCAndSentence[1], supportOCAndSentence[2]) )
                print("")
        print("----------------------------------------------------------")

if __name__ == "__main__":
    pass