#import pygame
import sys
import random
import operator
import math
from math import sqrt


monograms = {}
digrams = {}
trigrams = {}

dataFile = open(sys.argv[1], 'r')
text = dataFile.read()
textList = list(text)
dataFile.close()


def frequencyAnalysis():
    # monograms
    for x in text:
        if monograms.has_key(x):
            monograms[x] += 1
        else:
            monograms[x] = 1

    # digrams
    for i, j in zip(text[::1], text[1::1]):
        key = i + j
        if digrams.has_key(key):
            digrams[key] += 1
        else:
            digrams[key] = 1

    # trigrams
    # for vigenere first find repeating trigrams
    index = 0
    for i, j, k in zip(text[::1], text[1::1], text[2::1]):
        key = i + j + k
        if trigrams.has_key(key):
            trigrams[key][0] += 1
            trigrams[key].append(index)
        else:
            trigrams[key] = [1, index]
        index += 1


def indexOfCoincidence():
    # index of Coincidence
    val = 0
    for x in monograms:
        val += (float(monograms[x]) / (len(text) - 1)) ** 2
    val = round(val, 5)
    print "IC: " + str(val)


def typeOfCipher():
    pass


def shiftCipher():
    shiftNumber = 0
    sortedMono = sorted(monograms, key=monograms.get, reverse=True)
    shiftNumber = ord(sortedMono[0]) - ord('E')

    if(shiftNumber < 0):
        shiftNumber += 26



    for x in range(0, len(textList)):
        if (ord(textList[x]) - shiftNumber) < 65:
            textList[x] = chr(ord(textList[x]) - shiftNumber + 26)
        else:
            textList[x] = chr(ord(textList[x]) - shiftNumber)

    textString = ''.join(textList)

    return textString


def subCipher():
    #key = "ETAOINSHRDLUCMWFYGPBVKXJQZ"
    #alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #newText = text
    #print monograms
    #stortedMono = sorted(monograms, key=monograms.get, reverse=True)
    #print stortedMono
    #print newText
    #keyIndices = [stortedMono.index(k) for k in newText]
    #print keyIndices
    #print ''.join(key[keyIndex] for keyIndex in keyIndices)
    #print newText
    #
    #print stortedMono
    #counter = 0;
    #print newText
    # for x in stortedMono:
    #    newText = newText.replace(x, key[counter])
    #    counter += 1
    #print newText
    pass


def vigenereCipher():
    factors = {}
    indexSpacing = []
    maybeKeys = {}
    for x in trigrams:
        if trigrams[x][0] > 1:
            #find spacing between these trigrams
            for index in range(1, len(trigrams[x])):
                for index2 in range(index+1, len(trigrams[x])):
                    indexSpacing.append(trigrams[x][index2] - trigrams[x][index])
    indexSpacing = list(set(indexSpacing))
    #then find the factors of the spacing
    for indexSpace in indexSpacing:
        for i in range(2, indexSpace + 1):
           if indexSpace % i == 0:
               if factors.has_key(i):
                   factors[i] += 1
               else:
                   factors[i] = 1
    #factor with the most hits is the length of the key
    maxFactor = 0
    keyLengths = []
    maxFactor = factors[sorted(factors, key=factors.get, reverse=True)[0]]
    for x in factors:
        if factors[x] == maxFactor:
            keyLengths.append(x)

    #get every Nth letter from string into their own string
    #for keyLength in keyLengths:
    keyLength = 4
    for iteration in range(keyLength):
        origTextList = []
        scores = []
        for x in text[iteration::keyLength]:
            origTextList.append(x)
        for shiftNumber in range(26):
            textList = list(origTextList)
            for x in range(0, len(textList)):
                if (ord(textList[x]) - shiftNumber) < 65:
                    textList[x] = chr(ord(textList[x]) - shiftNumber + 26)
                else:
                    textList[x] = chr(ord(textList[x]) - shiftNumber)
            shiftedString = {}
            textString = ''.join(textList)
            for character in textString:
                if shiftedString.has_key(character):
                    shiftedString[character] += 1
                else:
                    shiftedString[character] = 1
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for character in alphabet:
                if character not in shiftedString.keys():
                    shiftedString[character] = 0
            sortedShift = sorted(shiftedString, key=shiftedString.get, reverse=True)
            count = 0
            score = 0
            for commonLetter in 'ETAOIN':
                if commonLetter in sortedShift[:6]:
                    score += 1
            for uncommonLetter in 'VKJXQZ'[-6:]:
                if uncommonLetter in sortedShift[-6:]:
                    score += 1
            scores.append(score)
        maxScore = max(scores)
        finalScores = []
        scoreIndex = 0;
        for score in scores:
            if score == maxScore:
                finalScores.append(chr(scoreIndex + 65))
            scoreIndex += 1
        maybeKeys[iteration] = finalScores
    print maybeKeys


    #do frequency analysis and see which is most like english
    #whichever character makes it most like english is the one that is the right one



def permutationCipher(keyLength):
    gridForm = []
    row = []
    currWordMax = 0
    wordMaxKeyLength = 0
    #row.append(textList[0])
    #3349 characters (len(textList))
    #8x258 (#ofchar)mod(keylength)x(ceil(characters/keylength))
    #5x257 [keylength - (#ofchar)mod(keylength)]x(floor(characters/keylength))

    #import pdb; pdb.set_trace()

    #begin
    fullLines = len(textList) % keyLength #8
    fullLinesLength = math.ceil(len(textList)/float(keyLength)) #258
    shortLines = (keyLength - (len(textList) % keyLength)) #5
    shortLinesLength = math.floor(len(textList)/float(keyLength)) #257
    midPoint = int(len(textList) - shortLines*shortLinesLength) #2064

    #import pdb; pdb.set_trace()
    if(fullLines == 0):
        row.append(textList[0])
        for i in range(1, len(textList)):
            if(i % fullLinesLength == 0):
                gridForm.append(row)
                row = []

            row.append(textList[i])

    else:
        row.append(textList[0])
        for i in range(1, midPoint):
            if(i % fullLinesLength == 0):
                gridForm.append(row)
                row = []

            row.append(textList[i])

        for j in range(midPoint, len(textList)):
            if((j-midPoint) % shortLinesLength == 0):
                gridForm.append(row)
                row = []

            row.append(textList[j])

        gridForm.append(row)

        for i in range(len(textList)%keyLength, keyLength):
            gridForm[i].append("&")


    transposeGridForm = [list(i) for i in zip(*gridForm)] #transpose matrix
    transposeGridFormOneLine = [y for x in transposeGridForm for y in x] #flatten transposed matrix

    transposeGridFormOneLineString = ''.join(transposeGridFormOneLine) #converting to string
    transposeGridFormOneLineString = transposeGridFormOneLineString.replace("&", "") #removing placeholder characters

    #import pdb; pdb.set_trace()
    #wordMax = transposeGridFormOneLineString.count("THE") + transposeGridFormOneLineString.count("AND")
    # if(transposeGridFormOneLineString.count("THE") > currWordMax):
    #     currWordMax = transposeGridFormOneLineString.count("THE")
    #     wordMaxKeyLength = keyLength

    #end

    print(transposeGridFormOneLineString)
    #print(transposeGridFormOneLineString)
    #print(transposeGridFormOneLineString.count("THE"))








    #print text in grid
    # for i in range(len(gridForm)):
    #     for j in range(len(gridForm[i])):
    #         sys.stdout.write(''.join(gridForm[i][j]))
    #     print()

    #theory
    #make ciphertext into grid
    #transpose grid [list(i) for i in zip(*theArray)]
    #add each row onto each other



    pass


def oneTimePad():
    pass


def printFrequency(object):
    for key in sorted(object):
        print key, round(((float(object[key]) / (len(text) - 1)) * 100), 2)


def main():
    frequencyAnalysis()

    # printFrequency(monograms)
    # printFrequency(digrams)
    # indexOfCoincidence()

    # subCipher()
    #print shiftCipher()
    permutationCipher(14)
    #vigenereCipher()

main()
