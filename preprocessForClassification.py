# This python program pre-processes data for Machine
# Learning classification

from tracemalloc import start
import pandas as pd
import sys
import datetime

# read in the training data file

# do a brutally simple command line argument extraction
# argparse is probably a better way to go, but for now just
# do this.
# timeInterval is given in units of seconds
[program, trainingFilename, dictionaryFilename, timeInterval] = sys.argv
timeInterval = float(timeInterval)

trainingDf = pd.read_csv(trainingFilename)
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
    print("Line {}: {}".format(cnt, line.strip()))
    line = fp.readline()
    cnt += 1

print(dictionary)

# Split the dataframe into time chunks of timeInterval
# and create a list of all the 'words' that appear in the 
# chunk.
# Each chunk will be a row in our training data frame.
# Each chunk should be representative of a big enough slice in time
# that all the "normal" traffic should appear in it.

chunkIndex = 0

# Create a new output dataframe to hold our output training data
# This training data will have the same number of columns as the dictionary has rows

outputDf = pd.DataFrame()
for key in dictionary:
    #outputDf[dictionary[key]] = []
    outputDf[key] = []

print(outputDf)

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
        new_df = pd.DataFrame.from_dict(nextRow)
        outputDf = pd.concat([outputDf, new_df], axis=0, ignore_index=True)
        resetNextRow = True

    if resetNextRow:
        print("resetting nextRow")
        nextRow = {}
        for key in dictionary:
            #nextRow[dictionary[key]] = [0]
            nextRow[key] = [0]

    # now, look at the 'notes' field and the 'type' field and see if they occur in the dictionary   
    for key in dictionary:
        #print('Comparing the dictionary to the dataset row')
        #print('dictionary key=', key, ' value=', dictionary[key])
        #print('dataset index=' +  str(index) + ' row[type]=' + row['type'] + ', row[notes]=' + str(row['notes']))

        if (dictionary[key] == row['type']):
            #print ('match found on type!')
            #nextRow[dictionary[key]] = [1]
            nextRow[key] = [1]
        elif (dictionary[key] == row['notes']):
            #print ('match found on notes!')
            #nextRow[dictionary[key]] = [1]
            nextRow[key] = [1]

print(outputDf)







