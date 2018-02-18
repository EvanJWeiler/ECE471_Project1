import pygame
import sys
import random


monograms = {}
digrams = {}
trigrams = {}

dataFile = open(sys.argv[1], 'r')
text = dataFile.read()
dataFile.close()

def frequencyAnalysis():
    #monograms
    for x in text:
        if monograms.has_key(x):
            monograms[x] += 1
        else:
            monograms[x] = 1

    #digrams
    for i, j in zip(text[::2], text[1::2]):
        key = i + j
        if digrams.has_key(key):
            digrams[key] += 1
        else:
            digrams[key] = 1

    #trigrams
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
        val += (float(monograms[x]) / (len(text)-1)) ** 2
    val = round(val, 5)
    print "IC: " + str(val)


def typeOfCipher():
    pass


def shiftCipher():

    pass


def subCipher():
    pass


def vigenereCipher():
    pass


def permutationCipher():
    pass


def oneTimePad():
    pass

def printFrequency(object):
    for key in sorted(object):
        print key, round(((float(object[key]) / (len(text)-1)) * 100) , 2)

def main():
    frequencyAnalysis()

    printFrequency(monograms)
    printFrequency(digrams)

    indexOfCoincidence()

main()
