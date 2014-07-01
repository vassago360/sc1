#runs explemar -> exemplar output ->
#use sentences exemplar thought was interesting (nothing else) and use that as input for stanford parser ->
#run functions that updates SQL database -> print SQL database

from derivedClasses import *

def outputExemplarSentences(exemplarRelationInfo):
    f = open("exemplarSentencesOutput.txt", "w+")
    for relationTuple in exemplarRelationInfo:
        f.write(relationTuple[3] + " \n")
    f.close()

def sqlStatementCount(sqlCursor):
    count = 0
    for row in sqlCursor:
        count += 1
    return count

def replaceSpaceWithPlus(s): #replace spaces with pluses (alchemy requires no spaces in the constants)
    sNew = ""
    for i in range(len(s)):
        if s[i] == " ":
            sNew += "+"
        else:
            sNew += s[i]
    return sNew

def createDB(fileName):
        print("Creating " + fileName + "...")
        open(fileName, 'w+').close()
        conn = sqlite3.connect(fileName)
        c = conn.cursor(cursor)
        c.execute("pragma foreign_keys = ON")
        c.execute("""CREATE TABLE textualPattern(
            pattern_type TEXT PRIMARY KEY NOT NULL
        )""")
        c.execute("""CREATE TABLE wordSenses(
            id_col INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
            ) """)
        c.execute("""CREATE TABLE support(
            support_col TEXT PRIMARY KEY NOT NULL,
            occurrences INTEGER
        )""")
        c.execute("""CREATE TABLE feature(
            feature_col TEXT PRIMARY KEY NOT NULL
        )""")
        c.execute("""CREATE TABLE sentence(
            sentence_col TEXT PRIMARY KEY NOT NULL
        )""")
        c.execute("""CREATE TABLE patterns(
            id_col INTEGER PRIMARY KEY AUTOINCREMENT,
            wordSense_col INTEGER,
            pattern_type TEXT,
            support_col TEXT,
            feature_col TEXT,
            sentence_col TEXT,
            FOREIGN KEY(wordSense_col) REFERENCES wordSenses(id_col) ON DELETE CASCADE,
            FOREIGN KEY(pattern_type) REFERENCES textualPattern(pattern_type) ON DELETE CASCADE,
            FOREIGN KEY(support_col) REFERENCES support(support_col) ON DELETE CASCADE,
            FOREIGN KEY(feature_col) REFERENCES feature(feature_col) ON DELETE CASCADE,
            FOREIGN KEY(sentence_col) REFERENCES sentence(sentence_col) ON DELETE CASCADE
        )""")
        c.execute(""" CREATE TABLE urlsProcessed (
            url_col TEXT PRIMARY KEY NOT NULL
        )""")
        c.execute(""" CREATE TABLE deleteWSTPSupport(
            wordSense_col INTEGER,
            pattern_type TEXT,
            support_col TEXT,
            FOREIGN KEY(wordSense_col) REFERENCES wordSenses(id_col) ON DELETE CASCADE,
            FOREIGN KEY(pattern_type) REFERENCES textualPattern(pattern_type) ON DELETE CASCADE,
            FOREIGN KEY(support_col) REFERENCES support(support_col) ON DELETE CASCADE
        )""")
        # return the sqlite connection and cursor
        return conn, c

def updateSQLRelationsDB(c, patternTuples, typeOfUpdate):
    #adding patternTuples to SQL database.  it is possible a primary key could already exists.
    for patternTuple in patternTuples:
        if typeOfUpdate == "exemplarRelationInfo":
            c.execute("""insert or ignore into textualPattern values ("%s")""" % (replaceSpaceWithPlus(patternTuple[0])))
            c.execute("""INSERT OR REPLACE INTO support
            VALUES ("%s",
              COALESCE(
                (SELECT occurrences FROM support
                   WHERE support_col="%s"),
                0) + 1);""" % (replaceSpaceWithPlus(patternTuple[1]), replaceSpaceWithPlus(patternTuple[1])))
            c.execute("""insert or ignore into sentence values ("%s")""" % (replaceSpaceWithPlus(patternTuple[3])))
            #c.execute("""SELECT * FROM patterns WHERE pattern_type="%s" AND support_col="%s" AND sentence_col="%s" """ % (replaceSpaceWithPlus(patternTuple[0]), replaceSpaceWithPlus(patternTuple[1]), replaceSpaceWithPlus(patternTuple[3])))
            #if not sqlStatementCount(c):
                #c.execute("""insert or ignore into patterns (pattern_type, support_col, feature_col, sentence_col) values ("%s", "%s", NULL, "%s")""" % (replaceSpaceWithPlus(patternTuple[0]), replaceSpaceWithPlus(patternTuple[1]), replaceSpaceWithPlus(patternTuple[3])))
        if typeOfUpdate == "features": #ex. [(textualPattern, supportItem, feature, sentence), ...
            c.execute("""insert or ignore into textualPattern values ("%s")""" % (replaceSpaceWithPlus(patternTuple[0])))
            c.execute("""insert or ignore into feature values ("%s")""" % (replaceSpaceWithPlus(patternTuple[2])))
            c.execute("""SELECT * FROM patterns WHERE pattern_type="%s" AND feature_col="%s" AND sentence_col="%s" """ % (replaceSpaceWithPlus(patternTuple[0]), replaceSpaceWithPlus(patternTuple[2]), replaceSpaceWithPlus(patternTuple[3])))
            if not sqlStatementCount(c):
                c.execute("""insert or ignore into patterns (pattern_type, support_col, feature_col, sentence_col) values ("%s", "%s", "%s", "%s")""" % (replaceSpaceWithPlus(patternTuple[0]), replaceSpaceWithPlus(patternTuple[1]), replaceSpaceWithPlus(patternTuple[2]), replaceSpaceWithPlus(patternTuple[3])))

def loadExemplarDict():
    try:
        exemplarDict = pickle.load( open( os.getcwd() + '/exemplarOutput/save.p', 'rb') )
    except:
        print("ERROR: recreating exemplarOutputPickle...")
        exemplarDict = dict()
        pickle.dump( exemplarDict, open( os.getcwd() + '/exemplarOutput/save.p', "wb" ) )
    return exemplarDict

def saveExemplarDict(exemplarDict, url):
    highestVal = 0
    fileNames = os.listdir(os.getcwd() + '/exemplarOutput')
    for fileName in fileNames:
        if 'exemplarOutput' in fileName:
            val = int(re.split(r'_', fileName)[1])
            if val > highestVal:
                highestVal = val
    newFileName = os.getcwd() + '/exemplarOutput/exemplarOutput_' + str(highestVal + 1)
    shutil.copyfile("exemplarOutput.txt", newFileName)
    exemplarDict[url] = newFileName
    pickle.dump( exemplarDict, open( os.getcwd() + '/exemplarOutput/save.p', "wb" ) )

def deleteInputTextFolderFiles():
    filelist = [ f for f in os.listdir(os.getcwd() + '/exemplar-master/inputText') ]
    for f in filelist:
        os.remove(os.getcwd() + '/exemplar-master/inputText/' + f)

def inputTextFolderHasFiles():
    if len(os.listdir(os.getcwd() + '/exemplar-master/inputText')) > 0:
        return True
    else:
        return False

def removeLongSentences(text):
    for sentence in re.split(r'\.', text):
        parsedSentence = nltk.word_tokenize(sentence)
        if len(parsedSentence) > 100:
            text = text.replace(sentence + ".", "")
    return text

def getExemplarRelations(urls):
    #It does whatever it needs to do to store the relations in exemplarOutput.txt
    f = open('exemplarOutput.txt', 'w+')
    f.write('Subjects\tRelation\tObjects\tNormalized Relation\tSentence\n')
    for count, url in enumerate(urls):
        if url == "wikiUofA.txt":
            f1 = open("wikiUofA.txt", "r+")
            f2 = open(os.getcwd() + '/exemplar-master/inputText/inputText_' + str(count) + '.txt', 'w+')
            f2.write(f1.read())
            f2.close()
            f1.close()
        else:
            #get and preprocess url text ( takes 3 mins :( )
            extractedText = boilerpipe.extract.Extractor(extractor='ArticleExtractor', url=url)
            extractedText = extractedText.getText()
            extractedText = extractedText.encode('unicode_escape')
            extractedText = re.sub(r"""(\\[0a-z1-9]*)|(\[[0a-z1-9]{0,20}\])""", '', extractedText)
            extractedText = extractedText.replace('\\', '')
            extractedText = extractedText.replace('/', '')
            extractedText = removeLongSentences(extractedText)
            f2 = open(os.getcwd() + '/exemplar-master/inputText/inputText_' + str(count) + '.txt', 'w+')
            f2.write(extractedText)
            f2.close()
    if inputTextFolderHasFiles():
        #extract relations and features
        print("using Exemplar for relation extraction...")
        osCwd = os.getcwd()
        os.chdir(os.getcwd() + "/exemplar-master")
        subprocess.call(r'./exemplar.sh stanford inputText exemplarTempOutput.txt > exemplarTerminalOutput.txt', shell=True)
        f2 = open("exemplarTempOutput.txt", "r+")
        for i, line in enumerate(f2):
            if i != 0:
                f.write(line)
        f2.close()
        os.chdir(osCwd)
        deleteInputTextFolderFiles()
    f.close()

def getWSDistinctCount(tPLists):
    #ex. tPLists = [ [ws1, tp1], [ws1, tp2], [ws2, t6], [ws2, t7] ... ]
    wordSenses = []
    for tPList in tPLists:
        wordSenses.append(tPList[0])
    return len(set(wordSenses))

def enoughURLsToWorkWith(urls, exemplarRelationInfo):
    if "backUpTaxonomy.db" in os.listdir(os.getcwd()): #an indication that taxonomy formation is running for the first time
        conn1 = sqlite3.connect('inputRelations.db')
        c1 = conn1.cursor(cursor)
        c1.execute("pragma foreign_keys = ON")
        conn2 = sqlite3.connect('taxonomyRelations.db')
        c2 = conn2.cursor(cursor)
        c2.execute("pragma foreign_keys = ON")
        tPListsWithSameVerb = c2.getTPsWithSameVerbButNothingElseAsWhatsInTheOtherDB(c1, includeWordSense=True, otherCHasWordSenses=False)
        tPListsWithSameTP = c2.getTPsWithSameTPButNothingElse(c1, includeWordSense=True, otherCHasWordSenses=False)
        distinctZeugmaReductionSituations = getWSDistinctCount(tPListsWithSameVerb + tPListsWithSameTP)
        conn1.commit()
        c1.close()
        conn2.commit()
        c2.close()
        if distinctZeugmaReductionSituations > 300:
            print("distinctZeugmaReductionSituations > 300")
            import pdb ; pdb.set_trace()
        if (distinctZeugmaReductionSituations >= 5) or (len(urls) > 2): #important during evalInput.  We want a consistant amount of wordSenses that a tP will be compared to (a parameter of the program so-to-speak)
            print("enough urls to work with.  there are " + str(distinctZeugmaReductionSituations) + " tps  in a zeugma/reduction situation.  But " + str(len(exemplarRelationInfo)) +  " extracted relations." )
            return True
        else:
            print("not enough urls to work with.  only " + str(distinctZeugmaReductionSituations) + " tps  in a zeugma/reduction situation.  But " + str(len(exemplarRelationInfo)) +  " extracted relations." )
            return False
    else:
        return True

def run(urls, checkIfURLsHaveAlreadyBeenProcessed=True): #urls = [url1, url2... #return False if nothing was extracted, otherwise return True
    #check first to make sure the url hasn't already been processed (if it has we can skip it)
    conn = sqlite3.connect('taxonomyRelations.db')
    c = conn.cursor(cursor)
    c.execute("pragma foreign_keys = ON")
    if checkIfURLsHaveAlreadyBeenProcessed:
        for i, url in enumerate(urls):
            if not c.uRLProcessed(url):
                break               #url has not been processed
            if (i == len(urls)-1) and c.uRLProcessed(url):
                return False    #all urls have already been processed
    #process urls
    conn, c = createDB("inputRelations.db")
    for url in urls:
        c.addURL(url)
    conn.commit()
    c.close()
    #extract relations
    getExemplarRelations(urls)
    exemplarRelationInfo = exemplarExtract.getInfo()  #list of tuples ex. [(textualPattern, supportItem, relation, sentence1), (textualPattern, supportItem, relation, sentence2), ...
    outputExemplarSentences(exemplarRelationInfo)
    #extract features
    print("using Stanford Parser for feature extraction...")
    subprocess.call(r"./stanford-parser-full-2014-01-04/lexparser.sh exemplarSentencesOutput.txt > stanfordParserOutput.txt", shell=True)
    #extract conjunction feature
    stanfordPOSFeatures = stanfordPOS.getFeatures(exemplarRelationInfo, "stanfordParserOutput.txt") #list of tuples ex. [(textualPattern, supportItem, feature, sentence), ...
    stanfordDepenFeatures = stanfordDepen.getFeatures(exemplarRelationInfo, "stanfordParserOutput.txt") #list of tuples ex. [(textualPattern, supportItem, feature, sentence), ...
    #extract NE features
    subprocess.call(r'cp exemplarSentencesOutput.txt figer-master/data', shell=True)
    cwd = os.getcwd()
    os.chdir(cwd + '/figer-master')
    subprocess.call(r'./run.sh "config/figer.conf" > figer.log', shell=True)
    os.chdir(cwd)
    figerNERFeatures = figerNER.getFeatures(exemplarRelationInfo, "figer-master/data/exemplarSentencesOutput.out") #list of tuples ex. [(textualPattern, supportItem, feature, sentence), ...
    #Save DB
    conn = sqlite3.connect('inputRelations.db')
    c = conn.cursor(cursor)
    c.execute("pragma foreign_keys = ON")
    updateSQLRelationsDB(c, exemplarRelationInfo, "exemplarRelationInfo")
    updateSQLRelationsDB(c, stanfordPOSFeatures, "features")
    updateSQLRelationsDB(c, stanfordDepenFeatures, "features")
    updateSQLRelationsDB(c, figerNERFeatures, "features")
    conn.commit()
    c.close()
    #check if there will be enough reduction and zeugma situations to do evaluations-- len(tPsWithSameVerb + tPsWithSameTP) = 10  or len(urls) > 10
    return enoughURLsToWorkWith(urls, exemplarRelationInfo)

if __name__ == "__main__":
    pass










