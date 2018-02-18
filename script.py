import pygame
import sys
import random


# monograms
monograms = {}

# digrams
digrams = {}

dataFile = open(sys.argv[1], 'r')
text = dataFile.read()


def frequencyAnalysis(text):
    for x in text:
        if monograms.has_key(x):
            monograms[x] += 1
        else:
            monograms[x] = 1

    for key in monograms:
        print key, monograms[key]

    for i, j in zip(text[::2], text[1::2]):
        key = i + j
        if monograms.has_key(key):
            monograms[key] += 1
        else:
            monograms[key] = 1

    for key in sorted(monograms):
        if len(key) == 2:
            print key, monograms[key]


def indexOfCoincidence(monograms):
    # index of Coincidence
    pass


def typeOfCipher(text):
    pass


def shiftCipher(text):
    pass


def subCipher(text):
    pass


def vigenereCipher(text):
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


def permutationCipher(text):
    pass


def oneTimePad(text):
    pass


def main():
    frequencyAnalysis(text)

    dataFile.close()


main()
