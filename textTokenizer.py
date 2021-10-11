
#The miscellaneous operating system interfaces will be used to determine whether the file read is a valid file
import os
#The regular expression operations will be used at various points during the Porter Stemmer process
import re

#These libraries will only be used to plot the graph of the vocabulary and collection in Moby Dick
#At no point are these libraries used in Part A of the project
import matplotlib.pyplot as plt
import numpy as np

vocabularyWordCounts = []
curVocabularyIndex = 0

collectionWordCounts = []
curCollectionIndex = 0

#The stopwords array will be used to contain all the words from stopwords.txt
#These words will be removed after running tokenization
stopwords = []
with open('stopwords.txt', 'r') as stopwordsFile:
    stopwordsLines = stopwordsFile.readlines()
    for line in stopwordsLines:
        stopwords.append(line.strip())

#The user determines which file they wish determines which file to read from
textFile = input("Enter the name of the text file you wish to read (E.g., 'Moby-Dick.txt'): ")

#As long as the user types an invalid file name, prompt them for a different input
while not os.path.isfile(textFile):
    textFile = input("Please enter a valid file name: ")


#PART A: IMPLEMENT A TOKENIZATION SYSTEM
#The inputWords array will contain all the words of a given text file after running tokenization on it
inputWords = []

#The vowels and consostants arrays will be used during the Porter Stemming Algorithm
vowels = ['a', 'e', 'i', 'o', 'u']
consonants = ['q', 'w', 'r', 't', 'y', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']

#The given file gets opened in 'read' mode with the correct encoding
with open(textFile, 'r', encoding="utf8") as inputAFile:
    #Read each line from the file individually
    for line in inputAFile:
        for word in line.split():

            #If conditionMet is set to True, then word has already been altered and should not be further modified
            #conditionMet is set to True whenever the word is modified
            conditionMet = False
            
            #Tokenization Implementation
            #Each word and number is split based on whitespaces and all punctuation except for periods
            wordSplit = []
            wordSplit = re.split('[^a-zA-Z0-9\.]', word)


            for splitWord in wordSplit:

                #The periods get removed from the words once they have been split
                splitWord = re.sub('\.', '', splitWord)

                #Each word needs to be set to lowercase before stopword removal begins
                splitWord = splitWord.lower()

                #Stopword Removal Implementation (implemented after tokenization and before stemming)
                if splitWord != '' and not splitWord in stopwords:

                    #Porter Stemming Step 1a
                    #4.
                    #Do nothing if the suffix is 'us' or 'ss'
                    if re.search('us$', splitWord) or re.search('ss$', splitWord):
                        conditionMet = True

                    #1.
                    #Replace the suffix 'sses' by 'ss'
                    if re.search('sses$', splitWord) and conditionMet == False:
                        splitWord = re.sub('sses$', 'ss', splitWord)
                        conditionMet = True

                    #3.
                    #Replace 'ied' or 'ies' by 'i' if preceded by more than one letter
                    #Otherwise, replace it by 'ie'
                    if re.search('ied$', splitWord) and len(splitWord) > 4 and conditionMet == False:
                        splitWord = re.sub('ied$', 'i', splitWord)
                        conditionMet = True
                    if re.search('ied$', splitWord) and len(splitWord) <= 4 and conditionMet == False:
                        splitWord = re.sub('ied$', 'ie', splitWord)
                        conditionMet = True
                    if re.search('ies$', splitWord) and len(splitWord) > 4 and conditionMet == False:
                        splitWord = re.sub('ies$', 'i', splitWord)
                        conditionMet = True
                    if re.search('ies$', splitWord) and len(splitWord) <= 4 and conditionMet == False:
                        splitWord = re.sub('ies$', 'ie', splitWord)
                        conditionMet = True

                    #2.
                    #Delete 's' if the preceding word part contains a vowel not immediately before the 's'
                    if len(splitWord) > 2 and conditionMet == False:
                        newSplitWord = splitWord[:len(splitWord) - 2]
                        if any(i in vowels for i in newSplitWord) and splitWord[-1] == 's':
                            conditionMet = True
                            splitWord = splitWord[:len(splitWord) - 1]


                    #Porter Stemming Step 1b
                    #1.
                    #Replace 'eed', 'eedly' by 'ee' if it is in the part of the word after the first nonvowel
                    #following a vowel
                    if re.search('eed$', splitWord) and splitWord[-4] in consonants and conditionMet == False:
                        conditionMet = True
                        newSplitWord = splitWord[:len(splitWord) - 3]
                        if any(i in vowels for i in newSplitWord):
                            splitWord = re.sub('eed$', 'ee', splitWord)
                    if re.search('eedly$', splitWord) and splitWord[-6] in consonants and conditionMet == False:
                        conditionMet = True
                        newSplitWord = splitWord[:len(splitWord) - 5]
                        if any(i in vowels for i in newSplitWord):
                            splitWord = re.sub('eedly$', 'ee', splitWord)

                    #2.
                    #Delete 'ed', 'edly', 'ing', or 'ingly' if the preceding word part contains a vowel
                    #Then, if the word ends in 'at', 'bl', or 'iz', add an 'e'
                    #Otherwise, if the word ends with a double letter that is not 'll', 'ss', or 'zz', remove the last letter
                    #Afterwards, if the word is short (length <= 3), add an 'e'
                    doubleLetterChecklist = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 'd', 'f', 'g', 'h', 'j', 'k', 'x', 'c', 'v', 'b', 'n','m']
                    if re.search('ed$', splitWord) and conditionMet == False:
                        newSplitWord = splitWord[:len(splitWord) - 2]
                        conditionMet = True
                        if any(i in vowels for i in newSplitWord):
                            splitWord = newSplitWord
                            if re.search('at$', splitWord) or re.search('bl$', splitWord) or re.search('iz', splitWord) or len(splitWord) <= 3:
                                splitWord += 'e'
                            elif splitWord[-1] == splitWord[-2] and splitWord[-1] in doubleLetterChecklist:
                                splitWord = splitWord[:len(splitWord) - 1]
                    if re.search('edly$', splitWord) and conditionMet == False:
                        newSplitWord = splitWord[:len(splitWord) - 4]
                        conditionMet = True
                        if any(i in vowels for i in newSplitWord):
                            splitWord = newSplitWord
                            if re.search('at$', splitWord) or re.search('bl$', splitWord) or re.search('iz', splitWord) or len(splitWord) <= 3:
                                splitWord += 'e'
                            elif splitWord[-1] == splitWord[-2] and splitWord[-1] in doubleLetterChecklist:
                                splitWord = splitWord[:len(splitWord) - 1]
                    if re.search('ing$', splitWord) and conditionMet == False:
                        newSplitWord = splitWord[:len(splitWord) - 3]
                        conditionMet = True
                        if any(i in vowels for i in newSplitWord):
                            splitWord = newSplitWord    
                            if re.search('at$', splitWord) or re.search('bl$', splitWord) or re.search('iz', splitWord) or len(splitWord) <= 3:
                                splitWord += 'e'
                            elif splitWord[-1] == splitWord[-2] and splitWord[-1] in doubleLetterChecklist:
                                splitWord = splitWord[:len(splitWord) - 1]
                    if re.search('ingly$', splitWord) and conditionMet == False:
                        newSplitWord = splitWord[:len(splitWord) - 5]
                        conditionMet = True
                        if any(i in vowels for i in newSplitWord):
                            splitWord = newSplitWord
                            if re.search('at$', splitWord) or re.search('bl$', splitWord) or re.search('iz', splitWord) or len(splitWord) <= 3:
                                splitWord += 'e'
                            elif splitWord[-1] == splitWord[-2] and splitWord[-1] in doubleLetterChecklist:
                                splitWord = splitWord[:len(splitWord) - 1]


                    #Finally, as long as the word is not short (length <= 3), append it to the input words array
                    if len(splitWord) > 3:

                        if splitWord not in inputWords:
                            if len(vocabularyWordCounts) > 0:
                                totalVocabularyWords = len(vocabularyWordCounts)
                                vocabularyWordCounts.append(vocabularyWordCounts[totalVocabularyWords - 2] + 1)
                            else:
                                vocabularyWordCounts.append(1)

                        collectionWordCounts.append(curCollectionIndex + 1)
                        curCollectionIndex += 1
 

                        inputWords.append(splitWord)



#If the user selected the 'tokenization-input-part-A.txt' file, open the file and write the tokenized input onto it
if textFile == 'tokenization-input-part-A.txt':
    with open('tokenized.txt', 'w', encoding="utf8") as outputAFile:
        for word in inputWords:
            outputAFile.write(word + '\n')


#PART B: EXPLORE THE MOST FREQUENT TERMS IN A LONGER DOCUMENT
#The Counter will be used to rank the 200 most common words in Moby-Dick.txt
from collections import Counter
with open('terms.txt', 'w', encoding="utf8") as outputAFile:
    c = Counter(inputWords)
    for word in c.most_common(200):
        outputAFile.write(word[0] + ' ' + str(word[1]) + '\n')

#Write down the values of the collection word count and vocabulary word count at each point for future reference
with open('vocabularyToCollectionGrowth.txt', 'w', encoding="utf8") as outputAFile:
    curIndex = 0
    while (curIndex < len(vocabularyWordCounts)):
        outputAFile.write(str(vocabularyWordCounts[curIndex]) + ' ' + str(collectionWordCounts[curIndex]) + '\n')
        curIndex += 1

    while (curIndex < len(collectionWordCounts)):
        outputAFile.write(str(collectionWordCounts[curIndex]) + '\n')
        curIndex += 1
 

    # Plot the Graph for the collection and vocabulary word counts in Moby Dick
    collectionWordCounts = collectionWordCounts[:len(vocabularyWordCounts)]

    plt.plot(collectionWordCounts, vocabularyWordCounts)
    plt.title("Vocabulary and Collection Growth Comparison")
    plt.xlabel("Collection Word Count")
    plt.ylabel("Vocabulary Word Count")
    plt.show()
