from derivedClasses import *
import createInitialDatabase

def processMainLoopException(e):
        print("ERROR with server")
        print(" -------- ")
        print(type(e))
        print(str(e.args))
        print(" -------- ")
        if "backUpTaxonomy.db" in os.listdir(os.getcwd()):
            shutil.copyfile("backUpTaxonomy.db", "taxonomyRelations.db")
        else:
            print("no backUpTaxonomy.db to fall back on.")
        time.sleep(2)
        print("---------------------restart program---------------------")
        if 'database is locked' in str(e.args):
            for fileName in os.listdir(os.getcwd()):
                if "db-journal" in fileName:
                    os.remove(os.getcwd() + "/" + fileName)
        else:
            for fileName in os.listdir(os.getcwd()):
                if "transportedTR" in fileName:
                    os.remove(os.getcwd() + "/" + fileName)
        python = sys.executable
        os.execl(python, python, * sys.argv)

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

def uploadBadWikipediaArticles():
    try:
        badURLs = pickle.load( open('badWikipediaArticles.p', 'rb') )
    except:
        print("Error loading bad wikipedia urls.  Recreating bad urls list...")
        badURLs = []
        pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
    subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < badWikipediaArticles.p ">" badWikipediaArticles1.p  ', shell=True)
    subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm badWikipediaArticles.p  ', shell=True)
    subprocess.call(r'ssh st1298@eros.cs.txstate.edu mv badWikipediaArticles1.p badWikipediaArticles.p ', shell=True)

def main():
    #createInitialDatabase.run()
    #badURLs = []
    #pickle.dump( badURLs, open('badWikipediaArticles.p', 'wb'))
    #import pdb ; pdb.set_trace()
    uploadBadWikipediaArticles()
    try:
        while(True):
            #process badURLs
            subprocess.call(r'scp st1298@eros.cs.txstate.edu:transportedBW*.p ./ ', shell=True)
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm transportedBW*.p  ', shell=True)
            processedSomething = False
            for fileName in os.listdir(os.getcwd()):
                if "transportedBW" in fileName:
                    print("processing " + fileName)
                    processedSomething = True
                    processBadWikipediaArticles(fileName)
                    os.remove(os.getcwd() + "/" + fileName)
            if processedSomething:
                    subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < badWikipediaArticles.p ">" badWikipediaArticles1.p  ', shell=True)
                    subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm badWikipediaArticles.p  ', shell=True)
                    subprocess.call(r'ssh st1298@eros.cs.txstate.edu mv badWikipediaArticles1.p badWikipediaArticles.p ', shell=True)
            #process transportedTR*.db
            subprocess.call(r'scp st1298@eros.cs.txstate.edu:transportedTR*.db ./ ', shell=True)
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm transportedTR*.db  ', shell=True)
            processedSomething = False
            for fileName in os.listdir(os.getcwd()):
                if "transportedTR" in fileName:
                    print("processing " + fileName)
                    processedSomething = True
                    processTransportedTR(fileName)
                    os.remove(os.getcwd() + "/" + fileName)
            if processedSomething or True:
            #if processedSomething:
                    subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < taxonomyRelations.db ">" taxonomyRelations1.db  ', shell=True)
                    subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm taxonomyRelations.db  ', shell=True)
                    subprocess.call(r'ssh st1298@eros.cs.txstate.edu mv taxonomyRelations1.db taxonomyRelations.db ', shell=True)
            time.sleep(2)
            conn2 = sqlite3.connect("taxonomyRelations.db")
            c2 = conn2.cursor(cursor)
            c2.execute("pragma foreign_keys = ON")
            if random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
                c2.printDB()
                c2.close()
                conn2.commit()
            elif random.choice([0,0,0,0,0,1]):
                print("removing unused items in database...")
                c2.removeItemsNotBeingUsed()
                c2.close()
                conn2.commit()
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < taxonomyRelations.db ">" taxonomyRelations1.db  ', shell=True)
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm taxonomyRelations.db  ', shell=True)
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu mv taxonomyRelations1.db taxonomyRelations.db ', shell=True)
            else:
                print("sleeping...")
                c2.close()
                conn2.commit()
                time.sleep(15)
            shutil.copyfile("taxonomyRelations.db", "backUpTaxonomy.db")

    except Exception as e:
        processMainLoopException(e)

if __name__ == "__main__":
    main()