from functools import reduce
import os
import fnmatch
from posixpath import split
import pygetwindow as gw
import time
import pyautogui as gui
# from helpers import *
# from ocr import core
# from startapp import login, startapp

sText = ''

isExisting = False
iSecondSleep = 10


def activeWndStrongHold():
    win = gw.getWindowsWithTitle('Stronghold Kingdoms - World 11')[0]
    win.activate()
    win.restore()


def clickPOS(pts):
    gui.mouseDown(pts.x, pts.y)
    time.sleep(0.5)
    gui.mouseUp(pts.x, pts.y)
    time.sleep(3)


def letGo():
    posGo = gui.locateCenterOnScreen(
        'images/collectRes/butGo.png', grayscale=True, confidence=0.7)
    time.sleep(3)
    clickPOS(gui.center(posGo))
    pass


def sendScout():
    posCollect = gui.locateCenterOnScreen(
        'images/collectRes/scout.png', grayscale=True, confidence=0.7)
    time.sleep(3)
    clickPOS(gui.center(posCollect))


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
    resImgpath = r'images\collectRes\stash3.png'

    posResource = gui.locateOnScreen(
        resImgpath, grayscale=True, confidence=0.5)
    time.sleep(5)
    if posResource is None:
        return None
    else:
        return gui.center(posResource)


def getResource(sResource):
    posResource = getPosRes(sResource)
    time.sleep(3)
    print(type(posResource))
    if posResource is None:
        gui.alert('Resource not found', 'Get Resource')
        exit(0)
    else:
        clickPOS(posResource)


activeWndStrongHold()
# pos = getPosRes(r'images\collectRes\stash2.png')
posResource = gui.locateOnScreen(
    r'images\collectRes\stash3.png')
time.sleep(3)
print(type(posResource))
gui.moveTo(gui.center(posResource).x, gui.center(posResource).y, 3)
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
