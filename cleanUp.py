from derivedClasses import *

def deleteInputTextFolderFiles():
    filelist = [ f for f in os.listdir(os.getcwd() + '/exemplar-master/inputText') ]
    for f in filelist:
        os.remove(os.getcwd() + '/exemplar-master/inputText/' + f)


#### delete exemplar files being used
deleteInputTextFolderFiles()
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