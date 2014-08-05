import extractRelationsNLTKCorpus, evalInputOne, mln2experimentOne, evalInputZero, mln2experimentZero, mln2experimentTwo, shutil, pickle, time, urllib2, sqlite3, sys
from derivedClasses import *
import sentences
import createInitialDatabase
#import createTaxonomy

oldUrls = ['http://en.wikipedia.org/wiki/Alberta', 'http://en.wikipedia.org/wiki/Edmonton', 'http://en.wikipedia.org/wiki/Canada', 'http://en.wikipedia.org/wiki/Alexander_Cameron_Rutherford',
        'http://en.wikipedia.org/wiki/Public_university', 'http://en.wikipedia.org/wiki/Students%27_unions', 'http://en.wikipedia.org/wiki/Student_activity_centre',
        'http://en.wikipedia.org/wiki/Higher_education_in_Alberta', 'http://en.wikipedia.org/wiki/Higher_education_in_Canada', 'http://en.wikipedia.org/wiki/Graduate_school',
        'http://en.wikipedia.org/wiki/Alberta_Eugenics_Board', 'http://en.wikipedia.org/wiki/Percy_Erskine_Nobbs', 'http://en.wikipedia.org/wiki/Frank_Darling_%28architect%29',
        'http://en.wikipedia.org/wiki/University_of_Alberta']

def deleteInputTextFolderFiles():
    filelist = [ f for f in os.listdir(os.getcwd() + '/exemplar-master/inputText') ]
    for f in filelist:
        os.remove(os.getcwd() + '/exemplar-master/inputText/' + f)

def processMainLoopException(e, urls):
        print("ERROR processing " + str(urls) + " will restore taxonomyRelations.db to last successful iteration and continue with next URL.")
        #import pdb ; pdb.set_trace()
        print("--------")
        print(type(e))
        print(str(e.args))
        print("-------- ")
        if "backUpTaxonomy.db" in os.listdir(os.getcwd()):
            shutil.copyfile("backUpTaxonomy.db", "taxonomyRelations.db")
        else:
            print("no backUpTaxonomy.db to fall back on.")
        deleteInputTextFolderFiles()
        #say urls are bad
        addBadURLs(urls)
        #restart program because it's likely the database is locked
        print("---------------------restart program---------------------")
        time.sleep(5)
        python = sys.executable
        os.execl(python, python, * sys.argv)

def convertListToSentence(sent):
    sentence = r""
    for i, word in enumerate(sent):
        if i == (len(sent) - 2):
            sentence += word + r""
        elif (i == (len(sent) - 1)) and (sent.count(word) > 1):
            return sentence
        elif i == (len(sent) - 1):
            sentence += word + r""
        else:
            sentence += word + r" "
    return sentence

def getAmbigiousSentences():
    #url = sentence.  I left things "url" out of convenience.
    urls = pickle.load( open('ambigiousSentences.p', 'rb') )
    #urlLargeChunks = divideURLsInChunks(urls, int(len(urls)/2))
    #return urlLargeChunks[1]
    return urls

def divideURLsInChunks(urls, chunkSize):
    if chunkSize < 1:
        chunkSize = 1
    urlExemplarChunks = []
    for i, url in enumerate(urls):
        if (i % chunkSize) == 0:
            urlExemplarChunks.append([url])
        else:
            urlExemplarChunks[len(urlExemplarChunks)-1].append(url)
    return urlExemplarChunks

def removeURLsAlreadyProcessed(urls):
    conn = sqlite3.connect('taxonomyRelations.db')
    c = conn.cursor(cursor)
    c.execute("pragma foreign_keys = ON")
    for i, url in enumerate(urls):
        if c.uRLProcessed(url):
            urls[i] = ""
    urls = list(set(urls))
    try:
        urls.remove("")
    except:
        pass
    c.close()
    conn.commit()
    return urls

def addBadURLs(urls):
        badURLs = getBadURLs()
        badURLs += urls
        print("adding " + str(urls) + " to the bad wikipedia articles.")
        pickle.dump( badURLs, open('transportedBW' + str(random.randrange(100000)) + '.p', 'wb'))
        #subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < badWikipediaArticles.p ">" ' + 'transportedBW' + str(random.randrange(100000)) + '.p', shell=True)

def getBadURLs():
    try:
        #subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat badWikipediaArticlesOneOne.p > badWikipediaArticles.p', shell=True)
        badURLs = pickle.load( open('badWikipediaArticles.p', 'rb') )
    except:
        print("Error loading bad wikipedia urls.  Recreating bad urls list...")
        badURLs = []
        pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
    return badURLs

def removeBadAndAlreadyProcessedURLs(urls):
    badURLs = getBadURLs()
    for url in urls[:]:
        if url in badURLs:
            urls.remove(url)
    urls = removeURLsAlreadyProcessed(urls)
    return urls

def processBadWikipediaArticles(fileName):
    try:
        badURLsToBeAdded = pickle.load( open(fileName, 'rb') )
    except:
        print("Error loading " + fileName)
        badURLsToBeAdded = []
    try:
        badURLs = pickle.load( open('badWikipediaArticles.p', 'rb') )
    except:
        print("Error loading bad wikipedia urls.  Recreating bad urls list...")
        badURLs = []
        pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
    badURLs += badURLsToBeAdded
    badURLs = list(set(badURLs))
    pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))

def processTransportedTR(fileName):
    conn1 = sqlite3.connect(fileName)
    c1 = conn1.cursor(cursor)
    c1.execute("pragma foreign_keys = ON")
    conn2 = sqlite3.connect("taxonomyRelations.db")
    c2 = conn2.cursor(cursor)
    c2.execute("pragma foreign_keys = ON")
    ####
    c1.renameHighWordSensesToNextAvailableWordSenseOfOtherC(c2)
    c1.deleteNecessaryRows(c2)
    c1.copyOverEverything(c2)
    ####
    conn1.commit()
    c1.close()
    conn2.commit()
    c2.close()

def main():
    open("printOuts.txt", "w+").close()
    try:
        #initialize
        #print("getting most recent taxonomyRelations.db ...")
        #subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat taxonomyRelationsOneOne.db > taxonomyRelations.db', shell=True)
        extraURLs = None
        urls = None
        urls = getAmbigiousSentences()
        #import pdb ; pdb.set_trace()
        urls = removeBadAndAlreadyProcessedURLs(urls)
        print("working with " + str(len(urls)))
        urlExemplarChunks = divideURLsInChunks(urls, 5) #list of lists
        random.shuffle(urlExemplarChunks) #reduce chance of multiple clients processing exact same urls at same time
        extraURLs = []
    except Exception as e:
        processMainLoopException(e, [])
    try:
        for urls in urlExemplarChunks:
            urls = removeBadAndAlreadyProcessedURLs(urls)
            print("processing (" + str(len(urls + extraURLs)) + ") " + str(urls + extraURLs))
            enoughToWorkWith = extractRelationsNLTKCorpus.run(urls + extraURLs)
            #print("getting most recent taxonomyRelations.db ...")
            #subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat taxonomyRelationsOneOne.db > taxonomyRelations.db', shell=True)
            if not enoughToWorkWith:
                extraURLs += urls
            if enoughToWorkWith:
                #MLN1
                tPsThatChangeC2 = evalInputOne.run()
                #subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < transportedTR.db ">" ' + 'transportedTROneOne' + str(random.randrange(100000)) + '.db', shell=True)
                #os.remove(os.getcwd() + "/transportedTR.db")
                shutil.copyfile("taxonomyRelations.db", "backUpTaxonomy.db")
                extraURLs = []
                #time.sleep(60)
                #server
                for fileName in os.listdir(os.getcwd()):
                    if "transportedBW" in fileName:
                        print("processing " + fileName)
                        processBadWikipediaArticles(fileName)
                        os.remove(os.getcwd() + "/" + fileName)
                for fileName in os.listdir(os.getcwd()):
                    if "transportedTR" in fileName:
                        print("processing " + fileName)
                        processTransportedTR(fileName)
                        os.remove(os.getcwd() + "/" + fileName)
                print("removing unused items in database...")
                conn2 = sqlite3.connect("taxonomyRelations.db")
                c2 = conn2.cursor(cursor)
                c2.removeItemsNotBeingUsed()
                c2.close()
                conn2.commit()
                #MLN2
                moveOrMerge = True
                while moveOrMerge:
                    #time.sleep(60) #assumes the server will take no longer than 60 seconds to update/upload the database
                    #print("getting most recent taxonomyRelations.db ...")
                    #subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat taxonomyRelationsOneOne.db > taxonomyRelations.db', shell=True)
                    moveOrMerge = mln2experimentTwo.run(tPsThatChangeC2)
                    #subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < transportedTR.db ">" ' + 'transportedTROneOne' + str(random.randrange(100000)) + '.db', shell=True)
                    #os.remove(os.getcwd() + "/transportedTR.db")
                    for fileName in os.listdir(os.getcwd()):
                        if "transportedBW" in fileName:
                            print("processing " + fileName)
                            processBadWikipediaArticles(fileName)
                            os.remove(os.getcwd() + "/" + fileName)
                    for fileName in os.listdir(os.getcwd()):
                        if "transportedTR" in fileName:
                            print("processing " + fileName)
                            processTransportedTR(fileName)
                            os.remove(os.getcwd() + "/" + fileName)
                    print("removing unused items in database...")
                    conn2 = sqlite3.connect("taxonomyRelations.db")
                    c2 = conn2.cursor(cursor)
                    c2.removeItemsNotBeingUsed()
                    c2.close()
                    conn2.commit()
                time.sleep(2)
    except Exception as e:
        if extraURLs:
            processMainLoopException(e, extraURLs)
        elif urls:
            processMainLoopException(e, urls)
        else:
            processMainLoopException(e, [])
    #createTaxonomy.run()




if __name__ == "__main__":
    main()