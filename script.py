import pygame
import sys
import random


# monograms
monograms = {}

# digrams
digrams = {}

dataFile = open(sys.argv[1], 'r')
text = dataFile.read()


def frequencyAnalysis():
    #monograms
    for x in text:
        if monograms.has_key(x):
            monograms[x] += 1
        else:
            monograms[x] = 1

    for key in monograms:
        monograms[key] = round(((float(monograms[key]) / (len(text)-1)) * 100) , 2)

    for key in monograms:
        print key, monograms[key]
    #digrams
    for i, j in zip(text[::2], text[1::2]):
        key = i + j
        if digrams.has_key(key):
            digrams[key] += 1
        else:
            digrams[key] = 1

    for key in digrams:
        digrams[key] = round(((float(digrams[key]) / (len(text)-1)) * 100) , 2)

    for key in sorted(digrams):
        print key, digrams[key]



def indexOfCoincidence():
    # index of Coincidence
    val = 0
    for x in monograms:
        val += (monograms[x]/100) * (monograms[x]/100)
    print val


def typeOfCipher():
    pass


def shiftCipher():

    pass


def subCipher():
    pass


def vigenereCipher():
    trigrams = {}
    for i, j, k in zip(text[::2], text[1::2], text[2::3]):
        key = i+j+k
        if monograms.has_key(key):
            monograms[key] += 1
        else:
            monograms[key] = 1

    for key in sorted(monograms):
        if len(key) == 3:
            print key, monograms[key]


def permutationCipher():
    pass


def oneTimePad():
    pass


def main():
    frequencyAnalysis()
    indexOfCoincidence()
    dataFile.close()


main()
