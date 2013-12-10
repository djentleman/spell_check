# based off the original version by Peter Norvig:
# http://norvig.com/spell-correct.html

import re
import collections

def words(text):
    # find all words comprised of lower case alphabet  in text file
    return re.findall('[a-z]+', text.lower()) 

base = lambda: 1 # lambda function that always returns 1 -> def base(): return 1

def train(words):
    model = collections.defaultdict(base)
    for word in words:
        model[word] += 1
    return model

dataset = words(open('dataset').read())
wordDict = train(dataset)
 # dict, with a score of every word, any word not contained will
 # have a score of 1.



def getDeletes(word):
    deletes = []
    for i in range(len(word)):
        deletes.append(word[:i] + word[i + 1:])
    return deletes

def getTransposes(word):
    transposes = []
    for i in range(len(word) - 1):
        transposes.append(word[:i] + word[i + 1] + word[i] + word[i + 2:])
    return transposes

def getReplaces(word):
    replaces = []
    for i in range(len(word)):
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            replaces.append(word[:i] + letter + word[i + 1:])
    return replaces
        
def getInserts(word):
    inserts = []
    for i in range(len(word)):
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            inserts.append(word[:i] + letter + word[i:])
    return inserts


def edits(word):
   deletes    = getDeletes(word)
   transposes = getTransposes(word)
   replaces   = getReplaces(word)
   inserts    = getInserts(word)
   # remove duplicates
   return set(deletes + transposes + replaces + inserts)


def recursiveEdits(word, levels):
    if levels <= 1:
        return edits(word)
    else:
        words = []
        for word in recursiveEdits(word, levels - 1):
            words += edits(word)
        return words
    
def maxScore(candidates):
    highScore = ""
    for word in candidates:
        if not (wordDict.get(highScore) == None or wordDict.get(word) == None):
            if wordDict.get(word) > wordDict.get(highScore):
                highScore = word
        elif wordDict.get(word) == None:
            continue
        else:
            highScore = word
    return highScore

def correct(word, depth):
    # if word is know, return word
    if (list(word for word in [word] if word in wordDict)) != []:
        return word
    candidates = [word]
    for i in range(1, depth + 1):
        candidates += list(set(word for word in recursiveEdits(word, i) if word in wordDict)) # nonrepeating list
    candidates += list(set(word for word in [word] if word in wordDict)) # level 0
    candidates = set(candidates)
    return maxScore(candidates) # checks which candidate has the highest score, based on the key
