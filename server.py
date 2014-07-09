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

def main():
    #createInitialDatabase.run()
    #import pdb ; pdb.set_trace()
    #try:
    while(True):
        subprocess.call(r'scp st1298@eros.cs.txstate.edu:transportedTR*.db ./ ', shell=True)
        subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm transportedTR*.db  ', shell=True)
        processedSomething = False
        for fileName in os.listdir(os.getcwd()):
            if "transportedTR" in fileName:
                print("processing " + fileName)
                processedSomething = True
                processTransportedTR(fileName)
                os.remove(os.getcwd() + "/" + fileName)
                #import pdb ; pdb.set_trace()
        if processedSomething:
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < taxonomyRelations.db ">" taxonomyRelations1.db  ', shell=True)
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm taxonomyRelations.db  ', shell=True)
                subprocess.call(r'ssh st1298@eros.cs.txstate.edu mv taxonomyRelations1.db taxonomyRelations.db ', shell=True)
        time.sleep(2)
        conn2 = sqlite3.connect("taxonomyRelations.db")
        c2 = conn2.cursor(cursor)
        c2.execute("pragma foreign_keys = ON")
        if random.choice([0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
            c2.printDB()
        elif random.choice([0,0,0,0,0,0,1]):
            print("removing unused items in database...")
            c2.removeItemsNotBeingUsed()
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu cat < taxonomyRelations.db ">" taxonomyRelations1.db  ', shell=True)
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu rm taxonomyRelations.db  ', shell=True)
            subprocess.call(r'ssh st1298@eros.cs.txstate.edu mv taxonomyRelations1.db taxonomyRelations.db ', shell=True)
<<<<<<< HEAD
        else:
            print("sleeping...")
            time.sleep(15)
        shutil.copyfile("taxonomyRelations.db", "backUpTaxonomy.db")

    """except Exception as e:
        processMainLoopException(e)"""
=======
            time.sleep(2)
            conn2 = sqlite3.connect("taxonomyRelations.db")
            c2 = conn2.cursor(cursor)
            c2.execute("pragma foreign_keys = ON")
            c2.printDB()
            shutil.copyfile("taxonomyRelations.db", "backUpTaxonomy.db")
            time.sleep(2)
    except Exception as e:
        processMainLoopException(e)
>>>>>>> 411b52108a347e52f5b66a2f03e12b8af2a9a8a2

if __name__ == "__main__":
    main()