# This program removes all lines in a file that contain a regex

import sys
import re

[program, inputFilename, outputFilename, regularExpression] = sys.argv
#regularExpression = str(regularExpression)

# Read in the dictionary as a hashmap
fpIn = open(inputFilename)
fpOut = open(outputFilename, "w")

line = fpIn.readline()
cnt = 0
while line:
    # Check to see if the line matches the regex
    if (not re.search(regularExpression, line)):
        fpOut.write(line)
    else:
        print("expression found!", regularExpression, line)
    #print("Line {}: {}".format(cnt, lineIn))
    line = fpIn.readline()
    cnt += 1

