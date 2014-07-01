import re, nltk

class ParseError(Exception):
    pass

def separateSentences(fileName): #return list of strings where each string represents a parse of a particular sentence
    separateSentenceParses = []
    f = open(fileName, "r").read()
    toks = re.compile('((.+\n)*\n){2}')
    for match in toks.finditer(f):
        s = match.group(0)
        separateSentenceParses.append(s)
    return separateSentenceParses

# Tokenize a string.
# Tokens yielded are of the form (type, string)
# Possible values for 'type' are '(', ')' and 'WORD'
def tokenize(s):
    tokens = []
    toks = re.compile('.+[(].+-\d.+-\d+\)')
    for match in toks.finditer(s):
        s = match.group(0)
        dep_toks = re.compile('.+[(]')
        for dep_match in dep_toks.finditer(s):
            dep_s = dep_match.group(0)[:-1]
        arg1_toks = re.compile('[(].+[,][ ]')
        for arg1_match in arg1_toks.finditer(s):
            arg1_s = arg1_match.group(0)[1:-2]
        arg2_toks = re.compile(', .+[)]')
        for arg2_match in arg2_toks.finditer(s):
            arg2_s = arg2_match.group(0)[2:-1]
        #try:
        tokens.append((dep_s, arg1_s, arg2_s))
        #except UnboundLocalError:
        #    continue
    return tokens

def extract_dependency_parts(toks):
    for tok in toks:
        print(tok)
        #print("")
        #print("")
        #for item in tok:
        #    print(item)
        #    print("")

def getClosestWord(word, tokSentence):
    for wS in tokSentence:
        if word in wS:
            return wS

def findStartingPosition(tokPhrase, tokSentence):
    wpIndex = 0
    for wP in tokPhrase:
        cWP = wP
        #cWP = getClosestWord(wP, tokSentence)
        #print("wpIndex: " + str(wpIndex))
        if (tokSentence.index(cWP) - 1 == wpIndex) or (wpIndex == 0):
            wpIndex = tokSentence.index(cWP)
            #print("wpIndex now: " + str(wpIndex))
        else:
            try:
                wpIndex = tokSentence.index(cWP, wpIndex)
            except ValueError:
                return -1
            #print("wpIndex else now: " + str(wpIndex))
    return wpIndex - (len(tokPhrase)-1)

def findWordLocation(word, tokPhrase, tokSentence):
    #my counting will almost certainly be different than stanfords.
    #get count of each word of phrase and compare that to each count of same word in depen
    startingPosition = findStartingPosition(tokPhrase, tokSentence)
    if startingPosition == -1: #the phrase (relation words) are backwards (out of order)
        return findStartingPosition([word], tokSentence)
    else:
        return startingPosition

def getAllOccurances(word, depenTuples):
    occurances = [] #ex. [3, 6]
    for depenTuple in depenTuples:
        if word == depenTuple[1].split("-")[0]:
            occurances.append(int(depenTuple[1].split("-")[-1:][0]))
        elif word == depenTuple[2].split("-")[0]:
            occurances.append(int(depenTuple[2].split("-")[-1:][0]))
    occurances = list(set(occurances))
    return occurances

def pickClosestDepenArg(word, tokPhrase, tokSentence, depenTuples):
    #print("word: " +str(word))
    #print("tokPhrase: "+str(tokPhrase))
    #print("tokSentence: "+str(tokSentence))
    myList = getAllOccurances(word, depenTuples) #ex. [3, 6]
    #print("myList: " + str(myList))
    myNumber = findWordLocation(word, tokPhrase, tokSentence) #ex. 4
    if myList:
        closestNum = min(myList, key=lambda x:abs(x-myNumber))
        #verify DependArg exists
        #dependArg = getClosestWord(word, tokSentence) + "-" + str(closestNum)
        dependArg = word + "-" + str(closestNum)
        for depenTuple in depenTuples:
            if dependArg in depenTuple:
                #print("CORRECT: pickClosestDepenArg found - "  + dependArg)
                return   dependArg
        print("ERROR: pickClosestDepenArg can't find: " + dependArg)
    else:
        pass
        #print("NOTICE: Skipping '" + word + "' because it's not an dependency argument")

def getPhraseLocations(phrase, sentence, depenTuples):
    phraseLocations = []
    tokPhrase = nltk.word_tokenize(phrase)
    if (len(tokPhrase) >= 2) and (tokPhrase[-1:][0] == '.'):
        tokPhrase = tokPhrase[:-2] + [tokPhrase[-2:-1][0] + tokPhrase[-1:][0]]
    tokSentence = nltk.word_tokenize(sentence)
    for wP in tokPhrase:
        dependArg = pickClosestDepenArg(wP, tokPhrase, tokSentence, depenTuples)
        if dependArg:
            phraseLocations.append(dependArg)
    #return [phrase[0]-4,phrase[1]-5,phrase[2]-6,phrase[3]-7]
    return phraseLocations

def getDependency(sentence, phrase, HeadOrDepen, depenTuples):
    #break phrase into individual words with its sentence location taken to account
    #return nsubj_aux_dobj
    dependency = ""
    phraseWLoc = getPhraseLocations(phrase, sentence, depenTuples) #let's say its [Mr-4,Jerry-5,Rice-6,Jr-7]
    count = 0 #use count to cap it at 3 dependencies so there's not so many combinations
    for wP in phraseWLoc: #[:3]:
        for depenTuple in depenTuples:
            #if we got makes-8 then nsubj(makes-8, Bell-1)  nsubj is the depen for looking for "depen"
            if HeadOrDepen == "head":
                if (wP == depenTuple[2]) and not (depenTuple[1] in phraseWLoc): #make sure a word in the phrase is in the dependency tuple and no other word in the phrase is in it
                    if count > 2:
                        return dependency
                    dependency += depenTuple[0] + "_"
                    count += 1
            if HeadOrDepen == "depen":
                if (wP == depenTuple[1]) and not (depenTuple[2] in phraseWLoc): #make sure a word in the phrase is in the dependency tuple and no other word in the phrase is in it
                    if count > 2:
                        return dependency
                    dependency += depenTuple[0] + "_"
                    count += 1
    return dependency

def getFeatures(exemplarRelationInfo, parserOutputFileName):
    #getting 2 features for each extracted relation
    features = []
    separateSentenceParses = separateSentences(parserOutputFileName)
    #verify exemplarRelationInfo and separateSentenceParses have the same length (length =- # of sentences)
    if len(exemplarRelationInfo) != len(separateSentenceParses):
        raise NameError("ERROR - sentence lengths not same size")
    #get features
    print("stanfordDepen: getting features for " + str(len(exemplarRelationInfo)) + " sentences ...")
    totalPatternPieces = 0
    for i in range(len(exemplarRelationInfo)):
        #first get the verb and arguments and get the corresponding depen tuple
        #print("exemplarRelationInfo[i]: " + str(exemplarRelationInfo[i]))                                                           #gives us relation verb (from textualPattern) and its arguments (from supportSet)    #(textualPattern, supportItem, relation, sentence1)
        depenTuples = tokenize(separateSentenceParses[i])                                             #generator object - "list" of depen tuples
        count = 0
        for patternPiece in re.split(r'_+', exemplarRelationInfo[i][0].rstrip('_')):
            totalPatternPieces += 1
            if patternPiece.find("#") != -1 and count < 3:
                arg = re.split(r'_+', exemplarRelationInfo[i][1].rstrip('_'))[count]
                depenFeature = getDependency(exemplarRelationInfo[i][3], arg, "depen", depenTuples)
                if (depenFeature != "None") and (depenFeature != ""):
                    features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENSUBARG" + str(count+1) + "_" + depenFeature, exemplarRelationInfo[i][3] ) )
                depenFeature = getDependency(exemplarRelationInfo[i][3], arg, "head", depenTuples)
                if (depenFeature != "None") and (depenFeature != ""):
                    features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENHEADARG" + str(count+1) + "_" + depenFeature, exemplarRelationInfo[i][3] ) )
                count += 1
        """if count == 0:
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENSUBARG" + str(1) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENSUBARG" + str(2) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENSUBARG" + str(3) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENHEADARG" + str(1) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENHEADARG" + str(2) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENHEADARG" + str(3) + "_None", exemplarRelationInfo[i][3] ) )
        if count == 1:
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENSUBARG" + str(2) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENSUBARG" + str(3) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENHEADARG" + str(2) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENHEADARG" + str(3) + "_None", exemplarRelationInfo[i][3] ) )
        if count == 2:
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENSUBARG" + str(3) + "_None", exemplarRelationInfo[i][3] ) )
            features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featDEPENHEADARG" + str(3) + "_None", exemplarRelationInfo[i][3] ) )"""
    print("stanfordDepen: extracted " + str(len(features)) + " features from " + str(totalPatternPieces) + " args/relations.")
    return features #list of tuples ex. [(textualPattern, supportItem, feature, sentence), (textualPattern, sentence, feature)

def main():
    pass

if __name__ == "__main__":
    getFeatures()




