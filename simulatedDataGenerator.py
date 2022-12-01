# This file generates simulated disk, cpu and memory data 
from dateutil import parser
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt
import math

timeStartString = '2022-12-01T09:00:00.000000' # ISO 8601 format
timeStart = parser.parse(timeStartString)
timeEndAfterStart = 12 # hours after start
timeEnd = timeStart + datetime.timedelta(hours=timeEndAfterStart)
timeInterval = 60 # units of seconds. This is how often we write out the metrics
currentTime = timeStart

secondsPerHour = 3600
deltaMax = 30.0
maxVal = 100
minVal = 15
numIntervals = 20
randomAmplitude = deltaMax * 0.01

t_0 = currentTime.timestamp() # seconds since 1970
delta = random.random()*timeEndAfterStart/numIntervals # hours for change
t_1 = t_0 + delta*secondsPerHour

period = math.pi/(delta*secondsPerHour)
m = delta/(t_1 - t_0)
y_0 = 22.0
sign = random.choice([-1, 1])
y = y_0 + sign*delta*(t_1 - t_0)/secondsPerHour

print("t_0=", t_0, " t_1=", t_1, " delta=", delta, " m=", m, " y_0=", y_0, " sign=", sign)
print("y=", y)
keepGoing = True

x_arr = []
y_arr = []

while (currentTime < timeEnd):

    t = currentTime.timestamp()
    randomAmount = math.sin(period*(t-t_0))
    y = y_0 + sign*delta*(t - t_0)/secondsPerHour + randomAmount
    print("currentTime=", currentTime, " t=", t, " y=", y)
    if (y > maxVal):
        y = maxVal
    elif (y < minVal):
        y = minVal
    x_arr.append(currentTime.isoformat())
    y_arr.append(y)

    if (t > t_1):
        # Reset the slopes, end time, etc
        t_0 = currentTime.timestamp() # seconds since 1970
        delta_t = random.random()*timeEndAfterStart/numIntervals # hours for change
        t_1 = t_0 + delta_t*secondsPerHour

        delta = random.random()*deltaMax
        m = delta/(t_1 - t_0)
        sign = random.choice([-1, 1])
        y_0 = y
    
    currentTime = currentTime + datetime.timedelta(seconds=timeInterval)

print(x_arr, y_arr)
plt.plot(x_arr, y_arr)
plt.show()

user_input = input("Do you want to save this graph? (y/n)")
if (user_input == 'y' or user_input == 'Y'):
    user_input = input("Enter the filename to write data to ")
    f = open(user_input, 'w')
    outpuString = "timestamp, memory\n"
    f.write(outpuString)
    for i in range(len(x_arr)):
        outputString = str(x_arr[i]) + "," + str(y_arr[i]) + "\n"
        f.write(outputString)

    f.close()




 