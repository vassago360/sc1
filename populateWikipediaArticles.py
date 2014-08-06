import createInitialDatabase, extractRelations, evalInput, shutil, pickle, time, urllib2, sqlite3, sys
from derivedClasses import *
#import createTaxonomy

def processMainLoopException(e, urls):
        print("ERROR processing " + str(urls) + " will restore taxonomyRelations.db to last successful iteration and continue with next URL.")
        import pdb ; pdb.set_trace()
        print("--------")
        print(type(e))
        print(str(e.args))
        print("--------")
        shutil.copyfile("backUpTaxonomy.db", "taxonomyRelations.db")
        shutil.copyfile(os.getcwd() + '/exemplarOutput/backupSave.p', os.getcwd() + '/exemplarOutput/save.p')
        try:
            f = open('exceptions', 'r+')
        except:
            print("Error loading exceptions. recreating....")
            f = open('exceptions', 'w+')
        f.read()
        f.write('\n')
        f.write(str(urls))
        f.write(str(type(e)))
        f.write(str(e.args))
        f.write("-----------")
        f.close()
        time.sleep(5)

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
    return urls

def convertToList(wikipediaCategories):  #go from "djd|eee" to ["djd", "eee"]
    return re.split(r'\|', wikipediaCategories)

def reCombineWikipediaCategories(wikipediaCategories):
    wikipediaString = ""
    for wikipediaCategory in wikipediaCategories:
        wikipediaString += wikipediaCategory + "|"
    if len(wikipediaCategories) > 0:
        wikipediaString = wikipediaString[:-1]
    return wikipediaString

def getWikipediaArticles(wikipediaCategories):
    wikipediaCategoriesInChunks = divideURLsInChunks(convertToList(wikipediaCategories), 2) #list of lists
    for wikipediaCategoriesInChunk in wikipediaCategoriesInChunks:
        print("now processing " + str(wikipediaCategoriesInChunk))
        masterURL = "http://tools.wmflabs.org/erwin85/randomarticle.php?lang=en&family=wikipedia&categories=" + reCombineWikipediaCategories(wikipediaCategoriesInChunk) + "&namespaces=0&subcats=1&d=9"
        try:
            urls = pickle.load( open('wikipediaArticles.p', 'rb') )
        except:
            print("Error loading wikipedia urls.  Recreating urls list...")
            urls = []
            pickle.dump( urls, open('wikipediaArticles.p', 'wb'))
        lenURLs = []
        errorCount = 0
        for i in range(20000): #the expected maximum number of wikipedia articles (duplicates included) for that given request
            try:
                url = urllib2.urlopen(masterURL).geturl()
            except Exception as e:
                if errorCount > 100:
                    print(str(type(e)))
                    print('quiting this wikipedia chunk (first sleep for 90 seconds): ' + str(wikipediaCategoriesInChunk))
                    time.sleep(90)
                    break
                else:
                    print("error: " + str(type(e)))
                    time.sleep(errorCount)
                    errorCount += 1
                    continue
            errorCount = 0
            urls.append(str(url))
            for i, url in enumerate(urls):
                if ("http://en.wikipedia.org/wiki/List" in url) or (not ("http://en.wikipedia.org/wiki" in url)):
                    urls[i] = ""
            urls = list(set(urls))
            print("len(urls): " + str(len(urls)))
            lenURLs.append(len(urls))
            if (len(lenURLs) > 20) and (float(numpy.mean(lenURLs[-20:])) == float(len(urls))):
                break
            pickle.dump( urls, open('wikipediaArticlesCelebrities.p', 'wb'))
            if len(urls) > 660:
                return urls
            time.sleep(3)
    return urls

def main():
    open("printOuts.txt", "w+").close()
    open('exceptions', 'w+').close()
    wikipediaCategories = 'American_female_pop_singers|American_film_actresses|21st-century American actresses|American_dance_musicians|American_hip_hop_singers|21st-century_American_male_actors|American male pop singers|Forbes_lists'
    #wikipediaCategories = 'Visitor_attractions|Historic_districts|Places|Religious_places'
    #wikipediaCategories = 'Tools|Cutting_tools|Machines|Cooking|Kitchenware|Cooking_appliances|Domestic_implements'
    getWikipediaArticles(wikipediaCategories)




if __name__ == "__main__":
    main()