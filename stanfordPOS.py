import re, nltk

#stanfordPOSFeatures = stanfordPOS.getFeatures(exemplarRelationInfo, "stanfordParserOutput.txt") #list of tuples ex. [(textualPattern, feature), (textualPattern, feature), ...
#exemplarRelationInfo: list of tuples ex. [(textualPattern, supportItem, relation, sentence1), (textualPattern, supportItem, relation, sentence2), ...

def getAllRelationMembers(exemplarRelationTuple):
    members = []
    count = 0
    for patternPiece in re.split(r'_+', exemplarRelationTuple[0].rstrip('_')):
        if patternPiece.find("#") != -1:
            members.append( re.split(r'_+', exemplarRelationTuple[1].rstrip('_'))[count] )
            count += 1
        #else:
        #    members.append( exemplarRelationTuple[2] )
    #Ensure members is 3 and only 3 elements
    members = members[:3]
    if len(members) == 0:
        members += ["None", "None", "None"]
    if len(members) == 1:
        members += ["None", "None"]
    if len(members) == 2:
        members += ["None"]
    return members

def checkWordIsSubsumed(word, tree):
    if type(tree) == str:
        return word == tree
    for leaf in tree.leaves():
        if word == leaf:
            return True
    return False

def checkThatWordsAreSubsumed(words, tree):
    for word in words:
        if not checkWordIsSubsumed(word, tree):
            return False
    return True

def tailFindLowestCommonParent(words, tree, allParents):
    if checkThatWordsAreSubsumed(words, tree):
        if type(tree) == str:
            allParents.append(tree)
        else:
            allParents.append(tree.node)
    if type(tree) != str:
        for subtree in tree:
            tailFindLowestCommonParent(words, subtree, allParents)

def findLowestCommonParent(words, tree):
    if words == ["None"]:
        return "None"
    allParents = []
    parsedWords = []
    for possiblePhrase in words:
        parsedWords += nltk.word_tokenize(possiblePhrase)
    tailFindLowestCommonParent(parsedWords, tree, allParents)
    if (len(words) == 1): #do this because otherwise the lowest common parent is the word itself
        if len(allParents) > 1:
            allParents.pop()
        else:
            return "None"
    return allParents.pop()

def tailFindINCC(words, tree, allParents):
    if checkThatWordsAreSubsumed(words, tree):
        if (type(tree) != str) and tree.node == "PP":
            try:
                if tree[0].node == "IN":
                    allParents.append(tree.node)
            except:
                pass
        if (type(tree) != str) and tree.node == "NP":
            for subtree in tree:
                try:
                    if subtree.node == "CC":
                        allParents.append(tree.node)
                except:
                    pass
    if (type(tree) != str):
        for subtree in tree:
            tailFindINCC(words, subtree, allParents)

def getConjunctionCount(words, tree):
    count = 0
    for possiblePhrase in words:
        allParents = []
        parsedWords = nltk.word_tokenize(possiblePhrase)
        tailFindINCC(parsedWords, tree, allParents)
        count += len(allParents)
    return count

def separateSentences(fileName): #return list of strings where each string represents a parse of a particular sentence
    separateSentenceParses = []
    f = open(fileName, "r").read()
    toks = re.compile('((.+\n)*\n){2}')
    for match in toks.finditer(f):
        s = match.group(0)
        separateSentenceParses.append(s)
    return separateSentenceParses

def getTree(sentenceParse):
    toks = re.compile('[(]ROO(.+\n)*')
    for match in toks.finditer(sentenceParse):
        stringRepOfTree = match.group(0)
        #print(stringRepOfTree)
        #stringRepOfTree = "(S (NP I) (VP (V saw) (NP him)))"
        return nltk.tree.Tree(stringRepOfTree)

def getFeatures(exemplarRelationInfo, parserOutputFileName):
    #setup
    features = []
    separateSentenceParses = separateSentences(parserOutputFileName)
    #verify exemplarRelationInfo and separateSentenceParses have the same length (length =- # of sentences)
    if len(exemplarRelationInfo) != len(separateSentenceParses):
        raise NameError("ERROR - sentence lengths not same size")
    #get features
    print("stanfordPOS: getting features for " + str(len(exemplarRelationInfo)) + " sentences ...")
    for i in range(len(exemplarRelationInfo)):
        members = getAllRelationMembers(exemplarRelationInfo[i])
        #getting feature:  part of speech of each word in relation  ex. NN ; NN ; DT
        tree = getTree(separateSentenceParses[i])
        #for j in range(len(members)):
        #    posOfEachMember = "featPOSARG" + str(j+1) + "_"
        #        posOfEachMember += findLowestCommonParent([members[j]], tree)
        #     features.append((exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], posOfEachMember, exemplarRelationInfo[i][3]))
        #number of conjunctions (CC & IN) presents for each arg    ex. 1
        features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featCONJCOUNT_" + str(getConjunctionCount(members, tree)), exemplarRelationInfo[i][3]))
    print("stanfordPOS: extracted " + str(len(features)) + " features.")
    return features #ex. [(textualPattern, supportItem, feature, sentence), (textualPattern, sentence, feature)

def main():
    pass

if __name__ == "__main__":
    getFeatures()

