import os
import json
import re
import sys
import math

mainHash = {}
negDecRepository = {}
negTruRepository = {}
posDecRepository = {}
posTruRepository = {}
stopwords = {}

def findClass(givenPath,outputFile):    
    for rootpath, subdirs, allFiles in os.walk(givenPath):
        for everyFile in allFiles:
            if everyFile.endswith(".txt") and everyFile != 'README.txt':
                eachFle1 = os.path.join(rootpath, everyFile)
                with open(eachFle1, 'r') as openedFile:                
                    dataInFile = openedFile.read()
                    tally = {}
                    #Prior probabilities
                    tally['negDecScore'] = math.log10(0.25)
                    tally['negTruScore'] = math.log10(0.25)
                    tally['posDecScore'] = math.log10(0.25)
                    tally['posTruScore'] = math.log10(0.25)
                    for eachLine in dataInFile.splitlines():
                        eachLine = re.sub('[^A-Za-z0-9\@#\$_]', ' ', eachLine)
                        wordsInLine = eachLine.split()                        
                        for eachword in wordsInLine:                            
                            word1 = eachword.lower()
                            if stopwords.has_key(word1) : continue         
                            if negDecRepository.has_key(word1):                                                                  
                                tally['negDecScore'] += negDecRepository[word1]                                                            
                            if negTruRepository.has_key(word1):                                
                                tally['negTruScore'] += negTruRepository[word1]                                
                            if posDecRepository.has_key(word1):                                                            
                                tally['posDecScore'] += posDecRepository[word1]                                                                
                            if posTruRepository.has_key(word1):                                
                                tally['posTruScore'] += posTruRepository[word1]
                                
                    label = max(tally, key=tally.get)
                    if label == 'negDecScore':
                        outputFile.write('deceptive' + ' ' + 'negative' + ' ' + everyFile)
                        outputFile.write('\n')                        
                    elif label == 'negTruScore':
                        outputFile.write('truthful' + ' ' + 'negative' + ' ' + everyFile)
                        outputFile.write('\n')                        
                    elif label == 'posDecScore':
                        outputFile.write('deceptive' + ' ' + 'positive' + ' ' + everyFile)
                        outputFile.write('\n')                        
                    elif label == 'posTruScore':
                        outputFile.write('truthful' + ' ' + 'positive' + ' ' + everyFile)
                        outputFile.write('\n')                        
                     
devPath = sys.argv[1]
fw = open('nboutput.txt','w') 
#Reading the json dump                   
with open('nbmodel.txt', 'r') as fp:    
    mainHash = json.load(fp)    
for jsonKey in mainHash.keys():
    if jsonKey == 'negative_deceptive':
        negDecRepository = mainHash[jsonKey]
    elif jsonKey == 'negative_truthful':
        negTruRepository = mainHash[jsonKey]
    elif jsonKey == 'positive_deceptive':
        posDecRepository = mainHash[jsonKey]
    elif jsonKey == 'positive_truthful':
        posTruRepository = mainHash[jsonKey]
        
with open('stopwords.txt', 'r') as fp:
    stopwords = json.load(fp)
        
findClass(devPath,fw)

