samplingFrequency = 2000000
satellites = [20, 11, 25, 2, 5, 12, 29, 19]

import os
import csv
import matplotlib.pyplot as plt

currentFolder = os.path.dirname(os.path.realpath(__file__))
snrDumpFolder = f'{currentFolder}/data'
dataPointsToSkip = 2000

def prnFileExists(prn):
    return os.path.exists(f'{snrDumpFolder}/snr_prn_{prn}.csv')

def getProcessedSatellites():
    allSatellites = []
    if 'satellites' in globals():
        allSatellites = satellites
    else:
        allSatellites = [i for i in range(1, 33)]
    processedSatellites = list(filter(prnFileExists, allSatellites))
    print(f'Processed SNR CSV files exist for PRNs: {processedSatellites}')
    return processedSatellites
    
def getSatelliteData(prn):
    csvFile = open(f'{snrDumpFolder}/snr_prn_{prn}.csv')
    csvReader = csv.reader(csvFile)
    xs, ys = [], []
    for row in csvReader:
        xs.append(int(row[0]) / samplingFrequency)
        ys.append(float(row[1]))
    return (xs[dataPointsToSkip:], ys[dataPointsToSkip:])

def main():
    sats = getProcessedSatellites()
    satData = [getSatelliteData(sat) for sat in sats]
    handles = []

    for (xs, ys) in satData:
        handle, = plt.plot(xs, ys)
        handles.append(handle)
    plt.legend(handles, sats, loc='lower left')
    plt.show()

main()
