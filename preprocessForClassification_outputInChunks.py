# This python program pre-processes data for Machine
# Learning classification.
# It outputs the results one chunk at a time in a dataframe every timeInterval seconds.
#
# It also randomly will remove lines that match the regularExpression, and classify these lines
# as "1" (positive). The lines that don't match the regular expression are classified as "0" (negative)

from time import sleep
import pandas as pd
import sys
import datetime
import pickle
import re
import random

# read in the training data file

# do a brutally simple command line argument extraction
# argparse is probably a better way to go, but for now just
# do this.
# timeInterval is given in units of seconds
# classification is an integer
[program, trainingInputFilename, dictionaryFilename, timeInterval, regularExpression, outputFilename] = sys.argv
timeInterval = float(timeInterval)

trainingDf = pd.read_csv(trainingInputFilename)
# first, replace all the NaN values with ''
trainingDf['notes'].fillna('', inplace=True)
print(trainingDf.head())

# Read in the dictionary as a hashmap
dictionary = {}
fp = open(dictionaryFilename)
line = fp.readline()
cnt = 0
while line:
    dictionary[cnt] = line.strip()
    print("Line {}: {}".format(cnt, dictionary[cnt]))
    line = fp.readline()
    cnt += 1

print(dictionary)

# Split the dataframe into time chunks of timeInterval
# and create a list of all the 'words' that appear in the 
# chunk.
# Each chunk will be a row in our training data frame.
# Each chunk should be representative of a big enough slice in time
# that all the "normal" traffic should appear in it.

ignorePacketsMathingRegex = False

# a variable to keep track of the words that have occurred in the timeChunk
nextRow = {}

for index, row in trainingDf.iterrows():
    #print("at top of loop")
    #print(index, row['timestamp'], row['notes'])
    resetNextRow = False
    timestampAsString = row['timestamp']
    timestamp = datetime.datetime.fromisoformat(timestampAsString)
    if (index == 0):
        startTimestamp = timestamp
        resetNextRow = True


    if timestamp > (startTimestamp + datetime.timedelta(seconds=timeInterval)):
        print('time rolled over!', startTimestamp, timestamp)
        startTimestamp = timestamp
        resetNextRow = True

    if resetNextRow:

        if (index != 0):
            print('Writing dataset to file')

            # Create a new output dataframe to hold our output training data
            # This training data will have the same number of columns as the dictionary has rows

            outputDf = pd.DataFrame()
            for key in dictionary:
                #outputDf[dictionary[key]] = []
                outputDf[key] = []

            new_df = pd.DataFrame.from_dict(nextRow)
            outputDf = pd.concat([outputDf, new_df], axis=0, ignore_index=True)
            #print(outputDf)

            # create a series which holds the training set "classfier". The classifier
            # has the same number of rows as the outputDf has rows
            numRowsInDf = len(outputDf.index)
            classification = False
            if (ignorePacketsMathingRegex == True):
                classification = True
            ylist = [int(classification)] * numRowsInDf
            y = pd.Series(ylist)

            #print(y)

            # write this as a dataset to file

            dataSet = {}
            dataSet['data'] = outputDf
            dataSet['target'] = y

            print(dataSet)
            outputFile = open(outputFilename, 'wb')
            pickle.dump(dataSet, file=outputFile)

            # Now, pause for timeInterval seconds to simulate the gathering of data
            sleep(int(10))
            
        # Randomly decide to ignore packets matching the regular expression
        ignorePacketsMathingRegex = random.choice([True, False])
        #ignorePacketsMathingRegex = True
        if (ignorePacketsMathingRegex == True):
            print("Classification of upcoming timeInterval=1")
        else:
            print("Classification of upcoming timeInterval=0")

        print("resetting nextRow")
        nextRow = {}
        for key in dictionary:
            #nextRow[dictionary[key]] = [0]
            nextRow[key] = [0]


    # Look to see if the regular expression matches the 'notes' or 'type' field
    if ((ignorePacketsMathingRegex == True) and
        (re.search(regularExpression, row['type']) or re.search(regularExpression, row['notes']))):
            print ("ignoring this line. Regex=", regularExpression, " type=", row['type'], " notes=", row['notes'])
    else:
        # now, look at the 'notes' field and the 'type' field and see if they occur in the dictionary   
        for key in dictionary:
            #print('Comparing the dictionary to the dataset row')
            #print('dictionary key=', key, ' value=', dictionary[key])
            #print('dataset index=' +  str(index) + ' row[type]=' + row['type'] + ', row[notes]=' + str(row['notes']))

            # randomly remove lines that match the regular expression

            if (dictionary[key] == row['type']):
                #print ('match found on type!')
                #nextRow[dictionary[key]] = [1]
                nextRow[key] = [1]
            elif (dictionary[key] == row['notes']):
                #print ('match found on notes!')
                #nextRow[dictionary[key]] = [1]
                nextRow[key] = [1]










