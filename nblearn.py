import os
import re
import math
import sys
import json

mainHash  = {}
stopwords = {}

def getWordHash(pathOfRoot):    
    HashOfWords = {}
    for rootPath, subdirs, allFiles in os.walk(pathOfRoot):            
        for everyFile in allFiles:            
            if everyFile.endswith(".txt") and everyFile != 'README.txt':                
                eachFle = os.path.join(rootPath, everyFile)
                with open(eachFle, 'r') as openedFile:                    
                    dataInFile = openedFile.read()                    
                    for oneLine in dataInFile.splitlines():
                        oneLine = re.sub('[^A-Za-z0-9\@#\$_]', ' ', oneLine)
                        wordsInLine = oneLine.split()                        
                        for eachword in wordsInLine:                            
                            word1 = eachword.lower()
                            if stopwords.has_key(word1) : continue
                            if word1 != '':
                                if HashOfWords.has_key(word1):
                                    countOfWords = HashOfWords[word1]
                                    countOfWords += 1
                                    HashOfWords[word1] = countOfWords
                                else:
                                    HashOfWords[word1] = 1
  
    return HashOfWords
#_______________________________________________________________    
def populateHash(currentClassWords,classToBeMatched):
    
    wordsFromOtherClasses = {}    
    if classToBeMatched != 'negTru':
        for word in negTruWordHash:
            if not currentClassWords.has_key(word): wordsFromOtherClasses[word] = 1
    if classToBeMatched != 'posDec':
        for word in posDecWordHash:
            if not currentClassWords.has_key(word): wordsFromOtherClasses[word] = 1
    if classToBeMatched != 'posTru':
        for word in posTruWordHash:
            if not currentClassWords.has_key(word): wordsFromOtherClasses[word] = 1            
    if classToBeMatched != 'negDec':
        for word in negDecWordHash:
            if not currentClassWords.has_key(word): wordsFromOtherClasses[word] = 1
                
    for word in wordsFromOtherClasses:
        currentClassWords[word] = 1
    for word in currentClassWords:
        if not wordsFromOtherClasses.has_key(word):
            earlierCount = int(currentClassWords[word])
            earlierCount += 1
            currentClassWords[word] = earlierCount
    return currentClassWords    
#_______________________________________________________
def getProbabilityHash(hashOfWords):
    totalCount = 0
    for i in hashOfWords.keys():
        totalCount+=hashOfWords[i]
    probTable = {}
    for i in hashOfWords.keys():    
        probTable[i] = math.log10(float(hashOfWords[i])) - math.log10(totalCount)     
    return probTable
#___________________________________________________
with open('stopwords.txt', 'r') as fp:
    stopwords = json.load(fp)
    
mainPath = sys.argv[1]
negDecPath = mainPath + 'negative_polarity/deceptive_from_MTurk' 
negDecWordHash = getWordHash(negDecPath)      
negTruPath = mainPath + 'negative_polarity/truthful_from_Web'
negTruWordHash = getWordHash(negTruPath)
posDecPath = mainPath + 'positive_polarity/deceptive_from_MTurk' 
posDecWordHash = getWordHash(posDecPath)
posTruPath = mainPath + 'positive_polarity/truthful_from_TripAdvisor' 
posTruWordHash = getWordHash(posTruPath)

negTruWordHash = populateHash(negTruWordHash,'negTru')
posDecWordHash = populateHash(posDecWordHash,'posDec')
posTruWordHash = populateHash(posTruWordHash,'posTru')
negDecWordHash = populateHash(negDecWordHash,'negDec')    

negDecProbHash = getProbabilityHash(negDecWordHash)
mainHash['negative_deceptive'] = negDecProbHash
negTruProbHash = getProbabilityHash(negTruWordHash)
mainHash['negative_truthful'] = negTruProbHash  
posDecProbHash = getProbabilityHash(posDecWordHash)
mainHash['positive_deceptive'] = posDecProbHash
posTruProbHash = getProbabilityHash(posTruWordHash)
mainHash['positive_truthful'] = posTruProbHash
with open('nbmodel.txt', 'w') as fp:
    json.dump(mainHash, fp)
            
