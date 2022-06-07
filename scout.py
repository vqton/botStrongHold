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
    time.sleep(3)
    clickPOS(gui.center(posGo))
    pass


def isNotAvailableScout():
    posScout = gui.locate(
        r'images\scout\zeroscout.png', r'temp\sample.png', grayscale=True)
    time.sleep(3)
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
        time.sleep(3)
        pts = gui.center(posCollect)
        clickPOS(pts)

        gui.screenshot(r'temp\sample.png')
        time.sleep(1)

        isAS = isNotAvailableScout()

        if isAS == True:
            pos = gui.locateOnScreen(r'images/scout/closeBtn.png')
            ps1 = gui.center(pos)
            clickPOS(ps1)
            time.sleep(3)

        time.sleep(5)
        sTime = core()
        a = ""
        for x in sTime:
            if x.isdigit():
                a = a+x
        sec = int(a[:2]) * 60 + int(a[-2:])

        f = open(r'temp\data.txt', 'w')
        f.write(str(sec))
        f.close()

        time.sleep(0.5)
        letGo()
    except Exception as e:
        print(e)
        pass


def clickWorldButton():
    try:
        time.sleep(5)
        posMapBtn = gui.locateOnScreen(
            r'images/collectRes/map.png', grayscale=True, confidence=0.75)
        time.sleep(3)
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
        time.sleep(5)
        if not isinstance(posResource, type(None)):
            pts = gui.center(posResource)
            print(f'Found {sResource} at {pts.x},{pts.y}')
            return pts


def getResource(sResource):
    posResource = getPosRes(sResource)
    time.sleep(3)
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
        time.sleep(3)
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

for i in range(0, len(lstRes)):
    f = open(r'temp\data.txt', 'r')
    line = f.readline()
    f.close()
    time.sleep(int(line[0]))
    print(line)
    getResource(lstRes[i])

gui.alert('Done')
# pos = getPosRes(r'images\collectRes\stash2.png')
# posResource = gui.locateOnScreen(
#     r'images\collectRes\stash3.png')
# time.sleep(3)
# print(type(posResource))
# gui.moveTo(gui.center(posResource).x, gui.center(posResource).y, 3)
# getResource('stone')
# def getResources(sResource):
#     try:
#         if getPos(sResource) is not None:
#             time.sleep(3)
#             print(f'Found {sResource} at ({pts.x},{pts.y}), ')
#             time.sleep(3)
#             gui.mouseDown(pts.x, pts.y)
#             time.sleep(1)
#             gui.mouseUp(pts.x, pts.y)
#             time.sleep(5)

#         sendScout()

#         gui.screenshot('temp/sample.jpg')
#         sTime = core()
#         char_to_replace = {'h': '',
#                            'm': '',
#                            's': '',
#                            ':': ''}
#         sTime = sTime.translate(str.maketrans(char_to_replace)).strip()

#         iSecondSleep = int(sTime[:2]) * 60 + int(sTime[-2:])
#         text_file = open("temp/data.txt", "w")

#         # write string to file
#         n = text_file.write(str(iSecondSleep))
#         # close file
#         text_file.close()
#         print(iSecondSleep)

#         time.sleep(5)
#         letGo()
#         time.sleep(3)
#     except Exception as e:
#         print(f'getResources: {e}')
#         isExisting = True
#         exit(1)


# try:
#     win = gw.getWindowsWithTitle('Stronghold Kingdoms - World 11')[0]
#     win.activate()
#     win.restore()
# except Exception as e:
#     print(e)
#     startapp()
#     time.sleep(30)
#     login()
#     time.sleep(15)
