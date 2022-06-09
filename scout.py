from ocr import core
from functools import reduce
import os

import fnmatch
from posixpath import split
import sre_compile
import pygetwindow as gw
import time
import pyautogui as gui
from helpers import *

# from ocr import core
from startapp import login, startapp

sText = ''

isExisting = False
iSecondSleep = 10
TIME_LOCATING = 1

def activeWndStrongHold():

    try:
        win = gw.getWindowsWithTitle('Stronghold Kingdoms - World 11')[0]
        win.activate()
        win.restore()
    except Exception as e:
        startapp()
        time.sleep(5)
        login()
        time.sleep(5)


def letGo():
    posGo = gui.locateOnScreen(
        'images/scout/butGo.png', grayscale=True, confidence=0.7)
    time.sleep(TIME_LOCATING)
    clickPOS(gui.center(posGo))
    pass


def isNotAvailableScout():
    posScout = gui.locate(
        r'images\scout\zeroscout.png', r'temp\sample.png', grayscale=True)
    time.sleep(TIME_LOCATING)
    # pts = gui.center(posScout)
    # print('({pts.x},{pts.y})')
    # return isinstance(posScout, type(None))
    if posScout is not None:
        return True
    else:
        return False


def sendScout():
    try:
        posCollect = gui.locateOnScreen(
            r'images\scout\scout.png', grayscale=True, confidence=0.7)
        time.sleep(TIME_LOCATING)
        pts = gui.center(posCollect)
        clickPOS(pts)

        if isfile(r'temp\sample.png'):
            os.remove(r'temp\sample.png')

        gui.screenshot(r'temp\sample.png')
        time.sleep(TIME_LOCATING)

        isAS = isNotAvailableScout()

        if isAS == True:
            pos = gui.locateOnScreen(r'images/scout/closeBtn.png')
            ps1 = gui.center(pos)
            clickPOS(ps1)
            time.sleep(TIME_LOCATING)

        time.sleep(TIME_LOCATING)
        sTime = core()
        sec = convertTime2Secound(sTime)

        f = open(r'temp\data.txt', 'w')
        f.write(str(sec))
        f.close()

        time.sleep(0.5)
        letGo()
    except Exception as e:
        print(f'sendScout: {e}')
        pass


def clickWorldButton():
    try:
        time.sleep(5)
        posMapBtn = gui.locateOnScreen(
            r'images/collectRes/map.png', grayscale=True, confidence=0.75)
        time.sleep(TIME_LOCATING)
        clickPOS(gui.center(posMapBtn))
    except Exception as e:
        gui.alert(e, 'clickWorldButton')
        exit(1)


def getPosRes(sResource):
    sPath = 'images/collectRes/'+sResource+"/"
    lstFile = getListFiles(sPath)
    for f in lstFile:
        spathRes = join(sPath, f)
        posResource = gui.locateOnScreen(
            spathRes, grayscale=True, confidence=0.8)
        time.sleep(TIME_LOCATING)
        if not isinstance(posResource, type(None)):
            pts = gui.center(posResource)
            print(f'Found {sResource} at {pts.x},{pts.y}')
            return pts


def getResourceByPos(pts):
    clickPOS(pts)
    sendScout()


def getResource(sResource):
    posResource = getPosRes(sResource)
    time.sleep(TIME_LOCATING)
    if isinstance(posResource, type(None)):
        return None
    else:
        print(f'{sResource}: ({posResource.y},{posResource.y})')
        clickPOS(posResource)
        sendScout()


def clickHome():
    try:
        pos = gui.locateOnScreen(
            r'images\\home.png', grayscale=True, confidence=0.8)
        time.sleep(TIME_LOCATING)
        pts = gui.center(pos)
        # print(f'{pts.x}, {pts.y}')
        clickPOS(pts)
    except:
        print('An exception occurred')


lstRes = ['stash', 'apple', 'wood', 'stone', 'iron',
          'cheese', 'meat', 'clothes', 'bread']
# lstRes = ['bread', 'wood']

activeWndStrongHold()
clickWorldButton()
clickHome()


f = open(r'temp\data.txt', 'w')
f.write('0')
f.close()

# for i in range(0, len(lstRes)):
#     f = open(r'temp\data.txt', 'r')
#     line = f.readline()
#     f.close()
#     time.sleep(int(line[0]))
#     print(line)
#     getResource(lstRes[i])

# gui.alert('Done')


def isResourceExisting(sResource):
    pass


# hold postion of resources at dictionary
dctResource = {'stash': (0, 0), 'apple': (0, 0), 'wood': (0, 0), 'stone': (0, 0), 'iron': (0, 0),
               'cheese': (0, 0), 'meat': (0, 0), 'clothes': (0, 0), 'bread': (0, 0)}


def getAllResourcePos(dctRes):
    try:
        for k, v in dctRes.items():
            pts = getPosRes(k)
            if isinstance(pts, type(None)) == False:
                dctRes.update({k: (pts[0], pts[1])})
        print('done')
        return dctRes
    except Exception as e:
        gui.alert(e, 'getAllResourcePos')


getAllResourcePos(dctResource)
for k, v in dctResource.items():
    value = dctResource.get(k)
    print(f'{k}{value}')
    if not value == (0, 0):
        getResourceByPos(value)
gui.alert('done', 'getAllResourcePos')

# pts = (580, 651)
# getResourceByPos(pts)
exit(0)


print(dctResource)

for k, v in dctResource.items():
    pass

def main():
    pass

if __name__ == '__main__':
    main()
    