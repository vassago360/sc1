import re, nltk

class ParseError(Exception):
    pass

# Tokenize a string.
# Tokens yielded are of the form (type, string)
# Possible values for 'type' are '/' and 'WORD'
def tokenize(s):
    toks = re.compile(' +|[^\s]+')
    for match in toks.finditer(s):
        sub_string = match.group(0)
        if sub_string[0] == ' ':
            continue
        else:
            word_toks = re.compile('[^\s]+/')
            for match in word_toks.finditer(sub_string):
                sub_string_word = match.group(0)[:-1]
            type_toks = re.compile('/[^\s]+')
            for match in type_toks.finditer(sub_string):
                sub_string_type = match.group(0)
            yield(sub_string_type, sub_string_word)

# Parse once we're inside an opening bracket.
def extract_named_entities(toks):
    previousTy = None
    fullName = ("", None)
    for ty, name in toks:
        if ty != '/O':
            if (fullName[0] != "") and (previousTy != ty):
                print(fullName)
                fullName = ("", None)
            fullName = (fullName[0] + " " + name, ty)
        previousTy = ty

def separateSentences(fileName): #return list of strings where each string represents a parse of a particular sentence
    separateSentenceParses = []
    f = open(fileName, "r").read()
    toks = re.compile(r'((.|\t)+[\n])+')
    for match in toks.finditer(f):
        s = match.group(0)
        separateSentenceParses.append(s)
    return separateSentenceParses

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

def getNE(phrase, nerSentence):
    if phrase == None:
        return None
    tokPhrase = nltk.word_tokenize(phrase)
    annotatedSentence = re.split(r'\n', nerSentence.rstrip('\n'))
    for word in tokPhrase:
        for annotatedWord in annotatedSentence:
            pieces = re.split(r'\t', annotatedWord.rstrip('\t'))
            for i in range(len(pieces)):
                if (word == pieces[i]):# and (pieces[i+1] != "O"):
                    fineGrainedNamedEntity = re.split(r'/', pieces[i+1].rstrip('/'))[-1:][0]
                    return fineGrainedNamedEntity

def getNEOneBefore(phrase, nerSentence):
    tokPhrase = [nltk.word_tokenize(phrase)[0]]
    #print(tokPhrase)
    tokNERSentence = nltk.word_tokenize(nerSentence)
    for word in tokPhrase:
        for annotatedWord in tokNERSentence:
            pieces = re.split(r'/', annotatedWord.rstrip('/'))
            for i in range(len(pieces)):
                if (word == pieces[i]):# and (pieces[i+1] != "O"):
                    try:
                        return pieces[i-1]
                    except:
                        print("too early which probably ok")
                        return None

def getNEOneAfter(phrase, nerSentence):
    tokPhrase = nltk.word_tokenize(phrase)[-1:]
    #print(tokPhrase)
    tokNERSentence = nltk.word_tokenize(nerSentence)
    for word in tokPhrase:
        for annotatedWord in tokNERSentence:
            pieces = re.split(r'/', annotatedWord.rstrip('/'))
            for i in range(len(pieces)):
                if (word == pieces[i]):# and (pieces[i+1] != "O"):
                    try:
                        return pieces[i+1]
                    except:
                        print("too late which probably ok")
                        return None

def getFeatures(exemplarRelationInfo, parserOutputFileName): # featNEARG1, featNEARG2, featNEARG3
    #setup
    features = []
    separateSentenceParses = separateSentences(parserOutputFileName)
    #verify exemplarRelationInfo and separateSentenceParses have the same length (length =- # of sentences)
    if len(exemplarRelationInfo) != len(separateSentenceParses):
        raise NameError("ERROR - sentence lengths not same size")
    #get features
    print("figerNER: getting features for " + str(len(exemplarRelationInfo)) + " sentences ...")
    for i in range(len(exemplarRelationInfo)):
        members = getAllRelationMembers(exemplarRelationInfo[i])
        #get feature:  named entity of each word in relation            ex. PERSON_O_LOCATION
        for j in range(len(members)):
            neARG = str(getNE(members[j], separateSentenceParses[i]))
            if (neARG != "None") and (neARG != ""):
                features.append( (exemplarRelationInfo[i][0], exemplarRelationInfo[i][1], "featNEARG" + str(j+1) + "_" + neARG, exemplarRelationInfo[i][3]))
    print("figerNER: extracted " + str(len(features)) + " features.")
    return features  #ex. [(textualPattern, supportItem, feature, sentence), (textualPattern, sentence, feature)

def main():
    pass

if __name__ == "__main__":
    getFeatures()


#subprocess.call("./stanford-ner-2014-01-04/ner.sh > stanfordNEROutput.txt", shell=True)
#stanfordNERFeatures = stanfordNER.getFeatures(exemplarRelationInfo, "stanfordNEROutput.txt") #list of tuples ex. [(textualPattern, supportItem, feature, sentence), ...