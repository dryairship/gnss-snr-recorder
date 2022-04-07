samplingFrequency = 2000000
rawDataFileName = '/mnt/mewis/Academics/ugp_AE471A/realdata/data/raw_hackrf2.dat'
satellites = [20, 11, 25, 2, 5, 12, 29, 19]

import os
import subprocess

currentFolder = os.path.dirname(os.path.realpath(__file__))
defaultConfigFileName = f'{currentFolder}/default-gnss-config.conf'
tmpFolder = f'{currentFolder}/tmp'
tmpConfigFileName = f'{tmpFolder}/tmp-config.conf'
snrDumpFolder = f'{currentFolder}/data'


def readConfigFile():
    configFile = open(defaultConfigFileName, mode='r')
    configFileText = configFile.read()
    configFile.close()
    return configFileText

def updateConfig(defaultConfig, prn):
    newConfig = defaultConfig
    newConfig += '\n'

    newConfig += f'GNSS-SDR.internal_fs_sps={samplingFrequency}\n'
    
    newConfig += f'SignalSource.sampling_frequency={samplingFrequency}\n'
    newConfig += f'SignalSource.filename={rawDataFileName}\n'
    
    newConfig += f'Channels_1C.count=1\n'
    newConfig += f'Channels.in_acquisition=1\n'
    newConfig += f'Channel0.satellite={prn}\n'

    newConfig += f'SNR.dump=true\n'
    newConfig += f'SNR.dump_filename={snrDumpFolder}/snr_prn_\n'

    return newConfig

def writeTmpConfigFile(config):
    newConfigFile = open(tmpConfigFileName, mode = 'w')
    newConfigFile.write(config)
    newConfigFile.close()

def getSatellites():
    if 'satellites' in globals():
        return satellites
    else:
        return [i for i in range(1, 33)]

def runGNSS():
    p = subprocess.Popen(['gnss-sdr', f'--config_file={tmpConfigFileName}'], cwd=tmpFolder, stdout=subprocess.PIPE, bufsize=32)
    print('Processed: 0 s', end='', flush=True)
    while True:
        line = str(p.stdout.readline().rstrip(), 'utf-8')
        if not line:
            break
        if line.startswith('Current receiver time:'):
            print(f'\rProcessed: {line[23:]}   ', end='', flush=True)
    print('\rProcessing complete                                            ')

def main():
    os.makedirs(tmpFolder, exist_ok=True)
    os.makedirs(snrDumpFolder, exist_ok=True)
    sats = getSatellites()
    defaultConfig = readConfigFile()
    for sat in sats:
        satConfig = updateConfig(defaultConfig, sat)
        writeTmpConfigFile(satConfig)
        print(f'Started processing data for PRN {sat}')
        runGNSS()
    print('All satellites processed')

main()
