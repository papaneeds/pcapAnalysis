# This file generates simulated disk, cpu and memory data 
from dateutil import parser
import datetime
import random

timeStartString = '2022-12-01T09:00:00.000000' # ISO 8601 format
timeStart = parser.parse(timeStartString)
timeEndAfterStart = 12 # hours after start
timeEnd = timeStart + datetime.timedelta(hours=timeEndAfterStart)
timeInterval = 60 # units of seconds. This is how often we write out the metrics
currentTime = timeStart

secondsPerHour = 3600
deltaMax = 20.0

t_0 = currentTime.timestamp() # seconds since 1970
delta_t = random.random()*timeEndAfterStart # hours for change
t_1 = t_0 + delta_t*secondsPerHour

delta = random.random()*deltaMax
m = delta/(t_1 - t_0)
y_0 = 10.0
sign = random.choice([-1, 1])
y = y_0 + sign*delta*(t_1 - t_0)/secondsPerHour

print("t_0=", t_0, " t_1=", t_1, " delta=", delta, " m=", m, " y_0=", y_0, " sign=", sign)
print("y=", y)
keepGoing = True

while (currentTime < timeEnd):
    t = currentTime.timestamp()
    y = y_0 + sign*delta*(t - t_0)/secondsPerHour
    print("currentTime=", currentTime, " t=", t, " y=", y)

    if (t > t_1):
        # Reset the slopes, end time, etc
        t_0 = currentTime.timestamp() # seconds since 1970
        delta_t = random.random()*timeEndAfterStart # hours for change
        t_1 = t_0 + delta_t*secondsPerHour

        delta = random.random()*deltaMax
        m = delta/(t_1 - t_0)
        sign = random.choice([-1, 1])
    
    currentTime = currentTime + datetime.timedelta(seconds=timeInterval)






 