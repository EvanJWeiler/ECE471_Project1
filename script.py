import pygame
import sys
import random
import operator


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
    for i, j in zip(text[::2], text[1::2]):
        key = i + j
        if digrams.has_key(key):
            digrams[key] += 1
        else:
            digrams[key] = 1

    # trigrams
    for i, j, k in zip(text[::2], text[1::2], text[2::3]):
        key = i + j + k
        if trigrams.has_key(key):
            trigrams[key] += 1
        else:
            trigrams[key] = 1


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

    # import pdb; pdb.set_trace()

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
    pass


def permutationCipher():
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
    print(shiftCipher())


main()
