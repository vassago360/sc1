import createInitialDatabase, extractRelations, evalInput, mln2experiment, shutil, pickle, time, urllib2, sqlite3, sys
from derivedClasses import *
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
        try:
            print("getting most recent taxonomyRelations.db ...")
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat taxonomyRelations.db > taxonomyRelations.db', shell=True)
        except:
            print("error getting taxonomyRelations.db using backUpTaxonomy.db instead <<<<<< ")
            if "backUpTaxonomy.db" in os.listdir(os.getcwd()):
                shutil.copyfile("backUpTaxonomy.db", "taxonomyRelations.db")
            else:
                print("no backUpTaxonomy.db to fall back on.")
                import pdb ; pdb.set_trace()
        try:
            shutil.copyfile(os.getcwd() + '/exemplarOutput/backupSave.p', os.getcwd() + '/exemplarOutput/save.p')
        except IOError:
            #### delete everything in exemplarOutput folder
            folder = os.getcwd() + '/exemplarOutput'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception, e:
                    print e
            ####
        deleteInputTextFolderFiles()
        #say urls are bad
        addBadURLs(urls)
        #restart program because it's likely the database is locked
        print("---------------------restart program---------------------")
        time.sleep(5)
        python = sys.executable
        os.execl(python, python, * sys.argv)

def getWikipediaArticles():
    urls = pickle.load( open('wikipediaArticles.p', 'rb') ) + oldUrls
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
        pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
        subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < badWikipediaArticles.p ">" ' + 'transportedBW' + str(random.randrange(100000)) + '.p', shell=True)

def getBadURLs():
    try:
        subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat badWikipediaArticles.p > badWikipediaArticles.p', shell=True)
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

def main():
    open("printOuts.txt", "w+").close()
    try:
        extraURLs = None
        urls = None
        #initialize
        urls = getWikipediaArticles()
        urls = removeBadAndAlreadyProcessedURLs(urls)
        print("working with " + str(len(urls)))
        urlExemplarChunks = divideURLsInChunks(urls, 3) #list of lists
        random.shuffle(urlExemplarChunks) #reduce chance of multiple clients processing exact same urls at same time
        extraURLs = []
        for urls in urlExemplarChunks:
            urls = removeBadAndAlreadyProcessedURLs(urls)
            print("processing (" + str(len(urls + extraURLs)) + ") " + str(urls + extraURLs))
            enoughToWorkWith = extractRelations.run(urls + extraURLs)
            print("getting most recent taxonomyRelations.db ...")
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat taxonomyRelations.db > taxonomyRelations.db', shell=True)
            if not enoughToWorkWith:
                extraURLs += urls
            if enoughToWorkWith:
                #MLN1
                tPsThatChangeC2 = evalInput.run()
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < transportedTR.db ">" ' + 'transportedTR' + str(random.randrange(100000)) + '.db', shell=True)
                os.remove(os.getcwd() + "/transportedTR.db")
                shutil.copyfile("taxonomyRelations.db", "backUpTaxonomy.db")
                extraURLs = []
                time.sleep(80)
                #MLN2
                print("getting most recent taxonomyRelations.db ...")
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat taxonomyRelations.db > taxonomyRelations.db', shell=True)
                mln2experiment.run(tPsThatChangeC2)
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < transportedTR.db ">" ' + 'transportedTR' + str(random.randrange(100000)) + '.db', shell=True)
                os.remove(os.getcwd() + "/transportedTR.db")
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