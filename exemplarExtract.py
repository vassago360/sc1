import re
import csv
import StringIO
import nltk

def getInfo():
    exemplarRelationInfo = []
    with open("exemplarOutput.txt") as tsv:
        tsv.readline() #read past the first line: "Subjects    Relation    Objects    Normalized Relation    Sentence"
        for line in csv.reader(tsv, dialect="excel-tab"):
            #line = new parsed sentence
            textualPattern = ""
            supportItem = ""
            relation = ""
            #line[3] == Normalized Relation
            normRelation = re.compile('.+')
            for normRelation_match in normRelation.finditer(line[3]):
                textualPattern += normRelation_match.group(0) + "_"
            #line[0] == Subjects
            reader = csv.reader(StringIO.StringIO(line[0]), delimiter=',')
            for row in reader:
                for item in row:
                    subj = re.compile('SUBJ:.+#[PERORGMISCLOC]+')
                    for subj_match in subj.finditer(item):
                        textualPattern += subj_match.group(0)[:subj_match.group(0).find(":")+1]
                        supportItem += subj_match.group(0)[subj_match.group(0).find(":")+1:subj_match.group(0).find("#")] + "_"
                        textualPattern += subj_match.group(0)[subj_match.group(0).find("#"):] + "_"
            #line[1] == Relation
            regRelation = re.compile('.+')
            for regRelation_match in regRelation.finditer(line[1]):
                relation += regRelation_match.group(0)
            #line[2] == Objects
            reader = csv.reader(StringIO.StringIO(line[2]), delimiter=',')
            for row in reader:
                for item in row:
                    objects = re.compile('.+:.+#[PERORGMISCLOC]+')
                    for objects_match in objects.finditer(item):
                        textualPattern += objects_match.group(0)[:objects_match.group(0).find(":")+1]
                        supportItem += objects_match.group(0)[objects_match.group(0).find(":")+1:objects_match.group(0).find("#")] + "_"
                        textualPattern += objects_match.group(0)[objects_match.group(0).find("#"):] + "_"
            #sentence
            sentence = line[4]
            #a final check and then done
            parsedSentence = nltk.word_tokenize(sentence)
            if len(parsedSentence) < 100:
                exemplarRelationInfo.append((textualPattern, supportItem, relation, sentence)) #list of tuples ex. [(textualPattern, supportItem, sentence1), (textualPattern, supportItem, sentence2), ...
            #print("textualPattern: " + textualPattern)
            #print("supportItem: " + supportItem)
            #print(line)
            #print("")
    return exemplarRelationInfo

def main():
    pass

if __name__ == "__main__":
    getInfo()
