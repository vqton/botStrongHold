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
# from startapp import login, startapp

sText = ''

isExisting = False
iSecondSleep = 10


def activeWndStrongHold():
    win = gw.getWindowsWithTitle('Stronghold Kingdoms - World 11')[0]
    win.activate()
    win.restore()





def letGo():
    posGo = gui.locateOnScreen(
        'images/scout/butGo.png', grayscale=True, confidence=0.7)
    time.sleep(3)
    clickPOS(gui.center(posGo))
    pass


def sendScout():
    try:
        posCollect = gui.locateOnScreen(
            r'images\scout\scout.png', grayscale=True, confidence=0.7)
        time.sleep(3)
        pts = gui.center(posCollect)
        clickPOS(pts)
        gui.screenshot(r'temp\sample.png')
        time.sleep(0.5)
        
        
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
        print(spathRes)
        posResource = gui.locateOnScreen(
           spathRes, grayscale=True, confidence=0.8)
        time.sleep(5)
        if posResource is not None:
            return gui.center(posResource)


def getResource(sResource):
    posResource = getPosRes(sResource)
    time.sleep(3)
    if isinstance(posResource, type(None)):
        return None
    else:
        print(f'{sResource}: ({posResource.y},{posResource.y})')
        clickPOS(posResource)
        sendScout()


lstRes = ['stash', 'wood', 'stone', 'iron', 'cheese','meat']

activeWndStrongHold()
clickWorldButton()
for i in range(0, len(lstRes)):
    # print(lstRes[i])
    getResource(lstRes[i])
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
