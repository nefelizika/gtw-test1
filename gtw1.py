from bluepy.btle import Scanner, DefaultDelegate
from dotenv import load_dotenv
import os
import requests
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    #Not needed yet
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ('Discovered device', dev.addr)
        elif isNewData:
            print ('Received new data from', dev.addr)

#------------------------------------------------------

load_dotenv()
IP = os.environ.get('IP')
URL = 'http://{}/'.format(IP)

def filterDevices(devices):
    beacons=set()
    for dev in devices:
        if dev.addr[:-3]=="48:23:35:00:00":
            beacons.add(dev)
    return beacons

def scanDevices(scanner):
    devices=scanner.scan(5, passive=True)
    beacons=filterDevices(devices)
    (viewers, msgList)=getData(beacons)
    r=requests.post(url=URL+'save',data={'viewers':viewers, 'msgList':msgList})
    print(r.text)

def getData(beacons):
    viewers=[]
    msgList=[]
    for beac in beacons:
        viewers.append(beac.addr)
        msgList.append(beac.getScanData()[0][2])
    return (viewers, msgList)

#------------------------------------------------------

testScans=['First','Second','Third']
scanner=Scanner()

try:
    r=requests.post(url=URL+'clear')
    scanNum = 1
    for scan in testScans:
        print('{} Scan\n{}'.format(scan,(len(scan)+5)*'-'))
        scanDevices(scanner)
        if scanNum<len(testScans):
            print('Program pausing for 5s to adjust the beacons...')
            time.sleep(5)
            scanNum+=1
        print('\n')
    r=requests.get(url=URL+'view')
    print('Viewers and their respective viewing duration:\n{}'.format(r.text))

except requests.exceptions.RequestException as e:
    print('Server closed\nExiting...')