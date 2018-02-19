#import pygame
import sys
import random
import operator
import math
from math import sqrt

dataFile = open(sys.argv[1], 'r')
text = dataFile.read()
textList = list(text)
dataFile.close()

monograms = {}
digrams = {}
trigrams = {}

def frequencyAnalysis():
    global monograms
    monograms = createMonogram(text)
    createDigram()
    createTrigram()
    print "The frequency of the monograms are:"
    printFrequency(monograms)
    print "the Frequency of the digrams are:"
    printFrequency(digrams)

def printFrequency(object):
    for key in sorted(object):
        print key, round(((float(object[key]) / (len(text) - 1)) * 100), 2)

def createMonogram(monoText):
    newMono = {}
    for x in monoText:
        if newMono.has_key(x):
            newMono[x] += 1
        else:
            newMono[x] = 1
    return newMono

def createDigram():
    for i, j in zip(text[::1], text[1::1]):
        key = i + j
        if digrams.has_key(key):
            digrams[key] += 1
        else:
            digrams[key] = 1

def createTrigram():
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

def indexOfCoincidence(mono):
    # index of Coincidence
    val = 0
    for x in mono:
        val += (float(mono[x]) / (len(text) - 1)) ** 2
    val = round(val, 5)
    return val

def typeOfCipher():
    IC = indexOfCoincidence(monograms)
    if IC > .05:
        print "The index of coincidence is: " + str(IC)
        print "This means the type is monoalphabetic"
        print "Attempting a shift cipher..."
        return 0
    else:
        print "The index of coincidence is: " + str(IC)
        print "This means the type is polyalphabetic"
        print "Attempting a vigenere cipher..."
        return 1

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
    print "The type of cipher is: Shift Cipher"
    print "The key is: " + str(shiftNumber)
    print "Below is the decoded text using a shift cipher:"
    print textString

def vigenereCipher():
    factors = {}
    indexSpacing = []
    maybeKeys = []
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
    keyLengths = []
    maxFactors = []
    for x in range(5):
        maxFactors.append(factors[sorted(factors, key=factors.get, reverse=True)[x]])
    for x in factors:
        if factors[x] in maxFactors:
            keyLengths.append(x)

    #get every Nth letter from string into their own string
    for keyLength in keyLengths:
        maybeKeysForLength = {}
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

                #do frequency analysis and see which is most like english
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
            maybeKeysForLength[iteration] = finalScores
        tempKeys = maybeKeysForLength[0]
        tempKeys2 = []
        for x in range(1,len(maybeKeysForLength)):
            for tempKey in tempKeys:
                for y in range(len(maybeKeysForLength[x]) ):
                    tempKeys2.append(tempKey + maybeKeysForLength[x][y])
            tempKeys = list(tempKeys2)
            tempKeys2 = []
        maybeKeys.extend(tempKeys)
    indexes = []
    for maybeKey in maybeKeys:
        newText = []
        textCounter = 0;
        for x in text:
            shift = ord(maybeKey[textCounter % len(maybeKey)]) - 65
            x = ord(x) - shift
            if x < 65:
                x += 26
            newText.append(chr(x))
            textCounter += 1
        keyText = ''.join(newText)
        tempMono = createMonogram(keyText)
        indexes.append([indexOfCoincidence(tempMono),maybeKey,keyText])
    finalIndexes = []
    for x in indexes:
        if x[0] > .05:
            finalIndexes.append(x)

    return finalIndexes

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

def waitForUser():
    wait = True
    correct = raw_input("Would you like to proceed? (y/n) ")
    while wait:
        if correct == 'y':
            running = False
            return 1
        elif correct == 'n':
            print "Goodbye."
            running = False
            return 0
        else:
            correct = raw_input("Invalid input, Please try again: (y/n) ")


def main():
    frequencyAnalysis()
    CipherType = typeOfCipher()
    terminate = waitForUser()
    if terminate == 0:
        return
    if CipherType == 0:
        shiftCipher()
        correct = raw_input("Is this correct? (y/n) ")
        running = True
        while running:
            if correct == 'y':
                print "Glad we could help!"
                running = False
            elif correct == 'n':
                print "If the output is not english, it must be encoded using a subsitution cipher."
                print "Here is a list of the monogram frequencies: "
                printFrequency(monograms)
                print "Here is a list of the digram frequencies: "
                printFrequency(digrams)
                print "Above are the monogram and digram frequencies. The text must be encoded using a subsitution cipher. \nDecoding must be done manually. Good Luck!"
                running = False
            else:
                correct = raw_input("Invalid input, Please try again: (y/n) ")

    else:
        correct = 'x'
        possibleSolutions = vigenereCipher()
        print "We found " + str(len(possibleSolutions)) + " possible keys."
        for solution in possibleSolutions:
            print "The type of cipher is: Vigenere Cipher"
            print "The key for this solution is: " + solution[1]
            print "The decoded text is:"
            print solution[2]
            correct = raw_input("Is this correct? (y/n) ")
            running = True
            while running:
                if correct == 'y':
                    print "Glad we could help!"
                    running = False
                    return
                elif correct == 'n' and solution != possibleSolutions[len(possibleSolutions)-1]:
                    print "Here is another possible answer:\n"
                    terminate = waitForUser()
                    if terminate == 0:
                        return
                    running = False
                elif correct == 'n' and solution == possibleSolutions[len(possibleSolutions)-1]:
                    print "The code must be encoded with a One Time Pad or a Permutation Cipher."
                    print "These must be done with more information. Good Luck!"
                    running = False
                else:
                    correct = raw_input("Invalid input, Please try again: (y/n) ")


main()
