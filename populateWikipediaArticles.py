import createInitialDatabase, extractRelations, evalInput, shutil, pickle, time, urllib2, sqlite3, sys
from derivedClasses import *
#import createTaxonomy

oldUrls = ['http://en.wikipedia.org/wiki/Alberta', 'http://en.wikipedia.org/wiki/Edmonton', 'http://en.wikipedia.org/wiki/Canada', 'http://en.wikipedia.org/wiki/Alexander_Cameron_Rutherford',
        'http://en.wikipedia.org/wiki/Public_university', 'http://en.wikipedia.org/wiki/Students%27_unions', 'http://en.wikipedia.org/wiki/Student_activity_centre',
        'http://en.wikipedia.org/wiki/Higher_education_in_Alberta', 'http://en.wikipedia.org/wiki/Higher_education_in_Canada', 'http://en.wikipedia.org/wiki/Graduate_school',
        'http://en.wikipedia.org/wiki/Alberta_Eugenics_Board', 'http://en.wikipedia.org/wiki/Percy_Erskine_Nobbs', 'http://en.wikipedia.org/wiki/Frank_Darling_%28architect%29',
        'http://en.wikipedia.org/wiki/University_of_Alberta']

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
            if (len(lenURLs) > 30) and (float(numpy.mean(lenURLs[-30:])) == float(len(urls))):
                break
            pickle.dump( urls, open('wikipediaArticles.p', 'wb'))
            time.sleep(3)
    return urls

def main():
    open("printOuts.txt", "w+").close()
    open('exceptions', 'w+').close()
    wikipediaCategories = "Academic_journals|Technical_communication|Academic_publishing|Education|Knowledge_sharing|Philosophy_of_education|History_of_education|Types_of_university_or_college|Public_universities|Education_portals|Academic_conferences|Academia|Conferences|University_of_Alberta|Consortium_for_North_American_Higher_Education_Collaboration|Education_in_Edmonton|Public_universities_in_Texas|Association_of_American_Universities|Association_of_Public_and_Land-Grant_Universities|Universities_and_colleges_in_Austin,_Texas|Educational_institutions_established_in_1883|Oak_Ridge_Associated_Universities|Universities_and_colleges_accredited_by_the_Southern_Association_of_Colleges_and_Schools|Flagship_universities_in_the_United_States|Public_universities_in_the_United_States|Educational_stages|Academic_institutions|Higher_education|Public_universities_and_colleges_in_the_United_States|Universities_and_colleges|Community_colleges_in_the_United_States|Bachelor_of_Education|Course_(education)|Curricula|Learning_standards|Academic_disciplines"
    getWikipediaArticles(wikipediaCategories) + oldUrls




if __name__ == "__main__":
    main()