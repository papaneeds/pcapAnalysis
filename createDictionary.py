# This program creates a dictionary of words that are in the 'notes' and 'type'
# column of the inputFilename.
# This is used to create a word list for the "bag of words" text processing
# for Machine Learning classification.
# The output from this program is a file called "dictionary.csv"

import pandas as pd
import sys

# A function to find all the distinct values in a
# column of a dataframe and then remove newlines
# from the strings
def findDistinctValues(dictionary, df, column):    
    # Find all the distinct values for the column
    distinctValues = df[column].value_counts()
    for items in distinctValues.iteritems():
        # remove newlines from strings
        stringItem = str(items[0]).replace('\n', '')
        dictionary[stringItem] = items[1]

# Main program

# do a brutally simple command line argument extraction
# argparse is probably a better way to go, but for now just
# do this.
[program, inputFilename] = sys.argv

df = pd.read_csv(inputFilename)

dictionary = {}

# first, replace all the NaN values with ''
df['notes'].fillna('', inplace=True)

# Now, find all the distinct values in the dataframe
# and peel off any newlines.
# find the distinct values for the 'notes' and 'type' columns
findDistinctValues(dictionary, df, 'notes')
findDistinctValues(dictionary, df, 'type')

print(dictionary)

# Now, write the dictionary to file
f = open('dictionary.csv', 'w')
for key in dictionary:
    f.write(key.replace('\n', '') + '\n')
f.close()