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
        time.sleep(10)

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
    c2.removeItemsNotBeingUsed()
    ####
    conn1.commit()
    c1.close()
    conn2.commit()
    c2.close()

def main():
    #createInitialDatabase.run()
    #import pdb ; pdb.set_trace()
    try:
        while(True):
            subprocess.call(r'scp st1298@eros.cs.txstate.edu:transportedTR*.db ./ ', shell=True)
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm transportedTR*.db  ', shell=True)
            for fileName in os.listdir(os.getcwd()):
                if "transportedTR" in fileName:
                    print("processing " + fileName)
                    processTransportedTR(fileName)
                    os.remove(os.getcwd() + "/" + fileName)
                    #import pdb ; pdb.set_trace()
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < taxonomyRelations.db ">" taxonomyRelations1.db  ', shell=True)
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm taxonomyRelations.db  ', shell=True)
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu mv taxonomyRelations1.db taxonomyRelations.db ', shell=True)
            time.sleep(2)
            conn2 = sqlite3.connect("taxonomyRelations.db")
            c2 = conn2.cursor(cursor)
            c2.execute("pragma foreign_keys = ON")
            c2.printDB()
            shutil.copyfile("taxonomyRelations.db", "backUpTaxonomy.db")
            time.sleep(2)
    except Exception as e:
        processMainLoopException(e)

if __name__ == "__main__":
    main()