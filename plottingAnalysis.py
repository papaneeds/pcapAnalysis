import pandas as pd
import matplotlib.pyplot as plt

eventFilename = '/home/tom/Documents/pcapAnalysis/Events.txt'
eventsDf = pd.read_csv(eventFilename, sep=':')
eventsDf['Time'] = eventsDf['Time'].astype('float')

print(eventsDf)
print(eventsDf.columns)

processedPcapData = '/home/tom/Documents/WiresharkCaptures/processedJunk.txt'
pcapDf = pd.read_csv(processedPcapData)
print(pcapDf)
print(pcapDf.columns)
print(pcapDf.dtypes)

outputPlotName = "/home/tom/Documents/pcapAnalysis/bytesPerSecond.png"

# Now, plot the two time series

# For fun, try creating another column to plot. Move this column to the right
# by a second
pcapDf['Time2'] = pcapDf['Time']+1

# Convert the times to dates (for easier plotting visualization)
eventsDf['Time'] = pd.to_datetime(eventsDf['Time'], unit='s')
pcapDf['Time']  = pd.to_datetime(pcapDf['Time'], unit='s')
pcapDf['Time2'] = pd.to_datetime(pcapDf['Time2'], unit='s')

print(pcapDf['Time'])
print(pcapDf.dtypes)

ax = pcapDf.plot(x='Time')

pcapDf.plot(x='Time', y='Bytes Per Second')
pcapDf.plot(ax=ax, x='Time2', y='Bytes Per Second')

# Now, annotate the plot with the events
yMax = pcapDf['Bytes Per Second'].max()*(0.7)
print(yMax)

for i in range(len(eventsDf['Time'])):
    print(eventsDf['Time'][i], eventsDf['Event'][i])
    plt.annotate(eventsDf['Event'][i], xy=(eventsDf['Time'][i], 0.0), xytext=(eventsDf['Time'][i], yMax), arrowprops=dict(arrowstyle="->"), rotation=90)
    # plt.annotate(eventsDf['Event'][i], xy=(eventsDf['Time'][i], 0.0), rotation=90)

# Add a y-axis label
plt.ylabel('Bytes Per Second')
plt.savefig(outputPlotName)
plt.show()














