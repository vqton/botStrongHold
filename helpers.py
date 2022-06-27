import win32gui
import random
import pyautogui as gui
import time
import re
import math
import json
from dict2xml import dict2xml

from os import listdir
from os.path import isfile, join

results = []
top_windows = []


def doubleClickPos(pts):
    gui.moveTo(pts[0], pts[1])
    time.sleep(0.5)
    gui.click(pts[0], pts[1], 2)
    time.sleep(3)


def parseString2Tuple(s):
    a = s.split(",")
    return (int(a[0]), int(a[1]))


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def wrtXmlSetting(fileName, data):
    with open(fileName, "w") as xFile:
        xFile.write(dict2xml(data, wrap="root"))


def wrtJSONSettings(fileName, data):
    with open(fileName, "w+") as f:
        json.dump(data, f)


def convertTime2Second(sTime):
    a = re.sub("[^0-9]+", "", sTime)

    try:
        min2sec = int(a[:2])
        sec = (min2sec * 60) + int(a[-2:])
        return sec
    except Exception as e:
        return 240


def get_distance(a, b):
    return math.dist(a, b)


def BringWindow2Front(sName):
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if sName.lower() in i[1].lower():
            print(i)
            win32gui.ShowWindow(i[0], 5)
            win32gui.SetForegroundWindow(i[0])
            break


def clickPOS(pts):
    second = random.uniform(0.1, 0.999)
    gui.moveTo(pts[0], pts[1])
    time.sleep(second)
    gui.mouseDown(pts[0], pts[1])
    time.sleep(second)
    gui.mouseUp(pts[0], pts[1])
    time.sleep(second)


def getListFiles(sPath):
    onlyfiles = [f for f in listdir(sPath) if isfile(join(sPath, f))]
    return onlyfiles


def AddUpdateValueDict(dctName, item, pts):
    dctName[item] = f"{int(pts[0])},{int(pts[1])}"
    wrtJSONSettings("settings.xml", dctName)
