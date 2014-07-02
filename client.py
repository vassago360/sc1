import createInitialDatabase, extractRelations, evalInput, mln2experiment, shutil, pickle, time, urllib2, sqlite3, sys
from derivedClasses import *
#import createTaxonomy

oldUrls = ['http://en.wikipedia.org/wiki/Alberta', 'http://en.wikipedia.org/wiki/Edmonton', 'http://en.wikipedia.org/wiki/Canada', 'http://en.wikipedia.org/wiki/Alexander_Cameron_Rutherford',
        'http://en.wikipedia.org/wiki/Public_university', 'http://en.wikipedia.org/wiki/Students%27_unions', 'http://en.wikipedia.org/wiki/Student_activity_centre',
        'http://en.wikipedia.org/wiki/Higher_education_in_Alberta', 'http://en.wikipedia.org/wiki/Higher_education_in_Canada', 'http://en.wikipedia.org/wiki/Graduate_school',
        'http://en.wikipedia.org/wiki/Alberta_Eugenics_Board', 'http://en.wikipedia.org/wiki/Percy_Erskine_Nobbs', 'http://en.wikipedia.org/wiki/Frank_Darling_%28architect%29',
        'http://en.wikipedia.org/wiki/University_of_Alberta']

def processMainLoopException(e, urls, urlExemplarChunks):
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
        try:
            f = open('exceptions', 'r+')
        except:
            print("Error loading exceptions. recreating....")
            f = open('exceptions', 'w+')
        import cleanUp
        f.read()
        f.write('\n')
        f.write(str(urls))
        f.write(str(type(e)))
        f.write(str(e.args))
        f.write("-----------")
        f.close()
        if 'database is locked' in str(e.args):
            urlExemplarChunks.append(urls) #try it again later
        else:
            try:
                badURLs = pickle.load( open('badWikipediaArticles.p', 'rb') )
            except:
                print("Error loading bad wikipedia urls.  Recreating bad urls list...")
                badURLs = []
                pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
            badURLs += urls
            print("adding " + str(urls) + " to the bad wikipedia articles.")
            pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
        #restart program because it's likely the database is locked
        print("---------------------restart program---------------------")
        time.sleep(10)
        python = sys.executable
        os.execl(python, python, * sys.argv)

def getWikipediaArticles():
    urls = pickle.load( open('wikipediaArticles.p', 'rb') ) + oldUrls
    urlLargeChunks = divideURLsInChunks(urls, int(len(urls)/11))
    return urlLargeChunks[0]

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
    """
    urls.remove('http://en.wikipedia.org/wiki/University_of_Wisconsin%E2%80%93Extension')
    urls.remove('http://en.wikipedia.org/wiki/University_of_North_Alabama')
    urls.remove('http://en.wikipedia.org/wiki/Texas_A%26M_University_System')
    urls.remove('http://en.wikipedia.org/wiki/Evanston_Township_High_School')
    urls.remove('http://en.wikipedia.org/wiki/University_of_St._Thomas_(Texas)')
    urls.remove('http://en.wikipedia.org/wiki/Lyndon_B._Johnson_School_of_Public_Affairs')
    urls.remove('http://en.wikipedia.org/wiki/University_of_North_Dakota')
    urls.remove('http://en.wikipedia.org/wiki/Hunter_College')
    urls.remove('http://en.wikipedia.org/wiki/Interpretive_discussion')
    urls.remove('http://en.wikipedia.org/wiki/Kod%C3%A1ly_Method')
    urls.remove('http://en.wikipedia.org/wiki/Challenge-Based_Learning')
    urls.remove('http://en.wikipedia.org/wiki/University_of_Florida')
    urls.remove('http://en.wikipedia.org/wiki/Air_University_(United_States_Air_Force)')
    urls.remove('http://en.wikipedia.org/wiki/Jefferson_Davis_Community_College')"""

    c.close()
    conn.commit()
    return urls

def getBadURLs():
    try:
        badURLs = pickle.load( open('badWikipediaArticles.p', 'rb') )
    except:
        print("Error loading bad wikipedia urls.  Recreating bad urls list...")
        badURLs = []
        pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
    return badURLs

def removeBadURLs(urls):
    badURLs = getBadURLs()
    for i, url in enumerate(urls):
        if url in badURLs:
            urls[i] = ""
    urls = removeURLsAlreadyProcessed(urls)
    return urls

def main():
    open("printOuts.txt", "w+").close()
    open('exceptions', 'w+').close()
    try:
        print("getting most recent taxonomyRelations.db ...")
        subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat taxonomyRelations.db > taxonomyRelations.db', shell=True)
        urls = getWikipediaArticles()
        urls = removeBadURLs(urls)
        print("working with " + str(len(urls)))
        urlExemplarChunks = divideURLsInChunks(urls, 4) #list of lists
        extraURLs = []
        for urls in urlExemplarChunks:
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
                time.sleep(60)
    except Exception as e:
        if urls and urlExemplarChunks and extraURLs:
            processMainLoopException(e, urls, urlExemplarChunks)
        elif urls and urlExemplarChunks:
            processMainLoopException(e, urls, urlExemplarChunks)
        elif urls:
            processMainLoopException(e, urls, [])
        else:
            processMainLoopException(e, [], [])
    #createTaxonomy.run()




if __name__ == "__main__":
    main()